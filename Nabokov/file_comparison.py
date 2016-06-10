import os
from lxml import etree


def merge_trees(path):
    root = etree.Element("html")
    head = etree.SubElement(root, "head")
    body = etree.SubElement(root, "body")
    para_counter = 0
    for file in os.listdir(path):
        try:
            with open(os.path.join(path, file), encoding="utf-8") as f:
                file_tree = etree.fromstring(f.read())
                for input_para in file_tree.iter('para'):
                    input_para.set('id', str(para_counter))
                    body.append(input_para)
                    para_counter += 1
        except Exception as e:
            print(e)
    return root


merged = merge_trees("Pnin/Pnin_iljin/")
with open("merged.xml", "wb") as w:
    w.write(etree.tostring(merged, method="html", pretty_print=True, encoding="utf-8"))
