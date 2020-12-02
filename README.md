# text-preprocessing
This module contains all my preprocessing functions for text data.  

The idea behind this is to make it easy to, from a high level, preprocess lots of text with an easy call to a high-level function that does everything for you. It needs to be flexible enough so that you can change what preprocessing you do while not having to rewrite code all the time. 

# Things I would like to include:
- [x] Tokenising (Using SpaCy)
- Normalising (Using SpaCy and re)
    - entities (e.g. names, places, organizations, numbers, etc.)
    - slang words (e.g. dunno => do not know)
    - contractions (e.g. don't know => do not know)
    - capitalization
    - non ASCII characters (done)
    - Smilies
- Stopword removal (Using SpaCy) (done)
- Punctuation removal (Using SpaCy) (done)
- Spelling correction (pySymSpell or some kind of dl model) (done)
- Lemmatization (Using SpaCy)
- Removal of noise (Using SpaCy) (done)
    - Extra whitespace (done)
    - HTML tags (done)
- POS tagging (Using SpaCy) (done)
- DEP tagging (Using SpaCy) (done)
- Removal of specifics such as: (Using SpaCy) (done)
    - Entities (done)
    - Dependencies (done)
    - Part of speech elements (done)

# Other components
1. It needs to be run in parallel so that it can handle a large number of documents at a time.  

pipeline would be:  
Removal of noise with re --> Spelling correction --> NLP with SpaCy --> all SpaCy cleaning functions.
