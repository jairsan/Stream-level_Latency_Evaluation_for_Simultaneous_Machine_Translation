from typing import List, Union


def load_file_to_list(file_fp: str) -> List[List[str]]:
    processed_words: List[List[str]] = []
    with open(file_fp) as in_file:
        for line in in_file:
            words = line.strip().split()
            processed_words.append(words)
    return processed_words


def transfer_segmentation_to_list(reference_segmentation: List[List[str]], list_to_transform: List[Union[str, float]]):
    """
    Given a reference representation of a segmented text file and a list containing the same number of items, transfer
    the segmentation to the elements of the list, so that it has the same number of segmentes as the provided reference.
    """
    assert sum(len(segment) for segment in reference_segmentation) == len(list_to_transform)
    output_list: List[List[Union[str, float]]] = []

    for segment in reference_segmentation:
        num_items = len(segment)
        generated_segment = list_to_transform[:num_items]
        assert num_items == len(generated_segment)
        output_list.append(generated_segment)
        list_to_transform = list_to_transform[num_items:]

    assert len(list_to_transform) == 0

    return output_list
