# encoding: utf-8
import sys
import io

__author__ = 'vtush'

twitter = False
url = False
makelower = True


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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Welcome to AKVA Tokenizer (Awesome Ksusha, Vlad and Albert's Tokenizer)!\n"
              "Please provide the paths to the source and output files.\n"
              "\n"
              "Supported arguments:\n"
              "-t - Twitter tag detection\n"
              "-u - advanced url and e-mail detection\n"
              "-c - preserve upper and lower case")
    else:
        try:
            f = open(sys.argv[1], "r", encoding="utf-8")
            print("Tokenization started")
            if "-t" in sys.argv:
                twitter = True
            if "-u" in sys.argv:
                url = True
            if "-c" in sys.argv:
                makelower = False
            tokenized = tokenize(f.read(), twitter, url, makelower)
            #print(tokenized)
            f.close()
            f = open(sys.argv[2], "w", encoding="utf-8")
            f.write("\n".join(tokenized))
            print("Here3")
            f.close()
            print("Tokenization completed")
        except Exception as e:
            print("An error occurred during tokenization. Please, double-check the arguments.")
            print(str(e))
