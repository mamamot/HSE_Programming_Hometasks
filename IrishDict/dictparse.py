# -*- coding=utf-8 -*-
import re
import os
__author__ = 'vtush'

headword_re = "<h3 headword_id=\"\d+\">(.+)</h3>"
forms_re = "<p class=\"small\">Forms:\s+(.+)</p>"
id_re = "<a class=\"reference\" href=\"(\d+)\">"

DIRECTORY = "pages"


def parse_page(text, f2l_dict):
    try:
        headword = re.findall(headword_re, text)[0]
        id = re.findall(id_re, text)[0]
        if re.search(forms_re, text):
            forms = re.findall(forms_re, text)[0].split(",")
        else:
            forms = [headword]
        for form in forms:
            f2l_dict[form.strip()] = [headword, id]
    except Exception as e:
        print("A necessary attribute was not found.")


def main():
    filenames = os.listdir(os.path.join(".", DIRECTORY))
    print(filenames)
    f2l_dict = dict()
    for filename in filenames:
        if filename.split(os.extsep)[-1] in ["htm", "html"]:
            print("Parsing file: " + filename)
            f = open(os.path.join(".", DIRECTORY, filename), "r", encoding="utf-8")
            parse_page(f.read(), f2l_dict)
            f.close()
        else:
            print("Wrong file type: " + filename)
    out = open("output.txt", "w", encoding="utf-8")
    out.write(str(f2l_dict))


if __name__ == '__main__':
    main()