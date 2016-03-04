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


def load_files(filenames):
    """
    Строит словарь, в котором ключ - название файла, а значение - список токенов
    :param filenames: пути к файлам
    :return:
    """
    doc_count = 0
    token_count = 0
    texts_tokens = dict()
    newline = 0
    c = 1
    print "Initializing the collection:"
    for filename in filenames:
        print ".",
        if newline == 50:
            print 50 * c
            newline = 0
            c += 1
        else:
            newline += 1
        file = codecs.open(filename, encoding="utf-8")
        doc_count += 1
        text = file.read()
        tokens = nltk.word_tokenize(text)
        texts_tokens[filename] = []
        for token in tokens:
            texts_tokens[filename].append(token)
            token_count += 1
        file.close()
    print()
    print("Loading done. A corpus of {0} tokens in {1} documents built.".format(token_count, doc_count))
    return texts_tokens


def build_freq_list(tokens):
    """
    Возвращает словарь, в котором ключ - токен, а значение - его частота
    :param tokens: словарь ключ: список токенов
    :return:
    """
    freq_list = dict()
    for file in tokens:
        for token in tokens[file]:
            if token in freq_list:
                freq_list[token] += 1
            else:
                freq_list[token] = 1
    return freq_list


def inverse_histogram(freq_list):
    """
    Строит инвертированную гистограмму - словарь, где ключ - частота,
    а значение - список лемм
    :param freq_list:
    :return:
    """
    hist = dict()
    for token in freq_list:
        freq = freq_list[token]
        if freq in hist:
            hist[freq].append(token)
        else:
            hist[freq] = [token]
    return hist


def get_filenames(path):
    """
    Получает названия всех файлов в директории (рекурсивно)
    :param path:
    :return:
    """
    fnames = list()
    for d, dirs, files in os.walk(path):
        for f in files:
            fnames.append(os.path.join(d, f))
    return fnames

if __name__ == "__main__":
    # список вероятного мусора
    token_stop_list = ["<", ">", "||", "*", "''", "``", "#"]
    extract("iswiki-20160203-pages-articles.xml.bz2")
    print "Files extracted"
    files = get_filenames("pages")
    print "Filenames retrieved"
    filetokens = load_files(files)
    print "Files loaded"
    freqlist = build_freq_list(filetokens)
    print "Frequency list built"
    hist = inverse_histogram(freqlist)
    print "Inverse histogram built"
    freqs = hist.keys()
    freqs.sort(reverse=True)
    lines = ["token\tfrequency"]
    for freq in freqs:
        for token in hist[freq]:
            if token not in token_stop_list and not(token.startswith("=")):
                lines.append(token + "\t" + unicode(freq))
    print "Output formed"
    with codecs.open("freqlist.tsv", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print "Job done"
