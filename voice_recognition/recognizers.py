import speech_recognition
from word2number import w2n


class SphinxRecognizer(object):
    def __init__(self, noise_adjust_duration=5, *args, **kwargs):
        self.recognizer = speech_recognition.Recognizer()
        self.noise_adjust_duration = noise_adjust_duration
        self.current_result_text = ""

    def recognize(self, digit_allowed=False, *args, **kwargs):
        with speech_recognition.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.noise_adjust_duration)
            print('fuck u')
            audio = self.recognizer.listen(source)
        try:
            self.current_result_text = self.recognizer.recognize_google(audio)
        except speech_recognition.UnknownValueError as e:
            raise e
        except speech_recognition.RequestError as e:
            raise e
        if digit_allowed:
            self.__convert_text_number_to_digit()
        return self.current_result_text

    def __convert_text_number_to_digit(self):
        text = self.current_result_text
        words = text.split()
        length = len(words)
        i = 0
        result_status, result = False, None
        while i < length:
            for j in range(i, length):
                try:
                    self.__is_valid_number_pattern(words[i: j + 1])
                    result = w2n.word_to_num(" ".join(words[i:j + 1]))
                    result_status = True
                    if j == length - 1:
                        text = text.replace(" ".join(words[i:j + 1]), str(result))
                        i = j + 1
                        break
                except ValueError:
                    if result_status:
                        text = text.replace(" ".join(words[i:j]), str(result))
                        result_status = False
                        i = j
                    else:
                        i += 1
                    break

        self.current_result_text = text

    @staticmethod
    def __is_valid_number_pattern(lst):
        for element in lst:
            if element not in w2n.american_number_system:
                raise ValueError


