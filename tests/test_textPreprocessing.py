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
        """Tests that the SpaCy NLP pipeline has been correctly set up."""
        self.assertEqual(self.proprocessor.nlp.pipe_names, \
             ['tagger', 'sentencizer', 'parser', 'ner', 'entity_ruler'])

    def test_no_additonal_pipes(self):
        """Tests that the default pipes get loaded in the SpaCy NLP pipeline"""
        preprocessor = tp.TextPreprocessing(self.test_utterances, pipes=None)
        self.assertEqual(preprocessor.nlp.pipe_names, \
             ['tagger', 'parser', 'ner'])

    def test_tokenizer(self):
        """Tests to see if the preprocessor has tokenised correctly"""
        self.assertEqual(['This', 'is', 'a', 'testing', 'sentence', '.'], \
            [token.text for token in self.proprocessor.nlp_utterances[0]])

if __name__ == '__main__':
    unittest.main()