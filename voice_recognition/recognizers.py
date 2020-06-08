import speech_recognition


class SphinxRecognizer(object):
    def __init__(self, noise_adjust_duration=5):
        self.recognizer = speech_recognition.Recognizer()
        self.noise_adjust_duration = noise_adjust_duration
        self.current_result_text = ""

    def recognize(self):
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.noise_adjust_duration)
            audio = self.recognizer.listen(source)
        try:
            self.current_result_text = self.recognizer.recognize_google(audio)
        except speech_recognition.UnknownValueError as e:
            raise e
        except speech_recognition.RequestError as e:
            raise e
        return self.current_result_text
