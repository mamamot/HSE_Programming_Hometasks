import string


def load_text():
    return "СТЕЖИЦА, ж. Стежка, тропинка, дорожка. И шьдъ приидеши къ ст#намъ, яже суть от земл# " \
           "до %нбсе, и обрящеши стьжицю малу, и по стьжици тои идеши и обрящеши окъньце мало в ст#н#" \
           ". (Сказ. Агапия) Усп.сб., 469. XII–XIIIвв.\n"

letters = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
letters = letters + letters.upper() + " #%XVI" + string.digits

tr_table = {
    ("lemma", letters): "lemma",
    ("lemma", ","): "pos",
    ("pos", letters): "pos",
    ("pos", "."): "def",
    ("def", letters + ","): "def",
    ("def", "."): "example",
    ("example", letters + ","): "example",
    ("example", "."): "source",
    ("source", letters + ",.()"): "source",
    ("source", "\n"): "endstate"
}


def fsa(text):
    parsed = dict()
    state = "lemma"
    states = list(tr_table.keys())
    buffer = list()
    for c in text:
        transition_made = False
        if state is "failstate":
            break
        for s in states:
            if s[0] == state and c in s[1]:
                if tr_table[s] == state:
                    buffer.append(c)
                    transition_made = True
                    break
                else:
                    parsed[state] = "".join(buffer)
                    buffer = list()
                    transition_made = True
                    state = tr_table[s]
                    break
        if not transition_made:
            state = "failstate"
    return parsed


print(fsa(load_text()))
