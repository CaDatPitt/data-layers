# Bob Nelkin Collection of ACC-PARC Records

<br>

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (Email: [bnaismith@pitt.edu](mailto:bnaismith@pitt.edu))

**Last modified:** July 31, 2021

<br>

This directory contains a natural language processing extension layer for the [Bob Nelkin Collection of Allegheny County Chapter of the Pennsylvania Association for Retarded Children (ACC-PARC) Records](https://historicpittsburgh.org/collection/nelkin-acc-parc-records) as part of Pitt's [CaD@Pitt](https://cadatpitt.github.io/) (short for Collections as Data at Pitt) project. Extension layers are "scholar-created datasets or outputs that enrich/augment library collections data".

The natural language processing folder contains the following five sections (each in a separate folder) which may be of use to researchers interested in the collection:

1. [Exploratory Data Analysis (EDA)](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/exploratory-data-analysis/): Exploratory data analysis provides a standard first step in any data exploration and corpus analysis. In this case, the EDA looks at the contents of the [`source-data`](https://github.com/CaDatPitt/data-layers/tree/master/source-data/bob-nelkin-collection) and [`base-layers`](https://github.com/CaDatPitt/data-layers/tree/master/base-layers/bob-nelkin-collection) folders to better understand the quantity and types of data present in the collection.   

2. [Pre-processing](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/pre-processing/): Pre-processing is carried out to create a single dataframe with the texts and their metadata, with standardized fields and no missing data. The output is a pickle file, [`bob_df_pre-processed.pkl`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/pre-processing/bob_df_pre-processed.pkl), of the dataframe with 13 columns.  

3. [Processing](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/processing/): Processing involves manipulating the text into formats which may be of use to researchers and allows for greater analysis. This notebook carries out the following processes: tokenization, part-of-speech tagging, lemmatization, spelling correction, and genre tagging. The output is a pickle file, [`bob_df.pkl`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/processing/bob_df.pkl), of the dataframe with 21 columns.  

4. [Text analysis](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/text_analysis/): Text analysis in this case refers to the use machine learning tools to extract information about the texts in terms of entities, topics, and sentiment. All of the text analysis tools use APIs from [meaningcloud.com](meaningcloud.com). This information can be used to filter only those texts related to certain topics or containing certain sentiments. The output includes two pickle files, an updated [`bob_df.pkl`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/text_analysis/bob_df.pkl) and [`bob_cluster.pkl`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/text_analysis/bob_cluster.pkl), the latter of which contains a dataframe with information about the text clusters in the collection. There is also a CSV file and a JSON file, both containing the same information found in the `bob_df` pickle file, in order to provide a range of data formats. However, due to data types and conversion issues, the CSV does not contain the columns with lists of tokenized texts.  

5. [Lexical analysis](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/lexical_analysis/): The tools and data in this notebook are intended to allow for a greater understanding of the lexis used in the collection's texts through consideration of frequencies of lexical items and the contexts in which they occur. There are two sections to the notebook, _Concordancing_ and _Collocations_ (see the [`README.md`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/lexical_analysis/README.md) file for details).   

<br>

#### Notes

1. It is suggested that the notebooks in these five folders be run in the order above, especially 1-3. For further information about any of these folders, please see the relevant README files. All code is Python 3.7.6 and presented in Jupyter notebooks.  

2. The final full dataframe with all of the combined data can be found in the [`text-analysis`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/text_analysis/) folder.
