import bz2
import json

if __name__=="__main__":
    print("Kyrgyz Super-Doooper Stemmer")
    try:
        with open("affixes.json", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("You have to provide the affix database as affixes.json or train your own model using learner.py")
        exit()
    while True:
        uinput = input(print("Enter a word or q to quit: ")).strip()
        if uinput == "q":
            exit()
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
                print(uinput[:len(uinput)-len(longest)] + "+" + longest)
            else:
                print(uinput)
        else:
            print(uinput)

