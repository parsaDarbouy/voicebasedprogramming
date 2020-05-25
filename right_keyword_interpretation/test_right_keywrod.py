import unittest

from right_keyword_interpretation.keyword_recognition import keyword_recognition
from right_keyword_interpretation.right_keyword import right_keyword
from right_keyword_interpretation.soundex_generator import soundex_generator

test_answer = [('def', 0.5, 'D1'), ('is', 0.5, 'I2'), ('variable', 0.5, 'V614'), ('string', 0.5, 'S365'),
               ('integer', 0.5, 'I532'), ('float', 0.5, 'F432'), ('list', 0.5, 'L232'), ('Dictionary', 0.5, 'D235')]
test_case_soundex = ['def', 'is', 'variable', 'string', 'integer', 'float', 'list', 'Dictionary']


class TestRightKeywordInterpretation(unittest.TestCase):

    def test_soundex_generator(self):
        self.assertEqual(
            soundex_generator(test_case_soundex), test_answer)

    def test_right_keyword(self):
        self.assertEqual(right_keyword("depth"), "def")
        self.assertEqual(right_keyword("deep"), "def")
        # self.assertEqual(right_keyword("ease"), "is")
        # self.assertEqual(right_keyword("Valuable"), "variable")

    def test_keyword_recognition(self):
        self.assertEqual(keyword_recognition("Valuable dog is teacher 2"), "variable dog is integer 2")
        self.assertEqual(keyword_recognition("depth Stream"), "def string")


if __name__ == '__main__':
    unittest.main()
