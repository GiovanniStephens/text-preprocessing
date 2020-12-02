# text-preprocessing
This module contains all my preprocessing functions for text data. 

# Things I would like to include:
1. Tokenising (Using SpaCy) (done)
2. Normalising (Using SpaCy and re)
    1. entities (e.g. names, places, organizations, numbers, etc.)
    2. slang words (e.g. dunno => do not know)
    3. contractions (e.g. don't know => do not know)
    4. capitalization
    5. non ASCII characters
    6. Smilies
3. Stopword removal (Using SpaCy) (done)
4. Punctuation removal (Using SpaCy) (done)
5. Spelling correction (pySymSpell or some kind of dl model)
6. Lemmatization (Using SpaCy)
7. Removal of noise (Using SpaCy)
    1. Extra whitespace
    2. HTML tags
8. POS tagging (Using SpaCy) (done)
9. DEP tagging (Using SpaCy) (done)
10. Removal of specifics such as: (Using SpaCy) (done)
    1. Entities (done)
    2. Dependencies (done)
    3. Part of speech elements (done)

# Other components
1. It needs to be run in parallel so that it can handle a large number of documents at a time.  

pipeline would be:  
Removal of noise with re --> Spelling correction --> NLP with SpaCy --> all SpaCy cleaning functions.
