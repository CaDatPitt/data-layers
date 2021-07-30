# Bob Nelkin Collection of ACC-PARC Records

<br>

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (Email: [bnaismith@pitt.edu](mailto:bnaismith@pitt.edu))

**Last modified:** July 15, 2021

<br>

### Exploratory Data Analysis

This folder contains the notebook for the Exploratory Data Analysis (EDA) of the Bob Nelkin Collection. Exploratory data analysis provides a standard first step in any data exploration and corpus analysis. In this case, the EDA looks at the contents of the [`source-data`](https://github.com/CaDatPitt/data-layers/tree/bnaismith/source-data/bob-nelkin-collection/) and [`base-layers`](https://github.com/CaDatPitt/data-layers/tree/bnaismith/base-layers/bob-nelkin-collection) folders to better understand the quantity and types of data for the collection.

The notebook contains the following sections:

1. Initial setup
2. `source-data` folder
    - `ead` folder
    - `mods` folder
    - `ocr` folder
    - `rel-ext` folder
    - `source-data` summary
3. `base-layers` folder

There are two main sections to the notebook, _`source-data` folder_ and _`base-layers` folder_.  

<br>

#### `source-data` folder

- `ead` folder: contains one large xml file with extensive metadata about the collection
- `ocr` folder: contains 537 text files. The quality of OCR appears to be variable, leading to spelling issues.
- `mods` and `rel-ext` folders: contain 542 .xml files with metadata which correspond to the OCR text files, plus one for the 'Finding aid content model'. These figures are in line with the [collection description](https://historicpittsburgh.org/collection/nelkin-acc-parc-records).

<br>

#### `base-layers` folder
- `collection-base-layer.csv` contains information the guide to the collection
- `base-layer_archival.csv` contains information about the objects in the collection (1 per row). There is one object missing an abstract.
