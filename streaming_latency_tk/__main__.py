import argparse
import os
import json

from streaming_latency_tk.resegment import resegment
from streaming_latency_tk.streaming_latency import compute_measures
from streaming_latency_tk.utils import load_file_to_list

TABS = "tabs"
TABLE = "table"
JSON = "json"


def main_cli():
    parser = argparse.ArgumentParser(prog="stream_latency")

    parser.add_argument("--hypotheses_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the system hypothesis.", metavar='HYPOTHESIS_FILE')
    parser.add_argument("--hypotheses_RW_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the sequence of READ/WRITE operations performed by the model. This "
                             "file should contain a single line of white-space separated symbols 'R' and 'W'.",
                        metavar='RW_FILE')
    parser.add_argument("--reference_source_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the source text. They will be used to compute the latency measures. "
                             "These should be the reference files with the original segmentation, they are not "
                             "affected by the actual segmentation used by your model.",
                        metavar='SRC_REFERENCE_FILE')
    parser.add_argument("--reference_target_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the reference text. The reference text is only used to re-align "
                             "the system hypothesis.",
                        metavar='TGT_REFERENCE_FILE')
    parser.add_argument("--penalty_scale_factor", type=float, default=1.0,
                        help="Scaling factor 's' used to scale the cost of the DAL write operations. s=1.0 behaves as "
                             "DAL, s=0.0 behaves as AL. A value close to, but not equal to 1 (i.e. 0.95) should be "
                             "used if one wishes to take long delays into account, but also to allow the system to "
                             "progressively recover if no more significant delays occur.")

    parser.add_argument("--remove_tokens_from_hypo", type=str, nargs="+", default=None, metavar='TOKEN',
                        help="Remove these tokens from the system output. Useful for removing meta-words "
                             "(i.e. [DOC], [SEP]) that are not present in the reference. If you use this option, your "
                             "system should not produce a W action when generating these tokens.")

    parser.add_argument("--read_action_repr", type=str, default="R", help="How READ actions are represented in "
                                                                          "the RW_FILE")
    parser.add_argument("--write_action_repr", type=str, default="W", help="How WRITE actions are represented in "
                                                                           "the RW_FILE")
    parser.add_argument("--output_format", type=str, choices=[TABS, TABLE, JSON], default=TABS,
                        help="How the output is formatted. 'tabs': Tab-separated columns, "
                             " 'json': json string, 'table': white-space formatted table")

    args = parser.parse_args()

    if args.remove_tokens_from_hypo is None:
        args.remove_tokens_from_hypo = []

    # If we are to process multiple files, we need to make sure that the exact number has been provided
    assert len(args.hypotheses_files) == len(args.reference_source_files) == len(args.reference_target_files) \
           == len(args.hypotheses_RW_files)

    headers = ["File", "AP", "AL", "DAL"]
    if args.output_format == TABS:
        print(f"{headers[0]}\t{headers[1]}\t{headers[1]}\t{headers[2]}")
    elif args.output_format == TABLE:
        print(f"{headers[0]:<40s} {headers[1]:>5s} {headers[1]:>5s} {headers[2]:>5s}")
    elif args.output_format == JSON:
        pass
    else:
        raise Exception

    json_output = []
    # Iterate over each tuple/hypothesis to score
    for hypo_file_fp, hypo_file_rw_fp, reference_src_fp, reference_tgt_fp \
            in zip(args.hypotheses_files, args.hypotheses_RW_files,
                   args.reference_source_files, args.reference_target_files):

        hypothesis = load_file_to_list(hypo_file_fp)
        if len(args.remove_tokens_from_hypo) > 0:
            hypothesis = [[x for x in sent if x not in args.remove_tokens_from_hypo] for sent in hypothesis]
        tgt_reference = load_file_to_list(reference_tgt_fp)

        # The reference translation is only used to re-align the system hypothesis
        aligned_hypothesis = resegment(hypothesis=hypothesis, reference=tgt_reference)

        # We expect the RW file to be a single line, however because we use a common function for reading
        # all text files, we first ensure that is is only one line, that we "flatten" it to a single list,
        # which is what is expected by compute_measures
        rw_stream = load_file_to_list(hypo_file_rw_fp)
        assert len(rw_stream) == 1
        rw_stream = rw_stream[0]

        src_reference = load_file_to_list(reference_src_fp)

        # With the re-aligned hypothesis, compute the evaluation measures using the re-aligned (src, tgt_hyp) pairs
        ap, al, dal = compute_measures(src_sentences=src_reference, tgt_sentences=aligned_hypothesis,
                                       actions=rw_stream, penalty_scale_factor=args.penalty_scale_factor,
                                       read_action_repr=args.read_action_repr,
                                       write_action_repr=args.write_action_repr)

        if args.output_format == TABS:
            print(f"{os.path.basename(reference_tgt_fp)}\t{ap:.1f}\t{al:.1f}\t{dal:.1f}")
        elif args.output_format == TABLE:
            print(f"{os.path.basename(reference_tgt_fp)[:40]:<40s} {ap:>5.1f} {al:>5.1f} {dal:>5.1f}")
        elif args.output_format == JSON:
            json_output.append({"file": os.path.basename(reference_tgt_fp),
                                "AP": ap,
                                "AL": al,
                                "DAL": dal})
        else:
            raise Exception

    if args.output_format == JSON:
        print(json.dumps(json_output))


if __name__ == "__main__":
    main_cli()
