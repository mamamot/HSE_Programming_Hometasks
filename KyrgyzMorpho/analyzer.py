import bz2
import json
import os
import nltk
import sys

def tokenize(text):
    return nltk.word_tokenize(text)


def parse_word(uinput):
    found = False
    longest = ""
    if len(uinput) > 3:
        affixes = list()
        for x in range(3, len(uinput)):
            affixes.append(uinput.lower()[x:])
        for affix in affixes[::-1]:
            if affix in data:
                found = True
                longest = affix
        if found:
            return uinput[:len(uinput) - len(longest)] + "+" + longest
        else:
            return uinput
    else:
        return uinput


if __name__=="__main__":
    print("Kyrgyz Super-Doooper Stemmer")
    try:
        with open("affixes.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("You have to provide the affix database as affixes.json or train your own model using learner.py")
        print(str(e))
        exit()
    if len(sys.argv) != 3:
        print("Usage: analyzer.py [inputfile] [outputfile]")
    else:
        if os.path.exists(sys.argv[1]):
            try:
                with open(sys.argv[1], encoding="utf-8") as f:
                    words = tokenize(f.read())
                result = "\n".join(map(parse_word, words))
                with open(sys.argv[2], "w", encoding="utf-8") as w:
                    w.write(result)
                print("Stemming done.")
            except Exception as e:
                print("Error parsing file: {}".format(str(e)))
        else:
            print("Usage: analyzer.py [inputfile] [outputfile]")

