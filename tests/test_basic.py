from .context import wnlu
import unittest
import copy

class BasicTestSuite(unittest.TestCase):
    """Some tests of basic package functionality."""

    def test_translator_loads_davis_examples(self):
        translator = wnlu.WinogradTranslator()
        self.assertEqual(len(translator.get_dev_set()), 141)

    def test_translator_premise(self):
        translator = wnlu.WinogradTranslator()
        example = translator.get_dev_set()[0]
        self.assertEqual(example.get_premise(), "The city councilmen refused the demonstrators a permit because they feared violence.")

    def test_proper_noun_normalization(self):
        examples = {
            "The dogs" : False,
            "Stephen" : True,
            "Casinos" : False,
            "A car" : False,
            "Wesley" : True,
            "Zhengdao" : True,
            "Pooja" : True,
            "Frank" : True,
            "Los Angeles" : True,
            "Cars" : False
        }
        incorrect = 0
        for phrase,value in examples.items():
            standardized = wnlu.Utils.standardize_noun_phrase(phrase)
            unchanged = (phrase == standardized)
            if unchanged != value:
                incorrect += 1
                print("Standardized: " + standardized)
                print("Original: " + phrase)
        self.assertEqual(incorrect, 0)

    def test_noun_possessive(self):
        examples = {
            "Stephen": "Stephen's",
            "The cat" : "The cat's",
            "The cats" : "The cats'"
         }
        incorrect = 0
        for np,poss in examples.items():
            if not wnlu.Utils.make_noun_phrase_possessive(np) == poss:
                incorrect += 1
        self.assertEqual(incorrect, 0)

    def test_pronoun_needs_posessive_noun(self):
        examples = {
            "his" : True,
            "he" : False,
            "her" : True,
            "their" : True,
            "us" : False
        }
        incorrect = 0
        for pronoun,needpos in examples.items():
            if not wnlu.Utils.is_possessive_determiner(pronoun) == needpos:
                incorrect += 1
        self.assertEqual(incorrect, 0)
