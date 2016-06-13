import os
import sys
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
                    # fix the common uk-en error
                    for se in input_para.iter("se"):
                        if se.get("lang") == "uk":
                            se.set("lang", "en")
                    paras.append(input_para)
                    para_counter += 1
        except Exception as e:
            print("Error loading corrupted files: " + str(e))
    return paras


def load_model(path):
    paras = list()
    try:
        with open(path, encoding="utf-8") as f:
            tree = etree.fromstring(f.read())
            paras = list(tree.iter('para'))
    except Exception as e:
        print("Error loading model " + str(e))
    return paras


def compare_and_fix(model, bad):
    counter = 1
    print("Correction phase 1 commencing.")
    for x in range(1, len(model)-1):
        print(x, end=" ", flush=True)
        for y in range(1, len(bad)-1):
            if model[x-1].xpath(".//se[@lang='en']/text()") == bad[y-1].xpath(".//se[@lang='en']/text()") and \
                            model[x+1].xpath(".//se[@lang='en']/text()") == bad[y+1].xpath(".//se[@lang='en']/text()"):
                if model[x].xpath(".//se[@lang='en']/text()") != bad[y].xpath(".//se[@lang='en']/text()"):
                    print()
                    print("{}. Found error".format(counter))
                    print(model[x].xpath(".//se[@lang='en']/text()")[0])
                    print(bad[y].xpath(".//se[@lang='en']/text()")[0])
                    print()
                    old_index = bad[y].get("id")
                    bad[y] = model[x]
                    bad[y].set("id", old_index)
                    counter += 1
                    break
    print()
    print("Correction phase 2 commencing.")
    for x in range(1, len(model) - 2):
        print(x, end=" ", flush=True)
        for y in range(1, len(bad) - 2):
            if model[x - 1].xpath(".//se[@lang='en']/text()") == bad[y - 1].xpath(".//se[@lang='en']/text()") and \
                            model[x + 2].xpath(".//se[@lang='en']/text()") == bad[y + 2].xpath(
                        ".//se[@lang='en']/text()"):
                if model[x].xpath(".//se[@lang='en']/text()") != bad[y].xpath(".//se[@lang='en']/text()"):
                    print()
                    print("{}. Found error".format(counter))
                    print(model[x].xpath(".//se[@lang='en']/text()")[0])
                    print(bad[y].xpath(".//se[@lang='en']/text()")[0])
                    print()
                    old_index = bad[y].get("id")
                    bad[y] = model[x]
                    bad[y].set("id", old_index)
                    counter += 1
                    break
    print()
    print("Correction phase 3 commencing.")
    for x in range(1, len(model) - 3):
        print(x, end=" ", flush=True)
        for y in range(1, len(bad) - 3):
            if model[x - 1].xpath(".//se[@lang='en']/text()") == bad[y - 1].xpath(".//se[@lang='en']/text()") and \
                            model[x + 3].xpath(".//se[@lang='en']/text()") == bad[y + 3].xpath(
                        ".//se[@lang='en']/text()"):
                if model[x].xpath(".//se[@lang='en']/text()") != bad[y].xpath(".//se[@lang='en']/text()"):
                    print()
                    print("{}. Found error".format(counter))
                    print(model[x].xpath(".//se[@lang='en']/text()")[0])
                    print(bad[y].xpath(".//se[@lang='en']/text()")[0])
                    print()
                    old_index = bad[y].get("id")
                    bad[y] = model[x]
                    bad[y].set("id", old_index)
                    counter += 1
                    break
    return build_output_tree(bad)


def build_output_tree(para_list):
    print("Comparison done. Building output of lenght ".format(len(para_list)))
    root = etree.Element("html")
    head = etree.SubElement(root, "head")
    body = etree.SubElement(root, "body")
    for para in para_list:
        body.append(para)
    return etree.tostring(root, method="html", encoding="utf-8", pretty_print=True)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        model_path = sys.argv[1]
        bad_path = sys.argv[2]
        merged = merge_trees(bad_path)
        model = load_model(model_path)
        fixed = compare_and_fix(model, merged)
        try:
            with open(sys.argv[3], "wb") as w:
                w.write(fixed)
        except Exception as e:
            print("Error writing output: " + str(e))
    else:
        print("Usage: file_comparison.py [model_file] [corrupted_path] [output_file]")
