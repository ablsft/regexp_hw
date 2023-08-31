import csv
import re

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

names = []
for string in contacts_list:
    if string[0].count(' ') != 0:
        if string[0].count(' ') == 2:
            string[2] = string[0].split()[2]
        string[1] = string[0].split()[1]
        string[0] = string[0].split()[0]

    if string[1].count(' ') != 0:
        string[2] = string[1].split()[1]
        string[1] = string[1].split()[0]

    names.append((string[0], string[1]))

    pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[ (доб.]*(\d+)*\)*")  
    if 'доб' in string[5]:
        subst_pattern = r"+7(\2)\3-\4-\5 доб.\6"
        string[5] = pattern.sub(subst_pattern, string[5])
    else:
        subst_pattern = r"+7(\2)\3-\4-\5"
        string[5] = pattern.sub(subst_pattern, string[5])

repeated_names = {}
for index, name in enumerate(names):
    if names.count(name) > 1:
        if name not in repeated_names.keys():
            repeated_names.update({name: [index]})
        else:
            repeated_names[name] += [index]

for positions in sorted(repeated_names.values(), reverse=True):
    for position in sorted(positions[1:], reverse=True):
        for index, field in enumerate(contacts_list[positions[0]]):
            if not field:
                contacts_list[positions[0]][index] = contacts_list[position][index]
            
        contacts_list.pop(position)

with open('phonebook.csv', 'w', encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)