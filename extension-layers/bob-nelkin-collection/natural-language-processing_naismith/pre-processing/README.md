# Bob Nelkin Collection of ACC-PARC Records

<br>

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (Email: [bnaismith@pitt.edu](mailto:bnaismith@pitt.edu))  

**Last modified:** July 15, 2021

<br>

### Pre-processing

This folder contains the notebook for the pre-processing stage of the Bob Nelkin Collection. Pre-processing is carried out here to create a single dataframe with the texts and their metadata, with standardized fields and no missing data.  

The notebook contains the following sections:

1. Initial setup
2. Combined dataframe
3. Missing data
4. Standardization
5. Save dataframe   

<br>

#### Output  
The output of this notebook is a pickle file of the pre-processed dataframe which is ready for processing. The dataframe contains the following columns:

column        | description
:---          | :---
id            | unique id for each object, matching the ids found in the source-data and base-layers folders, e.g., _MSS_1002_B001_F11_I01_
title	        | the title assigned to the object by the collection creators, e.g., _Recent Litigation Memo_
display_date  | the data the object was created, using the following format: _July 11, 1975_
abstract	    | short abstracts describing the object, e.g., _Letter from Peter Polloni to Bob Nelkin_. All abstracts provided by the collection creators except for two which were created in this notebook for two missing items
host          | the collection name (same for all objects): _Bob Nelkin Collection of ACC-PARC Records_
series        | the grouping by purpose and date (2 groups total): _I. Administrative Records 1953-1983_ and _II. State School and Hospital (SSH) and Interim Care Committee Records 1972-1997_
container     | the physical location of the object, e.g., _box 1, folder 11, Item 1_
owner         | the collection owner (same for all objects): _Heinz History Center_
depositor     | the depositor of the object (same for all objects): _Detre Library & Archives, Heinz History Center_
collection_id |	internal collection_id number (same for all objects): _collection.341_
text          | the text of the documents (all objects except for 5 photos)
language      | the text language (same for all objects): _English_

<br>

#### Notes
In addition to the elements in the item level of the [CaD@Pitt Archival Collection Metadata Element Set](https://cadatpitt.github.io/documentation/data-dictionary/archival-collections.html#item-level) and data in the [Bob Nelkin Collection base layer](https://github.com/CaDatPitt/data-layers/blob/master/base-layers/bob-nelkin-collection/bob-nelkin-collection_item-base-layer_archival.csv), this extension layer contributes the following element and/or data:
- `abstract` (adds `abstract` data missing in base layer)
- `text`
- `language` (adds `language` data missing in base layer)
