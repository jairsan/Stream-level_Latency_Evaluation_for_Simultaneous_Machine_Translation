# Stream-level Latency Evaluation for Simultaneous Machine Translation
This repository contains the code of the paper [Stream-level Latency Evaluation for Simultaneous Machine Translation](https://aclanthology.org/2021.findings-emnlp.58/).

## Installation
```shell
git clone https://github.com/jairsan/Stream-level_Latency_Evaluation_for_Simultaneous_Machine_Translation.git
pip install .
```

## Usage 
```
stream_latency [-h] --hypotheses_files HYPOTHESIS_FILE [HYPOTHESIS_FILE ...] 
                          --hypotheses_RW_files RW_FILE [RW_FILE ...] 
                          --reference_source_files SRC_REFERENCE_FILE [SRC_REFERENCE_FILE ...]
                          --reference_target_files TGT_REFERENCE_FILE [TGT_REFERENCE_FILE ...]
                          [--penalty_scale_factor PENALTY_SCALE_FACTOR]
                          [--remove_tokens_from_hypo TOKEN [TOKEN ...]] 
                          [--read_action_repr READ_ACTION_REPR] 
                          [--write_action_repr WRITE_ACTION_REPR]
                          [--output_format {tabs,table,json}]
```
The software uses 4 mandatory arguments: ```--hypotheses_files  --hypotheses_RW_files --reference_source_files --reference_target_files```.
Internally, latency is computed for each stream, with a stream being defined as a tuple composed of ```(HYPOTHESIS_FILE, RW_FILE, SRC_REFERENCE_FILE, TGT_REFERENCE_FILE)```. Words are assumed to be
whitespace delimited in all files. 

* ```HYPOTHESIS_FILE```: The translation produced by the streaming system. 
* ```RW_FILE```: The sequence of READ/WRITE operations (whitespace delimited) performed by the streaming system. The number of actions should be equal to the number of words in the ``HYPOTHESIS_FILE``. By default, each read action is represented by "R", each write action by "W".
* ```SRC_REFERENCE_FILE```: Reference source file, split into lines. Necessary for computing the latency.
* ```TGT_REFERENCE_FILE```: Reference target file, split into lines. This file is used to re-segment the streaming system's hypothesis.

### Example
Reproducing the results of the EMNLP2021 paper, Figure 2, k=5:
```
loc=emnlp2021/REPRODUCIBLE/REAL
k=5
stream_latency --hypotheses_files $loc/$k.orig_h --hypotheses_RW_files $loc/$k.RW \
                      --reference_source_files emnlp2021/REPRODUCIBLE/norm.iwslt17.dev2010.de \
                      --reference_target_files emnlp2021/iwslt17.dev2010.prepro.en \
                      --penalty_scale_factor 0.95 \
                      --output_format table
```

The output should look like this:
```
File                                        AP    AP    AL
iwslt17.dev2010.prepro.en                  0.8   4.4   5.8
```

## Original implementation
Originally, the experiments we conducted
for the EMNLP 2021 Findings paper used [MWER](https://aclanthology.org/2005.iwslt-1.19/) for resegmenting the system hypothesis.
In order to avoid the dependency on the MWER C binary (as well as some edge cases where the tool crashed), we
have updated the code to use the Levenshtein distance realignment of the [SubER](https://github.com/apptek/SubER.git)
package. The code has also been updated into a proper software package.


Note that both versions of this software are "proper" implementations of the techniques described in the paper,
as the only difference between them is some minor details on the Levensthen distance re-alignment. 
This new implementation obtains the same results with very small differences (+- 0.1), but is much easier to use, and
therefore I reccommend you use this updated version.

Nevertheless, a snapshot of the original code at the time of publication is stored in the branch "emnlp2021", as well
as in the "emnlp2021" folder.

## Standalone resegmentation
Using the aforementioned SubER resegmentation, you can run just the resegmentation procedure by calling the wrapper ```stream_resegment``` command.

```
stream_resegment [-h] --hypo_file HYPO_FILE --reference_file REFERENCE_FILE [--output_file OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --hypo_file HYPO_FILE
                        File to be resegmented, contains the system hypothesis.
  --reference_file REFERENCE_FILE
                        Reference file to be used for resegmentation. The output will be segmented into the same number of lines as this file.
  --output_file OUTPUT_FILE
                        If set, the resegmented output is stored on this file instead of stdout.
```

The typical use case for this wrapper is to re-segment the system hypothesis for running quality evaluation. Thus, you would
run resegmentation on the hypothesis before using you software of choice, such as sacrebleu, to compare against the reference. This way,
both latency and quality evaluation are carried out on the same resegmentation.


## Citation
```bibtex
@inproceedings{iranzo-sanchez-etal-2021-stream-level,
    title = "Stream-level Latency Evaluation for Simultaneous Machine Translation",
    author = "Iranzo-S{\'a}nchez, Javier  and
      Civera Saiz, Jorge  and
      Juan, Alfons",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2021",
    month = nov,
    year = "2021",
    address = "Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.findings-emnlp.58",
    pages = "664--670",
    abstract = "Simultaneous machine translation has recently gained traction thanks to significant quality improvements and the advent of streaming applications. Simultaneous translation systems need to find a trade-off between translation quality and response time, and with this purpose multiple latency measures have been proposed. However, latency evaluations for simultaneous translation are estimated at the sentence level, not taking into account the sequential nature of a streaming scenario. Indeed, these sentence-level latency measures are not well suited for continuous stream translation, resulting in figures that are not coherent with the simultaneous translation policy of the system being assessed. This work proposes a stream level adaptation of the current latency measures based on a re-segmentation approach applied to the output translation, that is successfully evaluated on streaming conditions for a reference IWSLT task.",
}
```

Please also cite [SubER](https://github.com/apptek/SubER.git) when appropriate.