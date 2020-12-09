# text-preprocessing
This module contains all my preprocessing functions for text data.  

The idea behind this is to make it easy to preprocess lots of text with an easy call to a high-level function that does everything for you. It is also flexible enough so that you can change what preprocessing you do while not having to rewrite code all the time. 

# Functionality:

## Text Cleaning:

1. Removal of extra whitespace
2. Removal of HTML tags
3. Transliterating non ASCII characters to ASCII characters.

## Text Normalisation:

1. Normalising chosen entities (e.g. names, places, organizations, numbers, dates, etc.)
2. Normalising chosen part of speech (POS) (e.g. 'NOUN', 'VERB', etc)
3. Normalising chosen semantic dependencies (DEP) (e.g. 'nsubj', 'ROOT')
4. Splitting contractions (e.g. don't know => do not know) ([contractions](https://pypi.org/project/contractions/) library) 
5. converting smilies (emoticons and emojis) to text.
6. Spelling correction (using [symspellpy](https://pypi.org/project/symspellpy/))
7. Lemmatization (Using [SpaCy](https://spacy.io/))

## Filtering
1. Stopword removal (Using [SpaCy](https://spacy.io/))
2. Punctuation removal (Using [SpaCy](https://spacy.io/))
3. Entity removal
4. POS removal
5. DEP removal

## Preprocessing Pipeline 

Removal of noise --> Basic Normalisation --> Spelling correction --> NLP with SpaCy --> Filtering --> Advanced Normalisation (ENT normalisation and lemmatisation).

# Installation

First, clone the repository. 

In your terminal, run:  
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Notes:
Installs the dependencies and the [language model](https://spacy.io/usage/models) the [SpaCy](https://spacy.io/) uses. 

# Basic Usage

```python
>>> import TextPreprocessing as tp
>>> processor = tp.TextPreprocessing(texts)
>>> processor.preprocess()
>>> cleaned_texts = processor.nlp_utterances
```

# Resources
- [SpaCy entities that can be normalised.](https://spacy.io/api/annotation#named-entities)
- [SpaCy semantic dependencies (DEP) types](https://spacy.io/usage/linguistic-features)
- [SpaCy part of speech (POS) types](https://spacy.io/usage/linguistic-features) 


# Dependencies 
1. [emot==2.1](https://pypi.org/project/emot/)
2. [Unidecode==1.1.1](https://pypi.org/project/Unidecode/)
3. [symspellpy==6.5.2](https://pypi.org/project/symspellpy/)
4. [spacy==2.3.0](https://spacy.io/)
5. [contractions==0.0.23](https://pypi.org/project/contractions/)
6. [toolz==0.10.0](https://pypi.org/project/toolz/)

# Contact

stephens.giovanni@gmail.com