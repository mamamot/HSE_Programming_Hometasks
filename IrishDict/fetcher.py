# -*- coding=utf-8 -*-
import urllib.request
import os
__author__ = 'vtush'

SITE = "http://dil.ie/"
PAGES = 60
SAVE_PATH = "pages"
EXTENSION = "htm"


def fetch(site=SITE, page_number=PAGES):
    """
    Проецедура, скачивающая страницы в каталог для последующей обработки
    :param site: адрес сайта
    :param page_number: количество страниц
    """
    for n in range(1, page_number+1):
        try:
            url = urllib.request.urlopen(site + str(n))
            text = url.readall()
            f = open(os.path.join(".", SAVE_PATH, os.extsep.join([str(n), EXTENSION])), "w", encoding="utf-8")
            f.write(text.decode("utf-8"))
            f.close()
            print(str(n) + " fetched")
        except Exception as e:
            print("Ошибка скачивания: " + str(e))
