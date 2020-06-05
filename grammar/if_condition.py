import functools

import inflect


class IfCondition:

    def __init__(self, command):
        self.variable_types = ['integer', 'float', 'string']   # dictionary and list need to be added
        self.compare_types = ['equal to', 'less than', 'greater than', 'less than or equal to', 'greater than or '
                                                                                                'equal to']
        self.command = command[2:]
        #print([i.split() for i in self.compare_types])
        self.first_part = self.dynamicOrNot(command[2:])
        #self.type = self.find_type()
        self.code = self.generate_code()

    @staticmethod
    def convert_to_snake_case(name: list) -> str:
        """
        This function gives a list a words, and concatenates them in snake case format.
            Args:
                name: The list of words which will be converted to snake case.
            Returns:
                The snake case format of the input list of words.
        """
        snake_case_name = functools.reduce(lambda first, second: f'{first}_{second}', name)
        return str(snake_case_name)

    def dynamicOrNot(self, command):
        if command[0] == 'variable':
            variable = self.find_name()
            return variable

        else:
            variable_type = self.find_type()
            return self.find_value(variable_type)

    def find_name(self) -> str:
        """
        This function finds the name of the dynamic variable.
            Returns:
                The exact name of the variable.
        """
        end_of_name_index = self.find_is_keyword_index()
        this_name = self.convert_to_snake_case(self.command[1:end_of_name_index])
        return this_name
    def find_type(self) -> str:
        """
        This function finds the variable which will be declared.
            Returns:
                The type of variable of the variable declarationcommand.
        """
        variable_type = self.command[0]
        return variable_type
    def find_value(self , variable_type) -> str:
        """
        This function finds the value of the variable which has to be declared based on the type.
            Returns:
                The exact value of the variable.
        """
        value = None
        if variable_type == 'integer':
            value = self.command[1]
        elif variable_type == 'float':
            value = f'{self.command[1]}.{self.command[3]}'
        elif variable_type == 'string':
            is_keyword_index = self.find_is_keyword_index()
            value = self.parse_string(self.command[1: is_keyword_index])
        return value

    @staticmethod
    def parse_string(input_string: list) -> str:
        """
        This function gives a list a words, and concatenates them and creates a string.
            Args:
                input_string: The list of words which will be converted to string.
            Returns:
                The string format of the input list of words.
        """
        if 'letters' in input_string and len(input_string) - 1 != input_string.index('letters'):
            for index, word in enumerate(input_string[:len(input_string) - 1]):
                if word == 'letters':
                    number_value = input_string[index + 1]
                    if 57 >= ord(number_value[0]) >= 10:
                        input_string[index + 1] = inflect.engine().number_to_words(int(number_value))
                        input_string.pop(index)
        value = str(functools.reduce(lambda first, second: f'{first} {second}', input_string))
        return f'\'{value}\''

    def find_is_keyword_index(self) -> int:
        """
        This function finds the index of the *is* keyword, which is followed by compare_types.
            Returns:
                The exact index of the *is* keyword.
        """
        is_keyword_indices = [index for index, value in enumerate(self.command) if value == 'is']
        is_keyword_index = filter(lambda index: index if self.command[index + 1 : index+3] in [compare_type.split() for
                                                        compare_type in self.compare_types] else 0, is_keyword_indices)
        return list(is_keyword_index)[0]
    def generate_code(self):
        """
        This function generates the final code of the input command.
            Returns:
                The exact code of the function definition command.
        """

        return

a = IfCondition("if condition float 32 point 5 is equal to integer 2".split())
print(a.first_part)


