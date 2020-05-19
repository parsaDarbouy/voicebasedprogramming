import fuzzy
from difflib import SequenceMatcher

keyword_list = [('def', 0.5, 'D1'), ('is', 0.5, 'I2'), ('variable', 0.5, 'V614'), ('string', 0.5, 'S365'),
                ('integer', 0.5, 'I532'), ('float', 0.5, 'F432'), ('list', 0.5, 'L232'), ('Dictionary', 0.5, 'D235')]

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
