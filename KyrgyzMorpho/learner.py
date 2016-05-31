# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# encoding: utf-8
from nltk import word_tokenize
import json
import os


def create_candidates(word):
    affixes = list()
    if len(word) > 3:
        for x in range(3, len(word)):
            affixes.append(word[x:])
        #print(word + ":" + str(affixes))
        return affixes
    else:
        return list()


def parse(words, affixes, stems):
    for word in words:
        previous_count = 0
        previous_candidate = None
        for candidate in create_candidates(word):
            candidate_count = 0
            for word_check in words:
                if word_check.endswith(candidate):
                    candidate_count += 1
            if previous_count < candidate_count and (previous_candidate is not None):
                found = False
                for affix in affixes:
                    if affix.endswith(candidate):
                        if len(affix) > len(candidate):
                            if word.endswith(affix):
                                found = True
                                stems.add(word[0:len(word)-len(affix)])
                if found:
                    break
                if candidate in affixes:
                    affixes[candidate] += candidate_count
                else:
                    affixes[candidate] = candidate_count
                stems.add(word[0:len(word)-len(candidate)])
                break
            else:
                previous_count = candidate_count
                previous_candidate = candidate


def crawl(path="./pages"):
    affixes = dict()
    stems = set()
    counter = 1
    for d, dirs, files in os.walk(path):
        print("Total: " + str(len(files)))
        for f in files:
            with open(os.path.join(path, f), encoding="utf-8") as file:
                print(str(counter) + ". Parsing " + f)
                parse(tokenize(file.read()), affixes, stems)
                counter += 1
    return affixes, stems


def tokenize(text):
    return [w.strip("«»").lower() for w in word_tokenize(text)]


aff, stems = crawl("./pages")
print("Affixes collected: " + str(len(aff)))
with open("affixes.json", "w") as w:
    json.dump(aff, w)
