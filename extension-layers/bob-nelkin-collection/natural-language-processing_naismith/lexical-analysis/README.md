# Bob Nelkin Collection of ACC-PARC Records

## Natural Language Processing Layer – Naismith

**Creator:** Ben Naismith (bnaismith@pitt.edu)  

**Last modified:** July 16, 2021

<br>

### Lexical analysis

This folder contains the notebook for the lexical analysis options with the Bob Nelkin Collection. These tools and data are intended to allow for a greater understanding of the lexis used in the collection's texts through consideration of frequencies of lexical items and the contexts in which they occur.

The notebook contains the following sections:

1. Initial setup
2. Concordancing
3. Collocations  

There are two main sections to the notebook, _Concordancing_ and _Collocations_:  

#### Concordancing

The following description of concordancing and the [`conc.py`](https://github.com/ELI-Data-Mining-Group/pelitk/blob/master/pelitk/conc.py) tool come from the [PELITK: Pitt English Language Institute ToolKit README file](https://github.com/ELI-Data-Mining-Group/pelitk):

Essentially, a concordance is a list of words or phrases from a text, presented with their immediate contexts. Concordancing has long been an integral part of corpus investigations; as John Sinclair describes,  

_"The normal starting point for a corpus investigation is the concordance, which from early days in computing has used the [Key Word In Context (KWIC)] format, where instances of a chosen word or phrase (the NODE) are presented in a layout that aligns occurrences of the node vertically, but otherwise keeps them in the order in which they appear in the corpus."_  

Sinclair (2003, xiii)  

[`conc.py`](https://github.com/ELI-Data-Mining-Group/pelitk/blob/master/pelitk/conc.py) creates a concordance list based on key words in a text, and it has options to allow for greater user flexibility. In the example usage below, there is a short text of two sentences which has been tokenized (split into a list of strings) to analyze the key word _platypus_. The output (presented in two formats) demonstrates how concordance lines provide a useful format for quickly seeing how a word (or phrase) is used in different contexts.


```python
>>> from pelitk import conc
>>> tok_text = ['The', 'key', 'word', 'in', 'this', 'text', 'is', 'the', 'noun', 'platypus', '.',
               'I', 'want', 'to', 'see', 'the', 'context', 'every', 'time', 'the', 'word', 'platypus', 'occurs', '.']

>>> print(conc.concordance(tok_text,'platypus',5))
[('this text is the noun', 'platypus', '. I want to see'),
('context every time the word', 'platypus', 'occurs .   ')]

>>> print(conc.concordance(tok_text,'platypus',5,pretty=True))
['                   this text is the noun   platypus   . I want to see                         ',
 '              context every time the word   platypus   occurs .                                ']
```

For more example code and a full description of the functions (including their arguments and sub-functions), see [`CONC.md`](https://github.com/ELI-Data-Mining-Group/pelitk/blob/master/docs/CONC.md) and [`conc.py`](https://github.com/ELI-Data-Mining-Group/pelitk/blob/master/pelitk/conc.py).

#### Collocations

Collocations are groups of 2-3 words that commonly occur together and are semantically linked in some way. For example, _Happy birthday_ is a collocation, but _Merry birthday_ is not. It can be useful to extract collocations of order to see lexical 'chunks' and not only single words.  

There are many approaches to defining and identifying collocations, related to form and meaning. Here, collocations are identified based on _Mutual Information (MI)_, a measure that describes collocational strength based on co-occurrence between words.

<br>

#### Notes

As part of the processing, frequency data from an external corpus, [COCA](https://www.english-corpora.org/coca/) (Davies, 2008-), is used. This data was accessed through a paid license. Please see [Dr Na-Rae Han](https://www.linguistics.pitt.edu/people/na-rae-han) for access information for Pitt students and faculty or the [COCA website](https://www.wordfrequency.info/purchase.asp) for purchase information.  

Davies, Mark. (2008-) _The Corpus of Contemporary American English (COCA)_. Available online at https://www.english-corpora.org/coca/.
