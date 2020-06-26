from builtins import Exception

from grammar.if_condition import IfCondition
from grammar.function_definition import FunctionDefinition
from grammar.variable_declaration import VariableDeclaration
from grammar.return_function import ReturnFunction
from grammar.function_call import FunctionCall


class CommandToCode:

    def __init__(self):
        self.variable_types = ['integer', 'float', 'string', 'list', 'dictionary', 'variable', 'operation']
        self.command = None

    def set_command(self, command: list):
        """
        This function sets the command variable.
            Args:
                command: The list of words which will be converted to code.
        """
        self.command = command

    def remove_command(self):
        """
        This function deletes the current command.
        """
        self.command = None

    def variable_error_check(self):
        """
        This function checks the correctness of variable declaration commands.
        """
        if len(self.command) < 5:
            raise Exception("The Format Is Wrong")
        is_index, point_index = -1, -1
        for index, item in enumerate(self.command):
            if item == 'is' and self.command[index + 1] in self.variable_types:
                is_index = index
            if item == 'point':
                point_index = index
        if is_index == -1:
            raise Exception("Is Keyword Not Found")
        if self.command[is_index + 1] not in self.variable_types:
            raise Exception("Variable Type Is Unacceptable")
        if self.command[is_index + 1] == 'float':
            if point_index == -1 or point_index < is_index + 1:
                raise Exception("The Value Is Not Float")
            if not self.command[point_index - 1].isdigit():
                raise Exception("The Value Is Not Float")
            if not self.command[point_index + 1].isdigit():
                raise Exception("The Value Is Not Float")
        if self.command[is_index + 1] == 'integer':
            if not self.command[-1].isdigit():
                raise Exception("The Value Is Not Number")
        if self.command[is_index + 1] == 'operation':
            if self.command[is_index + 2] == 'add':
                if 'to' not in self.command[is_index + 2:]:
                    raise Exception("To keyword not found")
                if self.command[is_index + 3] not in ['integer', 'float', 'string', 'list', 'variable']:
                    raise Exception("Variable Type is Unacceptable")
            elif self.command[is_index + 2] == 'subtract':
                if 'from' not in self.command[is_index + 2:]:
                    raise Exception("From keyword not found")
                if self.command[is_index + 3] not in ['integer', 'float', 'string', 'list', 'variable']:
                    raise Exception("Variable Type is Unacceptable")
            elif self.command[is_index + 2] == 'multiply' or self.command[is_index + 2] == 'divide':
                if 'by' not in self.command[is_index + 2:]:
                    raise Exception("By keyword not found")
                if self.command[is_index + 3] not in ['integer', 'float', 'string', 'list', 'variable']:
                    raise Exception("Variable Type is Unacceptable")
            else:
                raise Exception("Operation Type Is Unacceptable")


    def return_error_check(self):
        """
        This function checks the correctness of return commands.
        """
        if len(self.command) < 3:
            raise Exception("The Format Is Wrong")
        if self.command[1] not in self.variable_types + ['variable']:
            raise Exception("Variable Type Is Wrong")
        if self.command[1] != 'variable':
            this_command = self.command
            self.command = ['variable', '_', 'is'] + self.command[1:]
            self.variable_error_check()
            self.command = this_command

    def function_call_error_check(self):
        """
        This function checks the correctness of function call commands.
        """
        if len(self.command) < 9:
            raise Exception("The Format Is Wrong")
        if 'parameters' not in self.command:
            raise Exception("Argument Parameters Is Missed")
        if self.command[-1] != 'parameters':
            raise Exception("End of Parameters Not Found")
        if self.command[-2] != 'of':
            raise Exception("End of Parameters Not Found")
        if self.command[-1] != 'end':
            raise Exception("End of Parameters Not Found")

    def generate_code(self) -> str:
        """
        This function, based on the command, generates the final code of the input command.
            Returns:
                The code of the input command.
        """
        if self.command is None:
            return 'Command has not been assigned.'
        elif self.command[0] == 'variable':
            self.variable_error_check()
            return VariableDeclaration(self.command).code
        elif self.command[0] == 'return':
            self.return_error_check()
            return ReturnFunction(self.command).code
        elif self.command[0] == 'function' and self.command[1] == 'call':
            self.function_call_error_check()
            return FunctionCall(self.command).code
        elif self.command[0] == 'if' and self.command[1] == 'condition':
            return IfCondition(self.command).code
        elif self.command[0] == 'define' and self.command[1] == 'function':
            return FunctionDefinition(self.command).code
        elif self.command[0] == 'end' and self.command[1] == 'of' and \
                (self.command[2] == 'function' or self.command[2] == 'if'):
            return ''
        else:
            raise Exception("Invalid Format")
