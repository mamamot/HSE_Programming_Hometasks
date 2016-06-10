import os
from lxml import etree


def merge_trees(path):
    paras = list()
    para_counter = 0
    for file in os.listdir(path):
        try:
            with open(os.path.join(path, file), encoding="utf-8") as f:
                file_tree = etree.fromstring(f.read())
                for input_para in file_tree.iter('para'):
                    input_para.set('id', str(para_counter))
                    paras.append(input_para)
                    para_counter += 1
        except Exception as e:
            print(e)
    return paras


def load_model(path):
    paras = list()
    try:
        with open(path, encoding="utf-8") as f:
            tree = etree.fromstring(f.read())
            paras = list(tree.iter('para'))
    except Exception as e:
        print(e)
    return paras


merged = merge_trees("Pnin/Pnin_iljin/")
model = load_model("Pnin/pnin_barabtarlo.xml")
print(len(merged))
print(len(model))

