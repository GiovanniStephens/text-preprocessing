import spacy
import functools
from toolz import compose

# def pipeline_func(data, fns):
#         return functools.reduce(lambda a, x: x(a), fns, data)

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
