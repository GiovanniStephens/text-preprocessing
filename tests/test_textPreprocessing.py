import unittest
import TextPreprocessing as tp

class test_textPreprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Instantiates the preprocessor"""
        self.test_utterances = [
            'This is a testing sentence.',
            'This is also a test phrase.',
            'Some things don\'t match with the others.'
        ]
        self.proprocessor = \
            tp.TextPreprocessing(self.test_utterances)

    def test_pipes_loaded(self):
        """Tests that the NLP pipeline has been correctly set up."""
        self.assertEquals(self.proprocessor.nlp.pipe_names, \
             ['tagger', 'sentencizer', 'parser', 'ner', 'entity_ruler'])

if __name__ == '__main__':
    unittest.main()