# README

## Bob Nelkin Collection Extension Layer

<br>

**Author:** Ben Naismith (bnaismith@pitt.edu)  
**Last modified:** July 16, 2021

<br>

This repository contains the extension layer for the [Bob Nelkin Collection of ACC-PARC Records](https://historicpittsburgh.org/collection/nelkin-acc-parc-records) as part of Pitt's [CaD@Pitt](https://cadatpitt.github.io/) (short for Collections as Data at Pitt) project. Extension layers are "scholar-created datasets or outputs that enrich/augment library collections data".

This extension layer contains the following five sections (each in a separate folder) which may be of use to researchers interested in the collection:

1. [Exploratory Data Analysis (EDA)](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/exploratory_data_analysis/): Exploratory data analysis provides a standard first step in any data exploration and corpus analysis. In this case, the EDA looks at the contents of the `source-data` and `base-layers` folders to better understand the quantity and types of data present in the collection.   

<br>

2. [Pre-processing](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/pre-processing/): Pre-processing is carried out to create a single dataframe with the texts and their metadata, with standardized fields and no missing data. The output is a pickle file, `bob_df_pre-processed.pkl`, of the dataframe with 13 columns.  

<br>

3. [Processing](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/processing/): Processing involves manipulating the text into formats which may be of use to researchers and allows for greater analysis. This notebook carries out the following processes: tokenization, part-of-speech tagging, lemmatization, spelling correction, and genre tagging. The output is a pickle file, `bob_df.pkl`, of the dataframe with 21 columns.  

<br>

4. [Text analysis](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/text_analysis/): Text analysis in this case refers to the use machine learning tools to extract information about the texts in terms of entities, topics, and sentiment. All of the text analysis tools use APIs from [meaningcloud.com](meaningcloud.com). This information can be used to filter only those texts related to certain topics or containing certain sentiments. The output is two pickle files, an updated `bob_df.pkl` and `bob_cluster.pkl` which contains a dataframe with informatio about the text clusters in the collection.   

<br>

5. [Lexical analysis](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/lexical_analysis/): The tools and data in this notebook are intended to allow for a greater understanding of the lexis used in the collection's texts through consideration of frequencies of lexical items and the contexts in which they occur. There are two sections to the notebook, _Concordancing_ and _Collocations_ (see the `README.md` file for details).   

<br>

It is suggested that the notebooks in these five folders be run in the order above, especially 1-3. For further information about any of these folders, please see the relevant README files. All code is Python 3.7.6 and presented in Jupyter notebooks.
