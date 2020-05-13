import functools
import inflect


class VariableDeclaration:

    def __init__(self, command):
        self.variable_types = ['integer', 'float', 'string', 'list', 'dictionary']
        self.command = command.split()
        self.name = self.find_name()
        self.type = self.find_type()
        self.value = self.find_value()
        self.code = self.generate_code()

    @staticmethod
    def convert_to_snake_case(name: list) -> str:
        snake_case_name = functools.reduce(lambda first, second: f'{first}_{second}', name)
        return str(snake_case_name)

    def find_type(self) -> str:
        variable_type = self.command[self.find_is_keyword_index() + 1]
        return variable_type

    @staticmethod
    def parse_string(input_string: list) -> str:
        if 'letters' in input_string and len(input_string) > input_string.index('letters'):
            number_value = input_string[input_string.index('letters') + 1]
            if int(number_value[0]) < 10:
                input_string[input_string.index('letters') + 1] = inflect.engine().number_to_words(int(number_value))
                input_string.remove('letters')
        value = str(functools.reduce(lambda first, second: f'{first} {second}', input_string))
        return value

    def find_value(self) -> str:
        is_keyword_index = self.find_is_keyword_index()
        value = None
        if self.type == 'integer':
            value = self.command[is_keyword_index + 2]
        elif self.type == 'float':
            value = f'{self.command[is_keyword_index + 2]}.{self.command[is_keyword_index + 4]}'
        elif self.type == 'string':
            value = self.parse_string(self.command[is_keyword_index + 2:])
        return value

    def find_name(self) -> str:
        end_of_name = self.find_is_keyword_index()
        words_of_name = self.command[1:end_of_name]
        return self.convert_to_snake_case(words_of_name)

    def find_is_keyword_index(self) -> int:
        is_keyword_indices = [index for index, value in enumerate(self.command) if value == 'is']
        is_keyword_index = filter(lambda index: index if self.command[index + 1] in self.variable_types else 0,
                                  is_keyword_indices)
        is_keyword_index = max(list(is_keyword_index))
        return is_keyword_index

    def generate_code(self) -> str:
        code = f'{self.name} = {self.value}'
        return code
