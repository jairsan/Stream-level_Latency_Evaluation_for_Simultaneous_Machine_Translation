from typing import List


def load_file_to_list(file_fp: str) -> List[List[str]]:
    processed_words: List[List[str]] = []
    with open(file_fp) as in_file:
        for line in in_file:
            words = line.strip().split()
            processed_words.append(words)
    return processed_words
