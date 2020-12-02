import spacy
import functools
from toolz import compose

# def pipeline_func(data, fns):
#         return functools.reduce(lambda a, x: x(a), fns, data)

def remove_stop_words(utterance):
        return [token for token in utterance if not token.is_stop]

def remove_punctuation(utterance):
        return [token for token in utterance if not token.is_punct]

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
