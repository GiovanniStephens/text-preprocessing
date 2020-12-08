# text-preprocessing
This module contains all my preprocessing functions for text data.  

The idea behind this is to make it easy to, from a high level, preprocess lots of text with an easy call to a high-level function that does everything for you. It needs to be flexible enough so that you can change what preprocessing you do while not having to rewrite code all the time. 

# Things I would like to include:
- [x] Tokenising (Using SpaCy)
- [ ] Normalising (Using SpaCy and re)
    - [x] chosen entities (e.g. names, places, organizations, numbers, dates, etc.)
    - [x] contractions (e.g. don't know => do not know) (contractions library)
    - <s>[ ] capitalization (lower function)</s> (This can be done in post at any point.)
    - [x] non ASCII characters
    - [x] Smilies 
    - [ ] slang words (e.g. dunno => do not know)
    - <s>[ ] word numerals to numbers (e.g. twenty three => 23)</s> (will use entity tagging to normalise this)
    - <s>[ ] date formats (normalise library.</s> Probably just replacing with a normalised version using SpaCy.)
    - [ ] Acronyms (e.g. US => United States, btw => by the way) 
    - <s>[ ] Substitution of rare words with closely related synonyms.(normalise library)</s> (likely a bigger problem to solve with word-sense-diambiguation.)
    - <s>[ ] Substitution of rare words with closely related synonyms.</s>
- [x] Stopword removal (Using SpaCy)
- [x] Punctuation removal (Using SpaCy)
- [x] Spelling correction (pySymSpell or some kind of dl model)
- [x] Lemmatization (Using SpaCy)
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

# To-do
- [x] Refactor tests to account for the refactoring of the preprocessing functions. 
- [x] Test the norm functions
- [ ] Create a high-level function to perform all the cleaning with default values.
- [ ] More testing
