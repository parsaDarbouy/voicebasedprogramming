import speech_recognition

from voice_recognition.exceptions import RecognizerException
from tkinter import messagebox


class GoogleRecognizer(object):
    def __init__(self, noise_adjust_duration=5):
        self.recognizer = speech_recognition.Recognizer()
        self.noise_adjust_duration = noise_adjust_duration
        self.current_result_text = ""

    def recognize(self):
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.noise_adjust_duration)
            messagebox.showinfo(message="speak now")
            audio = self.recognizer.listen(source)
        try:
            self.current_result_text = self.recognizer.recognize_google(audio)
        except speech_recognition.UnknownValueError:
            raise RecognizerException("Sorry! Could not understand what you said")
        except speech_recognition.RequestError:
            raise RecognizerException("Seems like we cannot connect to google at this time! Try again later")
        return self.current_result_text
