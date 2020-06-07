from right_keyword_interpretation.right_keyword import right_keyword

keyword_list = [('variable', 0.5, 'V614'), ('define', 0.5, 'D155')]

variable_declaration = {('is', 0.6, 'I2')}
variable_type = {('string', 0.6, 'S365'),
                 ('integer', 0.6, 'I532'), ('float', 0.6, 'F432'), ('list', 0.6, 'L232'), ('Dictionary', 0.6, 'D235')}

define_function = [('function', 0.5, 'F523')]
parameters = [('parameters', 0.7, 'P653')]
next_or_end_parameter = [('next', 0.6, 'N233'), ('end', 0.5, 'E533')]
end_of = [('of', 0.5, 'O133')]


def keyword_recognition(string):
    case_0 = -1
    case_1 = -1
    words_list = string.split(" ")
    n = len(words_list)
    answer = []
    index = 0
    while index < n:
        word = words_list[index]
        if case_0 == -1:
            word = right_keyword(word, keyword_list)
            if word == "variable":
                case_0 = 0

            elif word == 'define':
                print(index)
                answer = answer + [word]
                index = index + 1
                print(index)
                word = words_list[index]
                word = right_keyword(word, define_function)
                if word == 'function':
                    case_0 = 1

        elif case_0 == 0:
            if case_1 == -1:
                word = right_keyword(word, variable_declaration)
                if word == "is":
                    case_1 = 0

            elif case_1 == 0:
                word = right_keyword(word, variable_type)
                if word in ['string', 'integer', 'float', 'list', 'Dictionary']:
                    case_1 = 1

        elif case_0 == 1:
            if case_1 == -1:
                word = right_keyword(word, parameters)
                if word == 'parameters':
                    case_1 = 0
            elif case_1 == 0:
                word = right_keyword(word, next_or_end_parameter)
                if word == 'end':
                    answer = answer + [word]
                    index = index + 1
                    print(index)
                    word = words_list[index]
                    word = right_keyword(word, end_of)
                    if word != 'of':
                        answer = answer + [word]
                        pass
                    else:  # 'of' has been founded, now 'parameters' has to be found
                        answer = answer + [word]
                        index = index + 1
                        print(index)
                        word = words_list[index]
                        word = right_keyword(word, parameters)
                        answer = answer + [word]
                        break
        index = index + 1
        print(index)
        answer = answer + [word]

    return answer


