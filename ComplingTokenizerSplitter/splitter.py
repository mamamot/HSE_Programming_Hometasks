import sys

FINAL_PUNCT = [".", "!", "?", "…", "\n"]
ACRONYMS = list()
EMPTY = ['', ' ', '\n', '\r\n']


def tokenize(text, twittermode, urlmode, makelower=True, include_whitespaces=False):
    # подготавливаем строку к обработке
    text = text.replace("\r\n", "\n")
    # список для хранения токенов
    tokens = list()
    # список для хранения символов, входящих в текущий токен
    buffer = list()
    # храним позицию в тексте
    position = 0
    # храним длину текста
    length = len(text)
    islinebreak = False
    # флаги для специальных случаев
    is_url = False
    is_tag = False
    is_mail = False
    for char in text:
        if char.isalnum():
            # если наш символ - просто буква или цифра, добавляем его в буфер
            buffer.append(char)
        elif char.isspace():
            # нам встретился пробельный символ
            if islinebreak:
                # это перенос слова
                islinebreak = False
                position += 1
                continue
            if len(buffer) > 0:
                # это пробел или новая строка после слова
                token = "".join(buffer)
                if is_url:
                    is_url = False
                elif is_tag:
                    is_tag = False
                elif is_mail:
                    is_mail = False
                else:
                    if makelower:
                        token = token.lower()
                tokens.append(token)
                buffer = list()
            if include_whitespaces:
                tokens.append(char)
        else:
            # нам встретился знак препинания
            if char == "-":
                # проверяем, не перенос ли это
                if len(buffer) > 0 and (length - position) > 1:
                    nextchar = text[position + 1]
                    if nextchar == "\n" and buffer[-1].isalpha():
                        islinebreak = True
                        position += 1
                        continue
                    elif nextchar.isalnum() and len(buffer) > 0:
                        buffer.append(char)
                        position += 1
                        continue
            if len(buffer) > 0:
                # это знак препинания после слова
                if char in [":", ".", "/"] and position < len(text) + 1:
                    if buffer[-1].isdigit() and text[position + 1].isalnum():
                        buffer.append(char)
                        position += 1
                        continue
                if urlmode and len(buffer) > 1:
                    # проверяем, не ссылка ли это
                    if "".join(buffer[0:2]) in ["ww", "ht"] and char in [".", "/", ":", "&", "?", "=", "-", "_", "@"]:
                        is_url = True
                        buffer.append(char)
                    # или почтовый адрес
                    elif char == "@":
                        is_mail = True
                        buffer.append(char)
                    elif is_mail:
                        if char in [".", "-", "_"]:
                            buffer.append(char)
                        else:
                            token = "".join(buffer)
                            buffer = list()
                            is_mail = False
                            tokens.append(token)
                            tokens.append(char)
                    else:
                        token = "".join(buffer)
                        if is_url:
                            is_url = False
                        elif is_tag:
                            is_tag = False
                        elif is_mail:
                            is_mail = False
                        else:
                            if makelower:
                                token = token.lower()
                        tokens.append(token)
                        tokens.append(char)
                        buffer = list()
                        # добавить распознавание (.), (:) и (/) для цифр и
                else:
                    token = "".join(buffer)
                    if is_url:
                        is_url = False
                    elif is_tag:
                        is_tag = False
                    elif is_mail:
                        is_mail = False
                    else:
                        if makelower:
                            token = token.lower()
                    tokens.append(token)
                    tokens.append(char)
                    buffer = list()
            else:
                if twittermode and char in ["@", "#"]:
                    is_tag = True
                    buffer.append(char)
                else:
                    tokens.append(char)
        if tokens[-3:] == [".", ".", "."]:
            # три точки подряд - явно троеточие
            tokens = tokens[:-3]
            tokens.append("…")
        position += 1
    return tokens


def load_acronyms(path):
    for ch in "АБВГДЕЖЗИКЛАМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        ACRONYMS.append(ch)
    f = open("acronyms.txt", "r", encoding="utf-8")
    for line in f:
        ACRONYMS.append(line.strip())


def split(text, twitter, url):
    load_acronyms("")
    text_tokenized = tokenize(text, twitter, url, False, True)
    pos = 0
    sentence_tokens = list()
    sentences = list()
    for token_pos in range(len(text_tokenized)):
        if text_tokenized[token_pos] in FINAL_PUNCT and token_pos > 0:
            if text_tokenized[token_pos - 1] not in ACRONYMS:
                if text_tokenized[token_pos] != "\n":
                    sentence_tokens.append(text_tokenized[token_pos])
                sentences.append("".join(sentence_tokens))
                sentence_tokens = list()
            else:
                sentence_tokens.append(text_tokenized[token_pos])
        else:
            sentence_tokens.append(text_tokenized[token_pos])
        pos += 1
    return sentences

if __name__ == "__main__":
    f = open(sys.argv[1], encoding="utf-8")
    if "-t" in sys.argv:
        twitter = True
    if "-u" in sys.argv:
        url = True
    splitted = split(f.read(), twitter, url)
    splitted = "\n".join([s.strip() for s in splitted if s not in EMPTY])
    f.close()
    f = open(sys.argv[2], "w", encoding="utf-8")
    f.write(splitted)
    f.close()


