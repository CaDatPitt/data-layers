# README

## Bob Nelkin Collection Extension Layer - Text analysis

<br>

**Author:** Ben Naismith (bnaismith@pitt.edu)  
**Last modified:** July 16, 2021

<br>

This folder contains the notebook for the text analysis stage of the Bob Nelkin Collection. Text analysis in this case refers to the use machine learning tools to extract information about the texts in terms of entities, topics, and sentiment. All of the text analysis tools use APIs from [meaningcloud.com](meaningcloud.com). This information can be used to filter only those texts related to certain topics or containing certain sentiments.  

The notebook contains the following sections:  

1. Initial setup
2. Sentiment analysis
3. Topic and entity extraction
4. Cluster analysis
5. Wrap-up

<br>

**Output:**  
The output of this notebook is two pickle files: the main `bob_df` dataframe produced in the _processing_ folder but with additional columns, and the `bob_cluster` dataframe.  

**bob_df 6 new columns:**   

column               | description
:---                 | :---
sentiment polarity   | identifies positive (P and P+), negative (N and N+), and neutral (NEU) sentiment for the text
sentiment agreement  | the agreement between the sentiments detected in the text, i.e., whether there is consistent polarity or not. The two possible values are _AGREEMENT_ and _DISAGREEMENT_
sentiment confidence | an integer between 0 and 100 representing the confidence level of the sentiment analysis. A minimum cut off of 80 is used here.
entities             | named entity recognition using meaningcloud's default dictionary. Types of entities include people, organizations, and places
topics               | topic extraction using meaningcloud's default dictionary. Types of topics include concepts, time expressions, money expres

<br>

**bob_cluster:**

column       | description
:---         | :---
cluster      | the name of the cluster, e.g., _Interim care Facilities_
cluster freq | the frequency of the cluster, i.e., in how many texts it occurs
score        | the relevance value assigned to the cluster
cluster_loc  | the location of the clusters, i.e., the rows in `bob_df` in which the clusters occur
