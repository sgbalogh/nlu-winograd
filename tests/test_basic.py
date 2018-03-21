from .context import wnlu
import unittest
import copy

class BasicTestSuite(unittest.TestCase):
    """Some tests of basic package functionality."""

    def test_translator_loads_davis_examples(self):
        translator = wnlu.WinogradTranslator()
        self.assertEqual(len(translator.schemata), 283)

    def test_translator_premise(self):
        translator = wnlu.WinogradTranslator()
        example = translator.schemata[0]
        self.assertEqual(example.get_premise(), "The city councilmen refused the demonstrators a permit because they feared violence.")