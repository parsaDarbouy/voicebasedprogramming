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
        if 'letters' in input_string and len(input_string) - 1 != input_string.index('letters'):
            for index, word in enumerate(input_string[:len(input_string) - 1]):
                if word == 'letters':
                    number_value = input_string[index + 1]
                    if 57 >= ord(number_value[0]) >= 10:
                        input_string[index + 1] = inflect.engine().number_to_words(int(number_value))
                        input_string.pop(index)
        value = str(functools.reduce(lambda first, second: f'{first} {second}', input_string))
        return f'\'{value}\''

    def find_last_index_of_string(self, input_list: list) -> int:
        for index, item in enumerate(input_list):
            if item == 'next' and input_list[index + 1] in self.variable_types: # problem : next + variable_type can
                # be part of the string
                return index
            if item == 'end' and input_list[index + 1] == 'of' and input_list[index + 2] == 'list': # problem : end
                # of list can be a part of the string
                return index

    @staticmethod
    def find_last_index_of_list(input_list: list) -> int:
        for index, item in enumerate(input_list):
            if item == 'end' and input_list[index + 1] == 'of' and input_list[index + 2] == 'list':
                return index + 3

    def find_last_index_of_string_in_dictionary(self, input_list: list) -> int:
        for index, item in enumerate(input_list):
            if input_list[index + 1] in self.variable_types:
                return index + 1
            if item == 'then' and input_list[index + 1] in self.variable_types:  # problem : then + variable_type can
                # be part of the string
                return index
            if item == 'end' and input_list[index + 1] == 'of' and input_list[index + 2] == 'dictionary':  # problem
                # : end of dictionary can be a part of the string
                return index

    def parse_list(self, input_list: list) -> list:
        this_type, this_list = None, []
        index, item = -1, None
        while True:
            index += 1
            item = input_list[index]
            if item == 'end' and index + 3 == len(input_list):
                break
            if item == 'next':
                continue
            if item in self.variable_types and (input_list[index - 1] != 'list' or index == 0):
                this_type = item
                continue
            if this_type == 'integer':
                this_list.append(int(item))
            elif this_type == 'float':
                this_list.append(float(f'{item}.{input_list[index + 2]}'))
                index += 2
            elif this_type == 'string':
                end_of_string = self.find_last_index_of_string(input_list[index:]) + index
                this_list.append(self.parse_string(input_list[index:end_of_string]))
                index += end_of_string - index - 1
            elif this_type == 'list':
                end_of_list = self.find_last_index_of_list(input_list[index:]) + index
                this_list.append(self.parse_list(input_list[index:end_of_list]))
                index += end_of_list - index - 1
        return this_list

    def parse_dictionary(self, input_list: list) -> dict:
        this_type, this_dict = None, {}
        index, item = -1, None
        key_is_set = False
        while True:
            index += 1
            item = input_list[index]
            if item == 'end' and index + 3 == len(input_list):
                break
            elif item == 'then':
                continue
            if item in self.variable_types and (input_list[index - 1] != 'list' or index == 0):
                this_type = item
                continue
            elif this_type == 'string':
                end_of_string = self.find_last_index_of_string_in_dictionary(input_list[index:]) + index
                if key_is_set:
                    key_value = self.parse_string(input_list[index:end_of_string])
                    this_dict[key] = key_value
                    key_is_set = False
                else:
                    key = self.parse_string(input_list[index:end_of_string])
                    key_is_set = True
                index += end_of_string - index - 1
            elif this_type == 'integer':
                if key_is_set:
                    key_value = int(item)
                    this_dict[key] = key_value
                    key_is_set = False
                else:
                    key = int(item)
                    key_is_set = True
            elif this_type == 'float':
                if key_is_set:
                    key_value = float(f'{item}.{input_list[index + 2]}')
                    this_dict[key] = key_value
                    key_is_set = False
                    index += 2
                else:
                    key = float(f'{item}.{input_list[index + 2]}')
                    key_is_set = True
                    index += 2
            elif this_type == 'list':
                continue
        return this_dict

    def find_value(self) -> str:
        is_keyword_index = self.find_is_keyword_index()
        value = None
        if self.type == 'integer':
            value = self.command[is_keyword_index + 2]
        elif self.type == 'float':
            value = f'{self.command[is_keyword_index + 2]}.{self.command[is_keyword_index + 4]}'
        elif self.type == 'string':
            value = self.parse_string(self.command[is_keyword_index + 2:])
        elif self.type == 'list':
            value = self.parse_list(self.command[is_keyword_index + 2:])
        elif self.type == 'dictionary':
            value = self.parse_dictionary(self.command[is_keyword_index + 2:])
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

