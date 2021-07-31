# Bob Nelkin Collection of ACC-PARC Records

<br>

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (Email: [bnaismith@pitt.edu](mailto:bnaismith@pitt.edu))

**Last modified:** July 31, 2021

<br>

This directory contains three folders for a natural language processing extension layer for the [Bob Nelkin Collection of Allegheny County Chapter of the Pennsylvania Association for Retarded Children (ACC-PARC) Records](https://historicpittsburgh.org/collection/nelkin-acc-parc-records) as part of Pitt's [CaD@Pitt](https://cadatpitt.github.io/) (short for Collections as Data at Pitt) project. Extension layers are "scholar-created datasets or outputs that enrich/augment library collections data".

The content of the three folders are as follows:

1. [`natural-language-processing_naismith`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/): The primary folder containing all of the code and output for the various elements of the extension layer (see the [`README.md`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/README.md) file in the folder for details).

2. [`CLAWS-tagged_naismith`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/CLAWS-tagged_naismith/): A folder containing each of the text files from the collection after tokenization and part-of-speech tagging using the CLAWS7 tagset (see the [`bob-nelkin-collection_processing.ipynb`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/processing/bob-nelkin-collection_processing.ipynb) notebook for details.)

3. [`ocr_naismith`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/ocr_naismith/): A folder containing text files for each of the texts in the collection. The original source data ocr folder contained a number of blank files, so all pdf files were converted to text files again using the [Optical Character Recognition (OCR) workstation](https://www.library.pitt.edu/digital-scholarship-commons) at Pitt, which uses ABBYY FineReader to convert images to text. These new text files are used throughout this extension layer.
