# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import lxml.html
import urllib.request
import urllib.error
import urllib.parse
import pymorphy2
import json

morph = pymorphy2.MorphAnalyzer()

BIGRAM_LINK = "http://search.ruscorpora.ru/search.xml?env=sas1_2&mycorp=&mysent=&mysize=&mysentsize=" \
              "&dpp=100&spp=100&spd=100&text=lexgramm&mode=ngrams_2_lexgr&sort=gr_freq&lang=ru&nodia=1" \
              "&parent1=0&level1=0&lex1=&gramm1=V%2Ctran&flags1=&parent2=0&level2=0&min2=1&max2=1&lex2={0}" \
              "&gramm2=%28gen%7Cgen2%7Cdat%7Cacc%7Cacc2%7Cins%29&flags2="
TRIGRAM_LINK = "http://search.ruscorpora.ru/search.xml?env=sas1_2&mycorp=&mysent=&mysize=&mysentsize=" \
               "&dpp=100&spp=100&spd=100&text=lexgramm&mode=ngrams_3_lexgr&sort=gr_freq&lang=ru&nodia=1" \
               "&parent1=0&level1=0&lex1=&gramm1=V&flags1=&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2=" \
               "PR&flags2=&parent3=0&level3=0&min3=1&max3=1&lex3={0}&gramm3=&flags3="

agent_name = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            
            
# загрузка страниц
def load_page(url, encoding="cp1251"):
    """
    Простая функция для загрузки страницы с сайта

    :param url: URI of the page
    :param encoding: page encoding
    :return: tuple: a boolean showing success, content of the page (or error message), and http code if available (or 0)
    """
    try:
        req = urllib.request.Request(urllib.parse.quote(url, safe=":/&=?%"), headers={'User-Agent': agent_name})
        with urllib.request.urlopen(req) as r:
            code = r.getcode()
            page = r.read().decode(encoding)
            loaded = True
    except urllib.error.HTTPError as e:
        page = e.reason
        code = e.code
        loaded = False
    except urllib.error.URLError as e:
        page = e.reason
        code = 0
        loaded = False
    except Exception as e:
        page = str(e)
        code = 0
        loaded = False
    return loaded, page, code

def load_words():
    """
    Загрузка списка слов
    """
    with open("w1.txt", "r") as f:
        txt = f.read()
        words1 = txt.split("\n")
        words1 = [w.strip().lower() for w in words1]
    with open("w2.txt", "r") as f:
        txt = f.read()
        words2 = txt.split("\n")
        words2 = [w.strip().lower() for w in words2]
    words = set(words1 + words2)
    return words

def create_link(word, is_trigram=False):
    """
    Создает ссылки на страницы в соответствии с необходимым запросом
    """
    if is_trigram:
        return TRIGRAM_LINK.format(word)
    else:
        return BIGRAM_LINK.format(word)

def lemma(token, morph):
    parse = morph.parse(token)
    for p in parse:
        if 'VERB' in p.tag:
            return True, p.normal_form
    return False, ""

def extract_words_freqs(bi_page, tri_page):
    """
    Извлекает из текста страницы глаголы/глаголы с предлогами и возвращает в виде словаря, где глаголы - ключи, частоты - 
    значения.
    """
    output_dict = dict()
    bi_tree = lxml.html.fromstring(bi_page)
    # обходим таблицу на странице по строкам
    for tr in bi_tree.iter('tr'):
        # прямо в ячейках живут цифры (номер пп. и частотность)
        td_text = tr.xpath(".//td/text()")
        if not td_text:
            continue
        # в тегах span живут слова
        span_text = tr.xpath(".//td/span/text()")
        freq = int(td_text[1])
        token = span_text[0]
        is_verb, word = lemma(token, morph)
        if is_verb:
            if word in list(output_dict.keys()):
                output_dict[word] = output_dict[word] + freq
            else:
                output_dict[word] = freq
    tri_tree = lxml.html.fromstring(tri_page)
    # переходим к триграммам
    for tr in tri_tree.iter('tr'):
        td_text = tr.xpath(".//td/text()")
        if not td_text:
            continue
        # в тегах span живут слова
        span_text = tr.xpath(".//td/span/text()")
        freq = int(td_text[1])
        token = span_text[0]
        is_verb, word = lemma(token, morph)
        prep_phrase = word + " " + span_text[1]
        if is_verb:
            if prep_phrase in list(output_dict.keys()):
                output_dict[prep_phrase] = output_dict[prep_phrase] + freq
            else:
                output_dict[prep_phrase] = freq
    return output_dict

def loader(words):
    output_dict = dict()
    counter = 1
    for word in words:
        print("Dumping data for {0}.".format(word))
        bi_loaded, bi_page, code = load_page(create_link(word, False))
        tri_loaded, tri_page, code = load_page(create_link(word, True))
        if bi_loaded and tri_loaded:
            output_dict[word] = extract_words_freqs(bi_page, tri_page)
            print("[{0}] Completed.".format(str(counter)))
            counter += 1
    return output_dict

def dumper():
    print("Starting the job")
    words = list(load_words())
    print("Wordlist is loaded: {0} entries".format(str(len(words))))
    loaded = loader(words)
    with open("out.json", "w") as w:
        json.dump(loaded, w)
    return loaded
    
    