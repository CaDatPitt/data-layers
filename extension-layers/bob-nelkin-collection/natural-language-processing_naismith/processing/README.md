# Bob Nelkin Collection of ACC-PARC Records

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (Email: [bnaismith@pitt.edu](mailto:bnaismith@pitt.edu))

**Last modified:** July 15, 2021

<br>

### Processing

This folder contains the notebook for the processing stage of the Bob Nelkin Collection. Processing involves manipulating the text into formats which may be of use to researchers and allows for greater analysis.  

The notebook contains the following sections:

1. Initial setup
2. Text cleaning
3. Tokenization
4. POS tagging and lemmatization
5. Spelling correction
6. Genre tagging
7. Wrap-up

#### Output

The output of this notebook is a pickle file of the processed dataframe called [`bob_df.pkl`](https://github.com/CaDatPitt/data-layers/blob/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/processing/bob_df.pkl). The dataframe contains the following columns:

column                     | description
:---                       | :---
id                         | unique id for each object, matching the ids found in the source-data and base-layers folders, e.g., _MSS_1002_B001_F11_I01_
title	                     | the title assigned to the object by the collection creators, e.g., _Recent Litigation Memo_
display_date               | the data the object was created, using the following format: _July 11, 1975_
abstract	                 | short abstracts describing the object, e.g., _Letter from Peter Polloni to Bob Nelkin_. All abstracts provided by the collection creators except for two which were created in this notebook for two missing items
host                       | the collection name (same for all objects): _Bob Nelkin Collection of ACC-PARC Records_
series                     | the grouping by purpose and date (2 groups total): _I. Administrative Records 1953-1983_ and _II. State School and Hospital (SSH) and Interim Care Committee Records 1972-1997_
container                  | the physical location of the object, e.g., _box 1, folder 11, Item 1_
owner                      | the collection owner (same for all objects): _Heinz History Center_
depositor                  | the depositor of the object (same for all objects): _Detre Library & Archives, Heinz History Center_
collection_id              | internal collection_id number (same for all objects): _collection.341_
text                       | the text of the documents (all objects except for 5 photos)
language                   | the text language (same for all objects): _English_
len                        | the length of the text (number of words), calculated using regex-based tokenization
tok_lem_POS_NLTK           | three-part tuples for word in the text consisting of the original word, the lemmatized form of the word (no inflections), and the part-of-speech. NLTK tools are used which employs the [Penn Treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
tok_lem_POS_CLAWS          | same as above but using the [CLAWS7 tagset](http://ucrel.lancs.ac.uk/claws7tags.html)
tok_lem_POS_NLTK_corrected | a spell-corrected version of the the `tok_lem_POS_NLTK` column using the [SymSpell](https://pypi.org/project/symspellpy/) library
misspelling_correction     | the words which were corrected in the spell-corrected version to allow for manual verification if desired
len_errors                 | the number of misspelled words based on the previous column
genre                      | the genre of the text as deduced from the title and abstract of the text
genre_MODS                 | the genre of the text coverted to the comply with the [genre terms list for University of Pittsburgh Library System (ULS) digital collections](https://github.com/uls-mad/islandora_metadata/wiki/Genre-Terms-for-Historic-Pittsburgh-Digital-Objects)
resource_type              | the resource type based on the previous column (either _text_ or _still image_)

<br>

#### Notes  

In addition to the elements in the item level of the [CaD@Pitt Archival Collection Metadata Element Set](https://cadatpitt.github.io/documentation/data-dictionary/archival-collections.html#item-level) and data in the [Bob Nelkin Collection base layer](https://github.com/CaDatPitt/data-layers/blob/master/base-layers/bob-nelkin-collection/bob-nelkin-collection_item-base-layer_archival.csv), this extension layer contributes the following elements and/or data:
- `text`
- `len`
- `tok_lem_POS_NLTK`
- `tok_lem_POS_CLAWS`
- `tok_lem_POS_NLTK_corrected`
- `misspelling_correction`
- `len_errors`
- `genre` (adds `genre` data missing in base layer)
- `genre_MODS` (adds `genre` data missing in base layer)
- `resource_type` (adds `type_of_resource` data missing in base layer)

As part of the processing, frequency data from an external corpus, [COCA](https://www.english-corpora.org/coca/) (Davies, 2008-), is used. This data was accessed through a paid license. Please contact [Dr. Na-Rae Han](https://www.linguistics.pitt.edu/people/na-rae-han) for access information for Pitt students and faculty or the [COCA website](https://www.wordfrequency.info/purchase.asp) for purchase information.  

Davies, Mark. (2008-) _The Corpus of Contemporary American English (COCA)_. Available online at https://www.english-corpora.org/coca/.
