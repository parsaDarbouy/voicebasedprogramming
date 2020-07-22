import subprocess

from voice_recognition.recognizers import GoogleRecognizer, SphinxRecognizer
from right_keyword_interpretation.keyword_recognition import keyword_recognition
from grammar.command_to_code import CommandToCode

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        self.filename = ""
        self.recognizer = GoogleRecognizer()
        self.code_converter = CommandToCode()
        self.indent = 0
        self.indent_phrases = ["if condition", "define function"]
        self.revert_indent_phrases = ["end of if", "end of function"]

        self.geometry("1920x1051+650+150")
        self.title("Voice-Based Programming")
        self.configure(background="#374046")
        self.attributes('-fullscreen', True)

        self.open_file = Button()
        self.open_file.place(relx=0.057, rely=0.447, height=133, width=486)
        self.open_file.configure(activebackground="#ff9100")
        self.open_file.configure(activeforeground="#000000")
        self.open_file.configure(background="#ff9100")
        self.open_file.configure(disabledforeground="#bfbfbf")
        self.open_file.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.open_file.configure(foreground="#ffffff")
        self.open_file.configure(highlightbackground="#ffffff")
        self.open_file.configure(highlightcolor="black")
        self.open_file.configure(pady="0")
        self.open_file.configure(relief="flat")
        self.open_file.configure(text='''Open Current File''')
        self.open_file.configure(command=self.open_current_file)

        self.select_file = Button()
        self.select_file.place(relx=0.057, rely=0.609, height=133, width=486)
        self.select_file.configure(activebackground="#ff9100")
        self.select_file.configure(activeforeground="#000000")
        self.select_file.configure(background="#ff9100")
        self.select_file.configure(disabledforeground="#bfbfbf")
        self.select_file.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.select_file.configure(foreground="#ffffff")
        self.select_file.configure(highlightbackground="#ffffff")
        self.select_file.configure(highlightcolor="black")
        self.select_file.configure(pady="0")
        self.select_file.configure(relief="flat")
        self.select_file.configure(text='''Select New File''')
        self.select_file.configure(command=self.select_new_file)

        self.exit = Button()
        self.exit.place(relx=0.057, rely=0.771, height=133, width=486)
        self.exit.configure(activebackground="#ff9100")
        self.exit.configure(activeforeground="#000000")
        self.exit.configure(background="#ff9100")
        self.exit.configure(disabledforeground="#bfbfbf")
        self.exit.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.exit.configure(foreground="#ffffff")
        self.exit.configure(highlightbackground="#ffffff")
        self.exit.configure(highlightcolor="black")
        self.exit.configure(pady="0")
        self.exit.configure(relief="flat")
        self.exit.configure(text='''Exit''')
        self.exit.configure(command=self.end_program)

        self.listen = Button()
        self.listen.place(relx=0.057, rely=0.095, height=133, width=486)
        self.listen.configure(activebackground="#ff9100")
        self.listen.configure(activeforeground="#000000")
        self.listen.configure(background="#ff9100")
        self.listen.configure(disabledforeground="#bfbfbf")
        self.listen.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.listen.configure(foreground="#ffffff")
        self.listen.configure(highlightbackground="#ffffff")
        self.listen.configure(highlightcolor="black")
        self.listen.configure(pady="0")
        self.listen.configure(relief="flat")
        self.listen.configure(text='''Start Listening...''')
        self.listen.configure(command=self.listen_and_generate_code)

        self.Scrolledtext = scrolledtext.ScrolledText()
        self.Scrolledtext.place(relx=0.496, rely=0.133, relheight=0.772, relwidth=0.467)
        self.Scrolledtext.configure(background="white")
        self.Scrolledtext.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Scrolledtext.configure(foreground="black")
        self.Scrolledtext.configure(highlightbackground="#ffffff")
        self.Scrolledtext.configure(highlightcolor="black")
        self.Scrolledtext.configure(insertbackground="black")
        self.Scrolledtext.configure(insertborderwidth="3")
        self.Scrolledtext.configure(selectbackground="blue")
        self.Scrolledtext.configure(selectforeground="white")
        self.Scrolledtext.configure(wrap="none")
        self.Scrolledtext.configure(state=DISABLED)

        self.t_separator1 = ttk.Separator()
        self.t_separator1.place(relx=0.435, rely=0.048, relheight=0.905)
        self.t_separator1.configure(orient="vertical")

        self.t_separator2 = ttk.Separator()
        self.t_separator2.place(relx=0.061, rely=0.39, relwidth=0.302)

        self.label1 = Label()
        self.label1.place(relx=0.057, rely=0.257, height=75, width=482)
        self.label1.configure(background="#374046")
        self.label1.configure(disabledforeground="#bfbfbf")
        self.label1.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.label1.configure(foreground="#ff8a65")
        self.label1.configure(text='''Do Not Speak...''')
        self.recognizer.set_speak_notify_targets([self.label1])

        self.label2 = Label()
        self.label2.place(relx=0.461, rely=0.057, height=46, width=802)
        self.label2.configure(background="#374046")
        self.label2.configure(disabledforeground="#bfbfbf")
        self.label2.configure(
            font="-family {JetBrains Mono} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
        self.label2.configure(foreground="#ffffff")
        self.label2.configure(text='''See Your Code Here''')

    def listen_and_generate_code(self):
        if self.filename:
            text = self.recognizer.recognize()
            words_list = keyword_recognition(text)
            print(text)
            if words_list[0].lower() == "remove" and words_list[1].lower() == "line":
                line_number = int(words_list[2])
                temp_file = open(self.filename, "r+")
                lines = temp_file.readlines()
                lines.pop(line_number - 1)
                temp_file.truncate(0)
                temp_file.writelines(lines)
                temp_file.close()
                self.Scrolledtext.configure(state=NORMAL)
                self.Scrolledtext.delete('1.0', END)
                self.Scrolledtext.insert('end', '\n'.join(lines))
                self.Scrolledtext.configure(state=DISABLED)
                return

            self.code_converter.set_command(words_list)
            if ' '.join(words_list[-3:]) in self.revert_indent_phrases and self.indent - 1 >= 0:
                self.indent -= 1

            with open(self.filename, "a") as file:
                generated_code = (self.indent * '\t') + self.code_converter.generate_code() + "\n"
                file.write(generated_code)
                self.Scrolledtext.configure(state=NORMAL)
                self.Scrolledtext.insert('end', generated_code)
                self.Scrolledtext.configure(state=DISABLED)

            if ' '.join(words_list[:2]) in self.indent_phrases:
                self.indent += 1

    def select_new_file(self):
        self.filename = filedialog.askopenfilename(title="Please choose a file", parent=self)
        with open(self.filename, 'r') as file:
            self.Scrolledtext.configure(state=NORMAL)
            self.Scrolledtext.insert('end', file.read())
            self.Scrolledtext.configure(state=DISABLED)

    def open_current_file(self):
        if self.filename:
            subprocess.run(['open', self.filename], check=True)

    def end_program(self):
        self.destroy()


root = Root()
root.mainloop()
