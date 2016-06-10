from lxml import etree
import csv
import os
import sys


def xml2prs(xml_filename, prs_filename):
    try:
        with open(xml_filename, encoding="utf-8") as f:
            data = list()
            # загружаем xml
            tree = etree.fromstring(f.read())
            sentence_count = 0
            for sentence in tree.iter('se'):
                word_count = 0
                sentence_count += 1
                # грязный способ узнать, сколько у нас предложений
                sent_len = len(list(tree.iter('se')))
                for word in sentence.iter('w'):
                    # узнаем пунктуацию справа
                    if word.tail:
                        punctr = word.tail.strip(" \t")
                    else:
                        punctr = ""
                    lemmas = set()
                    # здесь мы храним номер варианта, на котором мы сейчас
                    variant_count = 0
                    # здесь общее количество разборов
                    variants_total = 0
                    word_count += 1
                    if word_count == sent_len:
                        sent_pos = 'eos'   # непонятно, что делать, если предложение из одного слова, пусть будет eos
                    elif word_count == 1:  # так как это упрощает обратный парсинг
                        sent_pos = 'bos'
                    else:
                        sent_pos = ''
                    # нам нужно посчитать, сколько у нас разных лемм и найти само слово из текста
                    ana = None
                    for ana in word.iter('ana'):
                        variants_total += 1
                        lemma = ana.get('lex')
                        if lemma not in lemmas:
                            lemmas.add(lemma)
                    else:
                        # собственно слово является хвостом последнего элемента ana.
                        if ana is not None:
                            word_entry = ana.tail.strip()
                        else:
                            word_entry = ""
                    # капитализация
                    if word_entry[0].isupper():
                        cap = "cap"
                    else:
                        cap = ""
                    # количество лемм
                    lemma_count = len(lemmas)
                    for ana in word.iter('ana'):
                        variant_count += 1
                        grammar = ana.get('gr')
                        # разбиваем грамматический тег
                        if "," in grammar:
                            pos, grammar_tag = grammar.split(",", 1)
                        else:
                            pos = grammar
                            grammar_tag = ""
                        entry = {
                            '#sentno': sentence_count,
                            '#wordno': word_count,
                            '#lang': "",
                            '#graph': cap,
                            '#word': word_entry,
                            '#indexword': "",
                            '#nvars': variants_total,
                            '#lems': lemma_count,
                            '#nvar': variant_count,
                            '#lem': ana.get('lex'),
                            '#trans': ana.get('trans'),
                            '#trans_ru': "",
                            '#lex': pos,
                            '#gram': grammar_tag.upper(), # нужно больше информации о номенклатуре тегов
                            '#flex': ana.get('morph'),
                            '#punctl': "",
                            '#punctr': punctr.strip(),
                            '#sent_pos': sent_pos
                        }
                        data.append(entry)

        with open(prs_filename, "w", encoding="utf-8", newline="") as w:
            fieldnames = ('#sentno', '#wordno', '#lang', '#graph', '#word', '#indexword', '#nvars', '#lems', '#nvar',
                          '#lem', '#trans', '#trans_ru', '#lex', '#gram', '#flex', '#punctl', '#punctr', '#sent_pos')
            writer = csv.DictWriter(w, fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(data)
        print("Converting done.")
    except Exception as e:
        print("Error converting XML to PRS: {}".format(str(e)))


def prs2xml(prs_filename, xml_filename):
    try:
        root = etree.Element("body")
        with open(prs_filename, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row['#wordno'] == '1' and row['#nvar'] == '1':
                    se = etree.SubElement(root, "se")
                if row['#nvar'] == '1':
                    word = etree.SubElement(se, "word")
                ana = etree.SubElement(word, "ana")
                ana.set("lex", row['#lem'])
                ana.set("morph", row['#flex'])
                ana.set("gr", ",".join([row['#lex'], row['#gram']]))
                if row['#nvar'] == row['#nvars']:
                    ana.tail = row["#word"]
                    word.tail = row['#punctr']
        with open(xml_filename, "wb") as w:
            # Pretty printing (or formatting) an XML document means adding white space to the content.
            # These modifications are harmless if they only impact elements in the document that do not
            # carry (text) data. They corrupt your data if they impact elements that contain data. If
            # lxml cannot distinguish between whitespace and data, it will not alter your data.
            # Поэтому при чтении красивого xml приходилось обрабатывать его strip'ами
            w.write(etree.tostring(root, pretty_print=True, encoding="utf-8"))
        print("Converting done.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("Welcome to the XML2PRS (and vice versa) converter!")
    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        if os.path.isfile(infile):
            # не обязательно заставлять пользователя указывать направление конвертации -
            # его можно угадать по расширению источника
            if os.path.splitext(infile)[1].lower() == ".xml":
                xml2prs(infile, outfile)
            elif os.path.splitext(infile)[1].lower() == ".prs":
                prs2xml(infile, outfile)
            else:
                print("Incorrect input file extension. Only XML and PRS are supported.")
        else:
            print("Input file does not exist.")
    else:
        print("Usage: python xml2prs.py [inputfile] [outputfile]")
