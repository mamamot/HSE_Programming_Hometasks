import re
import lxml.html
import json
from lxml import etree

def dict_parse(dictfile, json_path=None):
    """
    Парсинг файла китайского словаря

    Получает на вход file object, на выходе - словарь следующей структуры:
    {
    иероглиф: [{значение: значение1, произношение: произношение1}, {...}]
    }
    :param dictfile:
    :param json_path: если задана строка, сохраняет по указанному адресу
    :return:
    """
    parsed = dict()
    for line in dictfile:
        if not line.startswith("#"):
            not_definition = line.split(" /")[0]
            #if len(not_definition) > 30: print(not_definition)
            pronunciation = re.findall("\[(.*?)\]", not_definition)[0]
            #if len(pronunciation) > 10: print(pronunciation)
            new_orth = re.findall("^.+\s(.*?)\s\[", not_definition)[0]
            definition = re.findall("\]\s(/.+)", line)[0].strip("/").replace(" ", "_").replace("/", ", ")
            if new_orth in parsed:
                parsed[new_orth].append({'transcr': pronunciation, 'sem': definition})
            else:
                parsed[new_orth] = [{'transcr': pronunciation, 'sem': definition}]
    if json_path:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f)
    return parsed


def sentences(path):
    with open(path, "r", encoding="utf-8") as f:
        tree = lxml.html.fromstring(f.read())
        for se in tree.xpath(".//se/text()"):
            yield se

with open("cedict_ts.u8", "r", encoding="utf-8") as f:
    parsed_dict = dict_parse(f)

words = list()
root = etree.Element("xml")
html = etree.SubElement(root, "html")
head = etree.SubElement(root, "head")
body = etree.SubElement(html, "body")
for sentence in sentences("stal.xml"):
    se = etree.SubElement(body, "se")
    window = len(sentence)
    while window > 1:
        if se[0, window] in parsed_dict:
            break
    else:
        pass



