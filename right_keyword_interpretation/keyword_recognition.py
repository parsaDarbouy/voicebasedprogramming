from right_keyword_interpretation.right_keyword import right_keyword


def keyword_recognition(string):
    words_list = string.split(" ")
    n = len(words_list)
    for i in range(n):
        word = right_keyword(words_list[i])
        words_list[i] = word
    return words_list
