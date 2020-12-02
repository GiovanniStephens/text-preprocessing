import unittest
import TextPreprocessing as tp

class test_textPreprocessing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Instantiates the preprocessor"""
        self.test_utterances = [
            'This is a testing sentence.',
            'This is also a test phrase.',
            'Some things don\'t match with the others.',
            'John is a common name.'
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

    def test_remove_stop_words(self):
        """Checks that stop words are being removed correctly."""
        no_stop_words = tp.remove_stop_words(\
            self.proprocessor.nlp_utterances[0])
        text_no_stop_words = [token.text for token in no_stop_words]
        self.assertEqual(text_no_stop_words, ['testing', 'sentence', '.'])

    def test_remove_punctuation(self):
        """Tests whether punctuation is correctly removed."""
        no_punc = tp.remove_punctuation(\
            self.proprocessor.nlp_utterances[0])
        text_no_punct = [token.text for token in no_punc]
        self.assertEqual(text_no_punct, ['This', 'is', 'a', 'testing', 'sentence'])

    def test_stop_and_punct_removal(self):
        self.proprocessor.preprocess_text()
        cleaned_text = [token.text for token in self.proprocessor.cleaned_utterances[0]]
        self.assertEqual(cleaned_text, ['testing', 'sentence'])

    def test_remove_entity(self):
        """Tests removing an entity from a test utterance."""
        no_ent = tp.remove_entity(\
            self.proprocessor.nlp_utterances[3], 'PERSON')
        text_no_ent = [token.text for token in no_ent]
        self.assertEqual(text_no_ent, ['is', 'a', 'common', 'name', '.'])

if __name__ == '__main__':
    unittest.main()