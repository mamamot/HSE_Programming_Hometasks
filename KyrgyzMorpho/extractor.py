# encoding: utf-8
# Написано на втором питоне, потому что приходилось одновременно отлаживать WikiExtractor.py, на втором же питоне
# написанный. Скрипт никаких файлов в итоге не создавал и бесславно завершался, плюясь Error'ами.  Была найдена точка,
# в которой он получает чистый текст статьи, в ней дописан кусок для сохранения этого текста в папку pages.

import os
import nltk
import codecs

def extract(file, path="./pages"):
    """
    Запускает WikiExtractor
    :param file: файл для передачи скрипту
    :param path: путь для сохранения результатов
    :return:
    """
    os.system("python ./wikiextractor/WikiExtractor.py --output {} --no-templates "
              "--escapedoc --processes 1 --debug {}".format(path, file))


if __name__ == "__main__":
    # список вероятного мусора
    token_stop_list = ["<", ">", "||", "*", "''", "``", "#"]
    extract("kywiki-20160501-pages-articles-multistream.xml")
    print("Files extracted")
