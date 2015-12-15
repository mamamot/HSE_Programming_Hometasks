# -*- coding: utf-8 -*-
import sys

__author__ = 'v. tushkanov'
CSVFILE = "transcription.csv"


def load_transcription(csvfile):
    """
    Загружает CSV-файл и возвращает словарь с соответствиями буква-звук
    :param csvfile: путь к файлу
    :return: словарь с соответствиями буква-звук.
    """
    try:
        f = open(csvfile, "r", encoding="utf-8")
        l2s_dict = dict()
        lines = f.read().split("\n")
        header = lines[0].split(",")
        for line in lines[1:]:
            line = line.split(",")
            for pos in range(1, len(header)):
                l2s_dict[line[pos]] = line[0] + header[pos]
        f.close()
        return l2s_dict
    except FileNotFoundError:
        print("Файл конфигурации не найден.")
        exit()
    except Exception as e:
        print("Ошибка загрузки конфигурации: " + str(e))
        exit()


def main(args):
    if len(args) < 3:
        print("Амхарский транскриптор!\nВведите название исходного файла и файла для вывода.")
    else:
        # загружаем соответствия букв и звуков
        l2s_dict = load_transcription(CSVFILE)
        try:
            # открываем исходный файл
            fsource = open(args[1], "r", encoding="utf-8")
            source = fsource.read()
            fsource.close()
            loutput = list()
            for letter in source:
                if letter in l2s_dict.keys():
                    loutput.append(l2s_dict[letter])
                elif letter in ",-:.":
                    # добавляем обозначение для пауз
                    loutput.append(" |")
                elif letter in " \n":
                    loutput.append(letter)
                else:
                    # мы пока игнорируем то, что не можем отпарсить, например, цифры
                    pass

            # сохраняем результат
            soutput = "".join(loutput)
            foutput = open(args[2], "w", encoding="utf-8")
            foutput.write(soutput)
            foutput.close()
            print("Транскрибирование завершено успешно!")
        except FileNotFoundError:
            print("Исходный файл не найден.")
        except Exception as e:
            print("Произошла ошибка: " + str(e))

if __name__ == '__main__':
    main(sys.argv)
