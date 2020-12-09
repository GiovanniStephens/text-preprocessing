import spacy
import re
from emot.emo_unicode import EMOTICONS, UNICODE_EMO
from unidecode import unidecode
import functools
from toolz import compose
import contractions

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
    return [token for token in utterance if (token.is_alpha or token.is_digit)]

def remove_entity(utterance, entities):
    """
    Removes specific entities from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :entities: the list of entity names you want to remove 
    (see this list for examples: https://spacy.io/api/annotation#named-entities)
    :return: list of SpaCy tokens minus the entities
    """
    return [token for token in utterance if token.ent_type_ not in entities]

def norm_entity(utterance, entities):
    norm_tokens = []
    for token in utterance:
        if not isinstance(token, str) and token.ent_type_ in entities:
            norm_tokens.append(token.ent_type_)
        else:
            norm_tokens.append(token)
    return norm_tokens

def lemmatise(utterance):
    return [token.lemma_ if isinstance(token, spacy.tokens.token.Token) \
        else token for token in utterance]

def remove_dependency(utterance, dep):
    """
    Removes specific semantic dependency from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :dep: the list of dependency name you want to remove 
    (see this list for examples: https://spacy.io/usage/linguistic-features#pos-tagging)
    :return: list of SpaCy tokens minus the dependency
    """
    return [token for token in utterance if token.dep_ not in dep]

def remove_pos(utterance, pos):
    """
    Removes specific part of speech from the input SpaCy nlp utterance
    
    :utterance: a SpaCy doc object (https://spacy.io/api/doc) or list of tokens
    :pos: the list of part of speech you want to remove 
    (see this list for examples: https://spacy.io/usage/linguistic-features#pos-tagging)
    :return: list of SpaCy tokens minus the dependency
    """
    return [token for token in utterance if token.pos_ not in pos]

def split_contractions(utterance):
    """
    Replaces contracts with their full counterparts. 
    e.g. don't becomes do not. 
    
    :utterance: phrase in a string.
    :return: expanded utterance with no contractions.
    """
    return contractions.fix(utterance)

def convert_emoticons(utterance):
    """
    Converts emoticons like :) to word representations.

    :utterance: phrase in a string.
    :return: expanded utterance with no emoticons.
    """
    for emot in EMOTICONS:
        utterance = utterance.replace(emot, " ".join(EMOTICONS[emot].replace(",","").replace(":","").split()))
    return utterance

def convert_emojis(utterance):
    """
    Converts emojis to word representations.

    :utterance: phrase in a string.
    :return: expanded utterance with no emojis.
    """
    for emot in UNICODE_EMO:
        utterance = utterance.replace(emot, " ".join(UNICODE_EMO[emot].replace(",","").replace(":","").replace('_', ' ').split()))
    return utterance



class TextPreprocessing():

    def __init__(self, utterances, pipes = ['entity_ruler', 'sentencizer']) -> None:
        self.raw_utterances = utterances
        self.cleaned_utterances = self.raw_utterances
        self.nlp_utterances = None

        # Load SpaCy model
        self.nlp = spacy.load('en_core_web_sm')
        # Load SpaCy pipeline 
        if pipes != None:
            self.load_nlp_pipe(pipes)
        
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

    def clean_text(self,
        drop_excess_whitespace=True,
        drop_html=True,
        clean_ascii=True):

        if drop_excess_whitespace: 
            self.cleaned_utterances = list(map(remove_excess_whitespace, self.cleaned_utterances))
        if drop_html: 
            self.cleaned_utterances = list(map(remove_html_tags, self.cleaned_utterances))
        if clean_ascii: 
            self.cleaned_utterances = list(map(convert_non_ascii, self.cleaned_utterances))

    def normalise_text(self,
        fix_spelling=False,
        normalise_contractions=True,
        normalise_emojis=True,
        norm_ents=None,
        lemma=True):

        if fix_spelling:
            self.cleaned_utterances = list(map(correct_spelling, self.cleaned_utterances))
        if normalise_contractions:
            self.cleaned_utterances = list(map(split_contractions, self.cleaned_utterances))
        if normalise_emojis:
            self.cleaned_utterances = list(map(convert_emoticons, self.cleaned_utterances))
            self.cleaned_utterances = list(map(convert_emojis, self.cleaned_utterances))

        if self.nlp_utterances == None:
             self.nlp_utterances = list(self.nlp.pipe(self.cleaned_utterances))
            
        if norm_ents != None:
            self.nlp_utterances = list(map(lambda utterance: \
                norm_entity(utterance, norm_ents), self.nlp_utterances))
        if lemma:
            self.nlp_utterances = list(map(lemmatise, self.nlp_utterances))

    def filter_text(self, 
        drop_stop_words=True,
        drop_punctuation=True,
        drop_pos = None,
        drop_dep = None,
        drop_ent = None):

        if self.nlp_utterances == None:
            self.nlp_utterances = list(self.nlp.pipe(self.cleaned_utterances))
        
        if drop_stop_words:
            self.nlp_utterances = list(map(remove_stop_words, self.nlp_utterances))
        if drop_punctuation:
            self.nlp_utterances = list(map(remove_punctuation, self.nlp_utterances))
        if drop_pos != None:
            self.nlp_utterances = list(map(lambda utterance: \
                remove_pos(utterance, drop_pos), self.nlp_utterances))
        if drop_dep != None:
            self.nlp_utterances = list(map(lambda utterance: \
                remove_dependency(utterance, drop_dep), self.nlp_utterances))
        if drop_ent != None:
            self.nlp_utterances = list(map(lambda utterance: \
                remove_entity(utterance, drop_ent), self.nlp_utterances))

    def preprocess(self):
        self.clean_text()
        self.normalise_text(
            fix_spelling=True,
            norm_ents=None,
            lemma=False)
        self.filter_text()
        self.normalise_text(
            norm_ents=[
                'PERSON',
                'DATE',
                'TIME',
                'MONEY',
                'QUANTITY',
                'ORDINAL',
                'CARDINAL',
                'PERCENT',
            ],
            lemma=True)