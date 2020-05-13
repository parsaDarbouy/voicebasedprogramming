import fuzzy
from difflib import SequenceMatcher

keyword_list = [("def", 0.5, "D1"), ('is', 0.5, "I2")]
soundex = fuzzy.Soundex(4)


def right_keyword(word):
    sound = soundex(word)
    for i in keyword_list:
        key_word = i[0]
        key_word_sound = i[2]
        ratio = SequenceMatcher(None, sound, key_word_sound).ratio()
        if ratio >= i[1]:
            return key_word
    return word
