import csv

with open ("1_data.json", "r") as file1:
    import json
    data = json.load(file1)
    list_of_dicts = [data["artifacts"][0]]

def get_keys():
    keys = []
    dict1 = list_of_dicts[0]
    for key in dict1:
        if key != 'substats':
            keys.append(key)
    return keys

def get_values():
    list_of_values = []
    i = 0
    for dict1 in list_of_dicts:
        values = [dict1['setKey'], dict1['slotKey'], dict1['rarity'], dict1['mainStatKey'], dict1['level'], dict1['location'], dict1['lock'], dict1['id']]
        list_of_values.append(values)
        i += 1
        print(f"{i}st iteration of get values")
    return list_of_values

def write_to_csv():
    with open("data.csv", "w", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerow(get_keys())
        writer.writerows(get_values())

print(list_of_dicts)
print(get_values())