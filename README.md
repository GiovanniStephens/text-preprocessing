# text-preprocessing
This module contains all my preprocessing functions for text data.  

The idea behind this is to make it easy to, from a high level, preprocess lots of text with an easy call to a high-level function that does everything for you. It needs to be flexible enough so that you can change what preprocessing you do while not having to rewrite code all the time. 

# Things I would like to include:
- [x] Tokenising (Using SpaCy)
- [ ] Normalising (Using SpaCy and re)
    - [ ] chosen entities (e.g. names, places, organizations, numbers, etc.)
    - [ ] slang words (e.g. dunno => do not know)
    - [ ] contractions (e.g. don't know => do not know) (contractions library)
    - [ ] capitalization (lower function)
    - <s>[ ] word numerals to numbers (e.g. twenty three => 23)</s> (will use entity tagging to normalise this)
    - [ ] date formats (normalise library)
    - [ ] Acronyms (e.g. US => United States, btw => by the way) (normalise library)
    - [ ] Substitution of rare words with closely related synonyms.
    - [x] non ASCII characters
    - [ ] Smilies 
- [x] Stopword removal (Using SpaCy)
- [x] Punctuation removal (Using SpaCy)
- [x] Spelling correction (pySymSpell or some kind of dl model)
- [ ] Lemmatization (Using SpaCy)
- [x] Removal of noise (Using SpaCy)
    - [x] Extra whitespace
    - [x] HTML tags
- [x] POS tagging (Using SpaCy)
- [x] DEP tagging (Using SpaCy)
- [x] Removal of specifics such as: (Using SpaCy)
    - [x] Entities
    - [x] Dependencies
    - [x] Part of speech elements

# Other components
1. It needs to be run in parallel so that it can handle a large number of documents at a time.  

pipeline would be:  
Removal of noise with re --> Normalization --> Spelling correction --> NLP with SpaCy --> all SpaCy cleaning functions.
