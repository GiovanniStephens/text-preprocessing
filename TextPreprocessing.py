import spacy

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