# encoding: utf-8
__author__ = 'vtush'

twitter = False
url = False


def tokenize(text, twittermode, urlmode):
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
                    token = token.lower()
                tokens.append(token)
                buffer = list()
        else:
            # нам встретился знак препинания
            if char == "-":
                # проверяем, не перенос ли это
                if len(buffer) > 1 and (length - position) > 1:
                    nextchar = text[position + 1]
                    if nextchar == "\n" and buffer[-1].isalpha():
                        islinebreak = True
                        position += 1
                        continue
                    elif nextchar.isalpha() and len(buffer) > 0:
                        buffer.append(char)
                        position += 1
                        continue
            if len(buffer) > 0:
                # это знак препинания после слова
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
                            token = token.lower()
                        tokens.append(token)
                        tokens.append(char)
                        buffer = list()
                else:
                    token = "".join(buffer)
                    if is_url:
                        is_url = False
                    elif is_tag:
                        is_tag = False
                    elif is_mail:
                        is_mail = False
                    else:
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
        position += 1
    return tokens

f = open("tokenizeme.txt", encoding="utf-8")
print(tokenize(f.read(), True, True))