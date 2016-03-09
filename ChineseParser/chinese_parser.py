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

html = etree.Element("html")
head = etree.SubElement(html, "head")
body = etree.SubElement(html, "body")
for sentence in sentences("stal.xml"):
    print("Analyzing sentence: {}".format(sentence))
    se = etree.SubElement(body, "se")
    window = len(sentence)
    print(window)
    last_w = None
    while window > 0:
        if sentence[0:window] in parsed_dict:
            word = sentence[0:window]
            print("Analyzing: {}".format(word))
            w = etree.SubElement(se, "w")
            last_w = w
            for ana in parsed_dict[word]:
                ana = etree.SubElement(w, "ana", lex=word, sem=ana['sem'], transcr=ana['transcr'])
                last_ana = ana
            last_ana.tail = word
            sentence = sentence[window:]
            window = len(sentence)
            continue
        else:
            print("Not match: {} len {}".format(sentence[0:window], window))
            window -= 1
        if window == 0:
            if last_w is not None:
                last_w.tail = sentence[0:1]
            else:
                if se.text is not None:
                    se.text += sentence[0:1]
                else:
                    se.text = sentence[0:1]
            sentence = sentence[1:]
            window = len(sentence)

with open("out.xml", "w", encoding="utf-8") as f:
    f.write(etree.tostring(html, encoding="utf-8", xml_declaration=True, pretty_print=True).decode("utf-8"))



