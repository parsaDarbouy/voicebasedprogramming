from if_condition import IfCondition
from function_definition import FunctionDefinition
from variable_declaration import VariableDeclaration


class CommandToCode:

    def __init__(self):
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

    def generate_code(self) -> str:
        """
        This function, based on the command, generates the final code of the input command.
            Returns:
                The code of the input command.
        """
        if self.command is None:
            return 'Command has not been assigned.'
        elif self.command[0] == 'variable':
            return VariableDeclaration(self.command).code
        elif self.command[0] == 'if' and self.command[1] == 'condition':
            return IfCondition(self.command).code
        elif self.command[0] == 'define' and self.command[1] == 'function':
            return FunctionDefinition(self.command).code
        elif self.command[0] == 'end' and self.command[1] == 'of' and (self.command[2] == 'function' or self.command[2] == 'if'):
            return ''
        else:
            return 'Command format is wrong'