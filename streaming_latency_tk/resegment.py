import argparse
from typing import List

from streaming_latency_tk.levenshtein_alignment import levenshtein_align_hypothesis_to_reference, Segment, Word
from streaming_latency_tk.utils import load_file_to_list


def resegment(hypothesis: List[List[str]], reference: List[List[str]]) -> List[List[str]]:
    """
    Receives the system hypothesis, and resegments it against the reference, using Levenshtein distance
    """
    hypothesis_segments: List[Segment] = []
    reference_segments: List[Segment] = []

    for hip_l in hypothesis:
        words: List[Word] = [Word(string=x) for x in hip_l]
        hypothesis_segments.append(Segment(word_list=words))
    for ref_l in reference:
        words: List[Word] = [Word(string=x) for x in ref_l]
        reference_segments.append(Segment(word_list=words))

    aligned_hypo_segments = levenshtein_align_hypothesis_to_reference(hypothesis=hypothesis_segments,
                                                                      reference=reference_segments)

    aligned_hypo: List[List[str]] = []

    for segment in aligned_hypo_segments:
        words_s = [x.string for x in segment.word_list]
        aligned_hypo.append(words_s)

    return aligned_hypo


def main_cli():
    parser = argparse.ArgumentParser(prog="stream_resegment")

    parser.add_argument("--hypo_file", type=str, required=True,
                        help="File to be resegmented, contains the system hypothesis.")

    parser.add_argument("--reference_file", type=str, required=True,
                        help="Reference file to be used for resegmentation. The output will be segmented into "
                             "the same number of lines as this file.")

    parser.add_argument("--output_file", type=str,
                        help="If set, the resegmented output is stored on this file instead of stdout.")

    args = parser.parse_args()

    hypo_lines = load_file_to_list(args.hypo_file)
    ref_lines = load_file_to_list(args.reference_file)

    reseg_hypo = resegment(hypothesis=hypo_lines, reference=ref_lines)
    out_sentences = [" ".join(sent) + "\n" for sent in reseg_hypo]

    if args.output_file is not None:
        with open(args.output_file, "w") as outf:
            outf.writelines(out_sentences)
    else:
        for line in out_sentences:
            print(line, end="")


if __name__ == "__main__":
    main_cli()

