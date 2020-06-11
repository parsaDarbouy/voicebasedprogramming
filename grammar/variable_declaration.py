# May have problem in this parts:
# Dictionary in dictionary
# Dictionary in list has not been defined yet

import functools

import inflect


class VariableDeclaration:

    def __init__(self, command):
        self.variable_types = ['integer', 'float', 'string', 'list', 'dictionary']
        self.command = command
        self.name = self.find_name()
        self.type = self.find_type()
        self.value = self.find_value()
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

    def find_type(self) -> str:
        """
        This function finds the variable which will be declared.
            Returns:
                The type of variable of the variable declarationcommand.
        """
        variable_type = self.command[self.find_is_keyword_index() + 1]
        return variable_type

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

    def find_last_index_of_string(self, input_list: list) -> int:
        """
        This function, when we wants to declare a string in the list, finds the last index of the string.
            Args:
                input_list: The list of words which contains the string
                            and also the remaining command of list declaration.
            Returns:
                The last index of the string in the list declaration command.
        """
        for index, item in enumerate(input_list):
            if item == 'next' and input_list[index + 1] in self.variable_types:  # problem : next + variable_type can
                # be part of the string
                return index
            if item == 'end' and input_list[index + 1] == 'of' and input_list[index + 2] == 'list':  # problem : end
                # of list can be a part of the string
                return index

    def find_last_index_of_string_in_dictionary(self, input_list: list) -> int:
        """
                This function, when we wants to declare a string in the dictionary, finds the last index of the string.
                    Args:
                        input_list: The list of words which contains the string
                                    and also the remaining command of dictionary declaration.
                    Returns:
                        The last index of the string in the dictionary declaration command.
                """
        for index, item in enumerate(input_list):
            if input_list[index + 1] in self.variable_types:
                return index + 1
            if item == 'then' and input_list[index + 1] in self.variable_types:  # problem : then + variable_type can
                # be part of the string
                return index
            if item == 'end' and input_list[index + 1] == 'of' and input_list[index + 2] == 'dictionary':  # problem
                # : end of dictionary can be a part of the string
                return index

    @staticmethod
    def inner_list_check(input_list: list, index: int) -> bool:
        """
        This function, in the list declaration, checks
        whether this index of the list is the last index of the list declaration or not.
        This will be useful when we have inner lists.
            Args:
                input_list: The list of words which contains the inner list declaration and remaining of the command.
                index: The specified index that should be checked.
            Returns:
                If the index is the last index returns true, Otherwise returns false.
        """
        if input_list[index - 1] != 'list':
            return True
        if index == 0:
            return True
        if input_list[index - 1] == 'list' and input_list[index - 2] == 'of' and input_list[index - 3] == 'end':
            return True
        return False

    def parse_list(self, input_list: list) -> list:
        """
        This function gets the command which is declaring lists, and declare the variables inside the list.
            Args:
                input_list: The list of words which contains the list declaration.
            Returns:
                The list which has been declared with the input command.
        """
        this_type, this_list = None, []
        index, item = -1, None
        while True:
            index += 1
            item = input_list[index]
            if item == 'end' and input_list[index + 1] == 'of' and input_list[index + 2] == 'list':
                break
            if item == 'next':
                continue
            if item in self.variable_types and self.inner_list_check(input_list, index):
                this_type = item
                continue
            if this_type == 'integer':
                this_list.append(int(item))
            elif this_type == 'float':
                this_list.append(float(f'{item}.{input_list[index + 2]}'))
                index += 2
            elif this_type == 'string':
                end_of_string = self.find_last_index_of_string(input_list[index:]) + index
                this_string = self.parse_string(input_list[index:end_of_string])
                this_list.append(this_string[1:len(this_string) - 1])
                index += end_of_string - index - 1
            elif this_type == 'list':
                parse_list_result = self.parse_list(input_list[index:])
                this_list.append(parse_list_result[0])
                index += parse_list_result[1] - 1
        return [this_list, index + 3]

    def parse_dictionary(self, input_list: list) -> dict:
        """
                This function gets the command which is declaring dictionary, and declare the variables inside the list.
                    Args:
                        input_list: The list of words which contains the dictionary declaration.
                    Returns:
                        The dictionary which has been declared with the input command.
                """
        this_type, this_dict = None, {}
        index, item = -1, None
        key_is_set = False
        key = None
        while True:
            index += 1
            item = input_list[index]
            if item == 'end' and index + 3 == len(input_list):
                break
            elif item == 'then':
                continue
            if item in self.variable_types and self.inner_list_check(input_list, index):
                this_type = item
                continue
            elif this_type == 'string':
                end_of_string = self.find_last_index_of_string_in_dictionary(input_list[index:]) + index
                this_string = self.parse_string(input_list[index:end_of_string])
                if key_is_set:
                    key_value = this_string[1:len(this_string) - 1]
                    this_dict[key] = key_value
                    key_is_set = False
                else:
                    key = this_string[1:len(this_string) - 1]
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
                if key_is_set:
                    key_value = self.parse_list(input_list[index:])
                    this_dict[key] = key_value[0]
                    key_is_set = False
                    index += key_value[1] - 1
                else:
                    parse_list_result = self.parse_list(input_list[index:])
                    key = parse_list_result[0]
                    key_is_set = True
                    index += parse_list_result[1] - 1
        return this_dict

    def find_value(self) -> str:
        """
        This function finds the value of the variable which has to be declared based on the type.
            Returns:
                The exact value of the variable.
        """
        is_keyword_index = self.find_is_keyword_index()
        value = None
        if self.type == 'integer':
            value = self.command[is_keyword_index + 2]
        elif self.type == 'float':
            value = f'{self.command[is_keyword_index + 2]}.{self.command[is_keyword_index + 4]}'
        elif self.type == 'string':
            value = self.parse_string(self.command[is_keyword_index + 2:])
        elif self.type == 'list':
            value = self.parse_list(self.command[is_keyword_index + 2:])[0]
        elif self.type == 'dictionary':
            value = self.parse_dictionary(self.command[is_keyword_index + 2:])
        return value

    def find_name(self) -> str:
        """
        This function finds the name of the variable which has to be declared.
            Returns:
                The exact name of the variable.
        """
        end_of_name = self.find_is_keyword_index()
        words_of_name = self.command[1:end_of_name]
        return self.convert_to_snake_case(words_of_name)

    def find_is_keyword_index(self) -> int:
        """
        This function finds the index of the *is* keyword, which can find name value of the variable based on that.
            Returns:
                The exact index of the *is* variable.
        """
        is_keyword_indices = [index for index, value in enumerate(self.command) if value == 'is']
        is_keyword_index = filter(lambda index: index if self.command[index + 1] in self.variable_types else 0,
                                  is_keyword_indices)
        is_keyword_index = max(list(is_keyword_index))
        return is_keyword_index

    def generate_code(self) -> str:
        """
        This function generates the final code of the input command.
            Returns:
                The exact code of the variable declaration command.
        """
        code = f'{self.name} = {self.value}'
        return code
