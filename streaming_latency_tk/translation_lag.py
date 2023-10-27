import argparse
import math
import os.path
import json
from typing import List

from streaming_latency_tk.resegment import resegment
from streaming_latency_tk.utils import load_file_to_list, transfer_segmentation_to_list

def sentence_translation_lag(src_timestamps: List[float], target_lags: List[float]) -> float:
    assert len(src_timestamps) == len(target_lags)
    lags: List[float] = []
    for i in range(len(target_lags)):
        j = math.ceil(i * len(src_timestamps)/len(target_lags))
        lags.append(target_lags[i] - src_timestamps[j])
    return sum(lags)/len(lags)

def main_cli():
    parser = argparse.ArgumentParser(prog="stream_latency")

    parser.add_argument("--hypotheses_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the system hypothesis.", metavar='HYPOTHESIS_FILE')
    parser.add_argument("--hypotheses_lag_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the cost/lag in seconds of each of the WRITE operations performed "
                             "by the model. This file should contain a single line of white-space separated floats.",
                        metavar='LAG_FILE')
    parser.add_argument("--reference_source_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the source text. They will be used to compute the latency measures. "
                             "These should be the reference files with the original segmentation, they are not "
                             "affected by the actual segmentation used by your model.",
                        metavar='SRC_REFERENCE_FILE')
    parser.add_argument("--reference_source_json_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the source text and timestamps. Should be json files.",
                        metavar='SRC_JSON_FILE')
    parser.add_argument("--reference_target_files", nargs="+", type=str, required=True,
                        help="File(s) that contain the reference text. The reference text is only used to re-align "
                             "the system hypothesis.",
                        metavar='TGT_REFERENCE_FILE')
    parser.add_argument("--remove_tokens_from_hypo", type=str, nargs="+", default=None, metavar='TOKEN',
                        help="Remove these tokens from the system output. Useful for removing meta-words "
                             "(i.e. [DOC], [SEP]) that are not present in the reference. If you use this option, your "
                             "system should not produce a W action when generating these tokens.")
    parser.add_argument("--read_action_repr", type=str, default="R", help="How READ actions are represented in "
                                                                          "the RW_FILE")
    parser.add_argument("--write_action_repr", type=str, default="W", help="How WRITE actions are represented in "
                                                                           "the RW_FILE")
    args = parser.parse_args()

    if args.remove_tokens_from_hypo is None:
        args.remove_tokens_from_hypo = []

    # If we are to process multiple files, we need to make sure that the exact number has been provided
    assert len(args.hypotheses_files) == len(args.reference_source_files) == len(args.reference_target_files) == len(args.hypotheses_lag_files) == len(args.reference_source_json_files)

    # Only TABS format for now
    headers = ["File", "TL"]
    print(f"{headers[0]}\t{headers[1]}")

    for hypo_file_fp, reference_src_fp, reference_tgt_fp, lag_file_fp, reference_json_file_fp \
            in zip(args.hypotheses_files,
                   args.reference_source_files, args.reference_target_files, args.hypotheses_lag_files, args.reference_source_json_files):

        hypothesis = load_file_to_list(hypo_file_fp)
        if len(args.remove_tokens_from_hypo) > 0:
            hypothesis = [[x for x in sent if x not in args.remove_tokens_from_hypo] for sent in hypothesis]
        tgt_reference = load_file_to_list(reference_tgt_fp)

        # The reference translation is only used to re-align the system hypothesis
        aligned_hypothesis = resegment(hypothesis=hypothesis, reference=tgt_reference)

        lag_stream = load_file_to_list(lag_file_fp)
        assert len(lag_stream) == 1
        lag_stream = lag_stream[0]

        aligned_lag_stream = transfer_segmentation_to_list(reference_segmentation=aligned_hypothesis, list_to_transform=lag_stream)

        src_reference = load_file_to_list(reference_src_fp)
        assert os.path.splitext(reference_json_file_fp)[1] == ".json"

        actual_words: List[List[str]] = []
        src_timestamps: List[float] = []

        with open(reference_json_file_fp) as jsonf:
            words_and_timestamps = json.load(jsonf)
            for segment in words_and_timestamps:
                segment_words = [word_dict["w"].strip() for word_dict in segment]
                actual_words.append(segment_words)
                src_timestamps.extend([word_dict["e"] for word_dict in segment])

        resegmented_actual_words = resegment(hypothesis=actual_words, reference=src_reference)

        aligned_src_timestamps = transfer_segmentation_to_list(reference_segmentation=resegmented_actual_words, list_to_transform=src_timestamps)

        assert len(aligned_src_timestamps) == len(aligned_lag_stream)

        tls: List[float] = []
        for src_t, tgt_t in zip(aligned_src_timestamps, aligned_lag_stream):
            tls.append(sentence_translation_lag(src_timestamps=src_t, target_lags=tgt_t))

        tl = sum(tls) / len(tls)

        print(f"{os.path.basename(reference_tgt_fp)}\t{tl:.1f}")


if __name__ == "__main__":
    main_cli()