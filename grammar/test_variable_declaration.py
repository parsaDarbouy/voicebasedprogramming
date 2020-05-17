import unittest

from variable_declaration import VariableDeclaration


class TestVariableDeclaration(unittest.TestCase):

    def test_integer(self):
        self.assertEqual(VariableDeclaration('variable my integer is number is integer 22').code,
                         'my_integer_is_number = 22')
        self.assertEqual(VariableDeclaration('variable number is integer 223425').code, 'number = 223425')

    def test_float(self):
        self.assertEqual(VariableDeclaration('variable my floating number is float 7 point 56').code,
                         'my_floating_number = 7.56')
        self.assertEqual(VariableDeclaration('variable number is integer 0 point 0').code, 'number = 0')
        self.assertEqual(VariableDeclaration('variable number is long is integer 0435235 point 0').code,
                         'number_is_long = 0435235')

    def test_string(self):
        self.assertEqual(VariableDeclaration('variable my first string is sentence is string my name is sina').code,
                         'my_first_string_is_sentence = \'my name is sina\'')
        self.assertEqual(VariableDeclaration('variable my second string is string consider the number 42').code,
                         'my_second_string = \'consider the number 42\'')
        self.assertEqual(VariableDeclaration('variable my third string is string consider the number letters 42').code,
                         'my_third_string = \'consider the number forty-two\'')

    def test_list(self):
        pass

    def test_dictionary(self):
        pass


if __name__ == '__main__':
    unittest.main()
