from voice_recognition.recognizers import SphinxRecognizer
from right_keyword_interpretation.keyword_recognition import keyword_recognition
from grammar.variable_declaration import VariableDeclaration

from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)
        self.wm_iconbitmap('icon.ico')
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
            recognizer = SphinxRecognizer()
            text = recognizer.recognize()
            words_list = keyword_recognition(text)
            obj = VariableDeclaration(words_list)
            file.write(obj.code)


root = Root()
root.mainloop()
