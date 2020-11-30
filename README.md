# text-preprocessing
This module contains all my preprocessing functions for text data. 

# Things I would like to include:
1. Tokenising (Using SpaCy)
2. Normalising (Using SpaCy and re)
    1. entities (e.g. names, places, organizations, numbers, etc.)
    2. slang words (e.g. dunno => do not know)
    3. contractions (e.g. don't know => do not know)
    4. capitalization
    5. non ASCII characters
    6. Smilies
3. Stopword removal (Using SpaCy)
4. Punctuation removal (Using SpaCy)
5. Spelling correction (pySymSpell or some kind of dl model)
6. Lemmatization (Using SpaCy)
7. Removal of noise (Using SpaCy)
    1. Extra whitespace
    2. HTML tags
8. POS tagging (Using SpaCy)
9. DEP tagging (Using SpaCy)
10. Removal of specifics such as: (Using SpaCy)
    1. Entities
    2. Dependencies
    3. Part of speech elements

# Other components
1. It needs to be run in parallel so that it can handle a large number of documents at a time. 
