from lxml import etree
import csv


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
                    # здесь общее количество разборо
                    variants_total = 0
                    word_count += 1
                    if word_count == 1:
                        sent_pos = 'bos'  # непонятно, что делать, если предложение из одного слова, пусть будет bos.
                    elif word_count == sent_len:
                        sent_pos = 'eos'
                    else:
                        sent_pos = ''
                    # нам нужно посчитать, сколько у нас разных лемм и найти само слово из текста
                    for ana in word.iter('ana'):
                        variants_total += 1
                        lemma = ana.get('lex')
                        if lemma not in lemmas:
                            lemmas.add(lemma)
                    else:
                        # собственно слово является хвостом последнего элемента ana.
                        word_entry = ana.tail.strip()
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
                            '#flex': "",
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
    except Exception as e:
        print("Error converting XML to PRS: {}".format(str(e)))


if __name__ == "__main__":
    xml2prs("example_corpus.xml", "test1.prs")
