# Bob Nelkin Collection of ACC-PARC Records

<br>

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (Email: [bnaismith@pitt.edu](mailto:bnaismith@pitt.edu))  

**Last modified:** July 16, 2021

<br>

### Text analysis

This folder contains the notebook for the text analysis stage of the Bob Nelkin Collection. Text analysis in this case refers to the use machine learning tools to extract information about the texts in terms of entities, topics, and sentiment. All of the text analysis tools use APIs from [meaningcloud.com](meaningcloud.com). This information can be used to filter only those texts related to certain topics or containing certain sentiments.  

The notebook contains the following sections:  

1. Initial setup
2. Sentiment analysis
3. Topic and entity extraction
4. Cluster analysis
5. Wrap-up

<br>

#### Output  
The output of this notebook is two pickle files: the main [`bob_df`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/processing/README.md#output) dataframe produced in the [`processing`](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/bob-nelkin-collection/natural-language-processing_naismith/processing/) folder but with additional columns, and the `bob_cluster` dataframe. Both dataframes are described below.  

There is also a CSV file and a JSON file, both containing the same information found in the `bob_df` pickle file, in order to provide a range of data formats. However, due to data types and conversion issues, the CSV does not contain the columns with lists of tokenized texts.

<br>

##### bob_df 6 new columns  

column               | description
:---                 | :---
sentiment polarity   | identifies positive (P and P+), negative (N and N+), and neutral (NEU) sentiment for the text
sentiment agreement  | the agreement between the sentiments detected in the text, i.e., whether there is consistent polarity or not. The two possible values are _AGREEMENT_ and _DISAGREEMENT_
sentiment confidence | an integer between 0 and 100 representing the confidence level of the sentiment analysis. A minimum cut off of 80 is used here.
entities             | named entity recognition using meaningcloud's default dictionary. Types of entities include people, organizations, and places
topics               | topic extraction using meaningcloud's default dictionary. Types of topics include concepts, time expressions, money expres

<br>

##### bob_cluster

column       | description
:---         | :---
cluster      | the name of the cluster, e.g., _Interim care Facilities_
cluster freq | the frequency of the cluster, i.e., in how many texts it occurs
score        | the relevance value assigned to the cluster
cluster_loc  | the location of the clusters, i.e., the rows in `bob_df` in which the clusters occur

<br>

#### Notes

This extension layer contributes all new elements and data  in addition to the elements in the item level of the [CaD@Pitt Archival Collection Metadata Element Set](https://cadatpitt.github.io/documentation/data-dictionary/archival-collections.html#item-level) and data in the [Bob Nelkin Collection base layer](https://github.com/CaDatPitt/data-layers/blob/master/base-layers/bob-nelkin-collection/bob-nelkin-collection_item-base-layer_archival.csv).
