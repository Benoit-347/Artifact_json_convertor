#This program reads the json file returned from inventory kamera app and creates a csv file such that it is formated with artifact headings and rows as substats

import csv

#read the json file
with open ("1_data.json", "r") as file1:
    import json
    data = json.load(file1)
    list_of_dicts = data["artifacts"]

#to get the whole file heading
def get_keys():
    keys = []
    dict1 = list_of_dicts[0]
    for key in dict1:
        if key != 'substats':   #the substats are going to be put seperately for quality of life
            keys.append(key)
    return keys

#the main program to get each artifact's details and put substats into newlines 
def get_values():
    list_of_values = []   #to leave a line
    j = 0
    for dict1 in list_of_dicts:
        values = [dict1['setKey'], dict1['slotKey'], dict1['rarity'], dict1['mainStatKey'], dict1['level'], dict1['location'], dict1['lock'], dict1['id']]
        list_of_values.append(values)
        list_of_dict_of_substats = dict1["substats"]
        list_of_values.extend([[], ['key', 'value']])
        for i in list_of_dict_of_substats:
            a = [i['key'], i['value']]
            list_of_values.append(a)
        list_of_values.append("")
        j += 1
        print(f"{j}st iteration of get values")
    return list_of_values

#writing the formated data into a csv file
def write_to_csv():
    with open("data.csv", "w", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerow(get_keys())
        writer.writerows(get_values())

write_to_csv()