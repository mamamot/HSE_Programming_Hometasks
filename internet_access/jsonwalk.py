import json
import os

PATH = "dump"

fs = list()

for root, dirs, files in os.walk(PATH):
    print(root, dirs, files)
    if files and files[0] != "info.csv":
        month = os.path.split(root)[1]
        year = os.path.split(root)[0].split("\\")[1]
        year_found = False
        for y in fs:
            if y['year'] == year:
                year_found = True
                if 'months' in list(y.keys()):
                    y['months'][month] = files
                else:
                    y['months'] = dict()
                    y['months'][month] = files
        if not year_found:
            y_dict = dict()
            y_dict['year'] = year
            y_dict['months'] = dict()
            fs.append(y_dict)

print(fs)

f = open("struct.json", "w", encoding="utf-8")
json.dump(fs, f, ensure_ascii=False, indent=2)
f.close()
