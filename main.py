from voice_recognition.recognizers import GoogleRecognizer
from right_keyword_interpretation.keyword_recognition import keyword_recognition
from grammar.command_to_code import CommandToCode

from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.recognizer = GoogleRecognizer()
        self.code_converter = CommandToCode()
        self.indent = 0
        self.indent_phrases = ["if condition", "define function"]
        self.revert_indent_phrases = ["end of if", "end of function"]
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)
        self.filename = None

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.labelFrame2 = ttk.LabelFrame(self, text="listen")
        self.labelFrame2.grid(column=4, row=1, padx=20, pady=20)

        self.button()
        self.button_to_listen()

    def button(self):
        self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.button.grid(column=1, row=1)

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(title="Select A File", parent=self)
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)

    def button_to_listen(self):
        self.button2 = ttk.Button(self.labelFrame2, text="listen", command=self.main)
        self.button2.grid(column=2, row=1)

    def main(self):
        print(self.filename)
        if self.filename is not None:
            file = open(self.filename, "a")
            text = self.recognizer.recognize()
            words_list = keyword_recognition(text)
            print(text)
            if words_list[0] == "remove" and words_list[1] == "line":
                line_number = int(words_list[2])
                temp_file = open(self.filename, "w")
                lines = temp_file.readlines()
                lines.remove(lines[line_number - 1])
                file.close()
                temp_file.close()
                temp_file = open(self.filename, "w")
                temp_file.writelines(lines)
                temp_file.close()
            self.code_converter.set_command(words_list)
            if ' '.join(words_list[-3:]) in self.revert_indent_phrases and self.indent - 1 >= 0:
                self.indent -= 1
            file.write((self.indent * '\t') + self.code_converter.generate_code() + "\n")
            if ' '.join(words_list[:2]) in self.indent_phrases:
                self.indent += 1
            file.close()


root = Root()
root.mainloop()
