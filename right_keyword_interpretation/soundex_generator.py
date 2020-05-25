import fuzzy

soundex = fuzzy.Soundex(4)

list = ['def', 'is', 'variable', 'string', 'integer', 'float', 'list', 'Dictionary']


def soundex_generator(list):
    keywords_soundex = []
    for i in list:
        sound = soundex(i)
        keywords_soundex.append((i, 0.5, sound))
    return keywords_soundex


print(soundex_generator(list))
