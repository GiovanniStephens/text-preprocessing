import unittest
import TextPreprocessing as tp
from TextPreprocessing import remove_html_tags

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

    def test_remove_dep(self):
        """Tests removing a dependency from a test utterance."""
        no_dep = tp.remove_dependency(\
            self.proprocessor.nlp_utterances[3], 'nsubj')
        text_no_dep = [token.text for token in no_dep]
        self.assertEqual(text_no_dep, ['is', 'a', 'common', 'name', '.'])

    def test_remove_pos(self):
        """Tests removing nouns from a test utterance."""
        no_pos = tp.remove_pos(\
            self.proprocessor.nlp_utterances[3], 'NOUN')
        text_no_pos = [token.text for token in no_pos]
        self.assertEqual(text_no_pos, ['John', 'is', 'a', 'common', '.'])

    def test_correct_spelling(self):
        """Testing the spell checker."""
        tp.load_sym_spell_dict()
        self.assertEqual(tp.correct_spelling('thsi is a test.'), 'this is a test')

    def test_correct_spelling_joined(self):
        """Testing the spell checker with joined words."""
        tp.load_sym_spell_dict()
        self.assertEqual(tp.correct_spelling('somethingcaroline did.'), \
             'something caroline did')

    def test_correct_spelling_caps(self):
        """Testing the spell checker with joined words."""
        tp.load_sym_spell_dict()
        self.assertEqual(tp.correct_spelling('somethingCaroline DID.'), \
            'something Caroline DID')

    def test_remove_html_tags(self):
        """Test removing HTML tags from a string."""
        self.assertEqual(tp.remove_html_tags('<title>Testing string</title>'), \
            'Testing string')

    def test_remove_excess_whitespace(self):
        """Test removing excess white space."""
        self.assertEqual(tp.remove_excess_whitespace('Hello  World   From Gio \t\n\r\tHi There'), \
            'Hello World From Gio Hi There')

    def test_convert_non_ascii(self):
        """Test transliterating non-ASCII characters to ASCII characters."""
        self.assertEqual(tp.convert_non_ascii('¿Hola, cómo estás, coño?'), \
            '?Hola, como estas, cono?')

if __name__ == '__main__':
    unittest.main()