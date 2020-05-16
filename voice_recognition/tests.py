# import speech_recognition as sr
from word2number import w2n
import unittest


class WordToNumberTest(unittest.TestCase):
    def test_decimal(self):
        self.assertEqual(w2n.word_to_num('two point three'), 2.3)
        self.assertEqual(w2n.word_to_num('two point zero three'), 2.03)

    def test_integer(self):
        self.assertEqual(w2n.word_to_num('two'), 2)
        self.assertEqual(w2n.word_to_num('two million three thousand nine hundred and eighty four'), 2003984)
        self.assertEqual(w2n.word_to_num('one hundred thirty-five'), 135)
        self.assertEqual(w2n.word_to_num('one hundred thirty five'), 135)
