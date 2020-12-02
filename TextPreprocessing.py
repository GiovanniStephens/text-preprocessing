import spacy
import re
from unidecode import unidecode
import functools
from toolz import compose

#Package discovery and resource access: https://setuptools.readthedocs.io/en/latest/pkg_resources.html
import pkg_resources

# Spell checking
from symspellpy import SymSpell, Verbosity 
sym_spell = SymSpell()

def load_sym_spell_dict():
    """
    This function loads the dictionary for the spell-corrector. 
    max edit distance is 2.
    """
    dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, 0, 1)

def correct_spelling(text):
    """
    This function attempts to correct the spelling of a string using Symspell.
    """
    return sym_spell.lookup_compound(text, max_edit_distance=2, transfer_casing=True, ignore_non_words=True)[0].term

def remove_html_tags(utterance):
    """
    Remove html tags from a string
    
    :utterance: string that we would like to clean.
    :return: cleanned string
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', utterance)

def remove_excess_whitespace(utterance):
    """
    Remove excess whitespace from string.

    :utterance: string that we would like to clean.
    :return: cleanned string
    """
    return " ".join(utterance.split())

def convert_non_ascii(utterance):
    """
    Try to convert non-ASCII characters to something readable in
    English.

    :utterance: string that we would like to clean.
    :return: cleanned string
    """
    return unidecode(utterance)

def remove_stop_words(utterance):
    """
    Removes stop words from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :return: list of SpaCy tokens minus stop words
    """
    return [token for token in utterance if not token.is_stop]

def remove_punctuation(utterance):
    """
    Removes punctuation from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :return: list of SpaCy tokens minus punctuation
    """
    return [token for token in utterance if not token.is_punct]

def remove_entity(utterance, entity):
    """
    Removes specific entities from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :entity: the entity name you want to remove (see this list for examples:
    https://spacy.io/api/annotation#named-entities)
    :return: list of SpaCy tokens minus the entities
    """
    return [token for token in utterance if token.ent_type_ != entity]

def remove_dependency(utterance, dep):
    """
    Removes specific semantic dependency from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :dep: the dependency name you want to remove (see this list for examples:
    https://spacy.io/usage/linguistic-features#pos-tagging)
    :return: list of SpaCy tokens minus the dependency
    """
    return [token for token in utterance if token.dep_ != dep]

def remove_pos(utterance, pos):
    """
    Removes specific part of speech from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :pos: the part of speech you want to remove (see this list for examples:
    https://spacy.io/usage/linguistic-features#pos-tagging)
    :return: list of SpaCy tokens minus the dependency
    """
    return [token for token in utterance if token.pos_ != pos]

class TextPreprocessing():

    def __init__(self, utterances, pipes = ['entity_ruler', 'sentencizer']) -> None:
        self.raw_utterances = utterances
        # Load SpaCy model
        self.nlp = spacy.load('en_core_web_sm')
        # Load SpaCy pipeline 
        if pipes != None:
            self.load_nlp_pipe(pipes)
        # Process utterances (i.e. tokenising, tagging, etc.)
        self.nlp_utterances = list(self.nlp.pipe(utterances))

    # Load NLP pipeline
    def load_nlp_pipe(self, pipes):
        """
        This function creates and loads all the pipes into the nlp-er

        :pipes: list of pipe names as strings
        """

        for pipe in pipes:
            nlp_pipe = self.nlp.create_pipe(pipe)
            if pipe == 'sentencizer': #needs to go before the parser. 
                self.nlp.add_pipe(nlp_pipe, before='parser')
            else:
                self.nlp.add_pipe(nlp_pipe)

    def preprocess_text(self, fns=[remove_stop_words, remove_punctuation]):
        nlp_pipeline = compose(*fns)
        self.cleaned_utterances = list(map(nlp_pipeline,self.nlp_utterances))
