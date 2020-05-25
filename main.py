import sublime_plugin
from voice_recognition.recognizers import SphinxRecognizer
from right_keyword_interpretation.keyword_recognition import keyword_recognition
from grammar.variable_declaration import VariableDeclaration


class Main(sublime_plugin.TextCommand):
    def run(self, edit):
        file = open("/Users/parsasina/Documents/school/soft 1/project/test.py", "a")
        recognizer = SphinxRecognizer()
        text = recognizer.recognize()
        words_list = keyword_recognition(text)
        obj = VariableDeclaration(words_list)
        file.write(obj.code)
