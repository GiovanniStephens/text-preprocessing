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
4. Splitting contractions (e.g. don't know => do not know) (contractions library) 
5. converting smilies (emoticons and emojis) to text.
6. Spelling correction (pySymSpell)
7. Lemmatization (Using SpaCy)

## Filtering
1. Stopword removal (Using SpaCy)
2. Punctuation removal (Using SpaCy)
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
```

# Basic Usage

```python
>>> import TextPreprocessing as tp
>>> processor = tp.TextPreprocessing(texts)
>>> processor.preprocess()
>>> cleaned_texts = processor.nlp_utterances
```