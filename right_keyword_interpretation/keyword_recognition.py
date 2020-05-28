from right_keyword_interpretation.right_keyword import right_keyword

keyword_list = [('def', 0.5, 'D1'), ('variable', 0.5, 'V614')]

variable_declaration = {('is', 0.6, 'I2')}
variable_type = {('string', 0.6, 'S365'),
                 ('integer', 0.6, 'I532'), ('float', 0.6, 'F432'), ('list', 0.6, 'L232'), ('Dictionary', 0.6, 'D235')}


def keyword_recognition(string):
    case_0 = -1
    case_1 = -1
    words_list = string.split(" ")
    n = len(words_list)
    answer = []
    for i in range(n):
        word = words_list[i]
        if case_0 == -1:
            word = right_keyword(word, keyword_list)
            if word == "variable":
                case_0 = 0

        elif case_0 == 0:
            if case_1 == -1:
                word = right_keyword(word, variable_declaration)
                if word == "is":
                    case_1 = 0

            elif case_1 == 0:
                word = right_keyword(word, variable_type)
                if word in ['string', 'integer', 'float', 'list', 'Dictionary']:
                    case_1 = 1

        answer = answer + [word]

    return answer
