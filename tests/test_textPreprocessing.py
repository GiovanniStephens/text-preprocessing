import unittest
import TextPreprocessing as tp
from TextPreprocessing import remove_html_tags
import spacy

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
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=False,
            drop_punctuation=True)
        self.assertEqual(['This', 'is', 'a', 'testing', 'sentence'], \
            [token.text for token in self.proprocessor.nlp_utterances[0]])

    def test_remove_stop_words(self):
        """Checks that stop words are being removed correctly."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=True,
            drop_punctuation=False)
        no_stop_words = self.proprocessor.nlp_utterances[0]
        text_no_stop_words = [token.text for token in no_stop_words]
        self.assertEqual(text_no_stop_words, ['testing', 'sentence', '.'])

    def test_remove_punctuation(self):
        """Tests whether punctuation is correctly removed."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=False,
            drop_punctuation=True)
        no_punc = self.proprocessor.nlp_utterances[0]
        text_no_punct = [token.text for token in no_punc]
        self.assertEqual(text_no_punct, ['This', 'is', 'a', 'testing', 'sentence'])

    def test_stop_and_punct_removal(self):
        """Test removing punctuation and stop words.""" 
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=True,
            drop_punctuation=True)
        cleaned_text = [token.text for token in self.proprocessor.nlp_utterances[0]]
        self.assertEqual(cleaned_text, ['testing', 'sentence'])

    def test_remove_entity(self):
        """Tests removing an entity from a test utterance."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=False,
            drop_punctuation=False,
            drop_ent=['PERSON'])
        no_ent = self.proprocessor.nlp_utterances[3]
        text_no_ent = [token.text for token in no_ent]
        self.assertEqual(text_no_ent, ['is', 'a', 'common', 'name', '.'])

    def test_remove_dep(self):
        """Tests removing a dependency from a test utterance."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=False,
            drop_punctuation=False,
            drop_dep=['nsubj'])
        no_dep = self.proprocessor.nlp_utterances[3]
        text_no_dep = [token.text for token in no_dep]
        self.assertEqual(text_no_dep, ['is', 'a', 'common', 'name', '.'])

    def test_remove_pos(self):
        """Tests removing nouns from a test utterance."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.filter_text(
            drop_stop_words=False,
            drop_punctuation=False,
            drop_pos=['NOUN'])
        no_pos = self.proprocessor.nlp_utterances[3]
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

    def test_correct_spelling_acronyms(self):
        """Shows how the spell-checker works."""
        tp.load_sym_spell_dict()
        self.assertEqual(tp.correct_spelling('I have never been to the US.'), \
            'I have never been to the US')

    def test_correct_spelling_contractions(self):
        """Shows how the spell-checker works with contractions."""
        tp.load_sym_spell_dict()
        self.assertEqual(tp.correct_spelling('I\'ve never been to the US though I\'m keen.'), \
            'Have never been to the US though I\'m keen')

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

    def test_split_contractions(self):
        """Test contractions splitter."""
        self.assertEqual(tp.split_contractions('I\'m wanting to test this.'), \
            'I am wanting to test this.')

    def test_convert_emoticons(self):
        """Test converting emoticons to text representations."""
        self.assertEqual(tp.convert_emoticons('Hi! :D'), \
            'Hi! Laughing big grin or laugh with glasses')

    def test_convert_emojis(self):
        """Tests converting emojis to a text representation."""
        self.assertEqual(tp.convert_emojis('Hilarious 😂.'), \
            'Hilarious face with tears of joy.')

    def test_norm_entity(self):
        """Tests normalising an entity."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.normalise_text(
            fix_spelling=False,
            normalise_contractions=False,
            normalise_emojis=False,
            norm_ents=['PERSON'],
            lemma=False)
        norm = self.proprocessor.nlp_utterances[3]
        norm_text = [token.text if isinstance(token, spacy.tokens.token.Token) \
            else token for token in norm]
        self.assertEqual(norm_text, ['PERSON', 'is', 'a', 'common', 'name', '.'])

    def test_lemmatise(self):
        """"Tests lemmatising the phrases."""
        self.proprocessor.nlp_utterances = None
        self.proprocessor.normalise_text(
            fix_spelling=False,
            normalise_contractions=False,
            normalise_emojis=False,
            norm_ents=None,
            lemma=True)
        norm = self.proprocessor.nlp_utterances[0]
        norm_text = [token.text if isinstance(token, spacy.tokens.token.Token) \
            else token for token in norm]
        self.assertEqual(norm_text, ['this', 'be', 'a', 'testing', 'sentence', '.'])

    def test_end_to_end(self):
        test_phrase = ['<p>Tis iz a testing thingy. I\'m wantin to test. John ows me $200 >.<.   </p>']
        processor = tp.TextPreprocessing(test_phrase)
        processor.clean_text()
        processor.normalise_text(
            fix_spelling=True,
            normalise_contractions=True,
            normalise_emojis=True,
            norm_ents=None,
            lemma=False
        )
        processor.filter_text(
            drop_stop_words=True,
            drop_punctuation=True,
            drop_pos = None,
            drop_dep = None,
            drop_ent = None
        )
        processor.normalise_text(
            fix_spelling=False,
            normalise_contractions=False,
            normalise_emojis=False,
            norm_ents=['PERSON', 'CURRENCY', 'MONEY', 'CARDINAL'],
            lemma=True
        )
        norm = processor.nlp_utterances[0]
        norm_text = [token.text if isinstance(token, spacy.tokens.token.Token) \
            else token for token in norm]
        self.assertEqual(norm_text, ['testing', 'thingy', 'want', 'test', 'PERSON', 'CARDINAL'])

if __name__ == '__main__':
    unittest.main()