# Stream-level Latency Evaluation for Simultaneous Machine Translation
This repository contains the code of the paper [Stream-level Latency Evaluation for Simultaneous Machine Translation](https://aclanthology.org/2021.findings-emnlp.58/).
Please refer to the publication:
```
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
