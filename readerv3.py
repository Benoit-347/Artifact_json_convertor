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

def get_values(CD=0, CR=0, ER=0, ATK_=0, HP_=0, EM=0, Atk=0, Hp=0, DEF_=0, Def=0):

    global crit_dmg, crit_rate, em, atk, hp_, er, hp, atk_, def_, def1

    crit_dmg    = CD/6.61
    crit_rate   = CR/3.305
    em          = EM/19.815
    atk         = Atk/16.535
    hp_         = HP_/4.955
    er          = ER/5.505
    hp          = Hp/253.94
    atk_        = ATK_/4.955
    def_        = DEF_/4.955
    def1        = Def/253.94

crit_dmg = 0.15129
crit_rate = 0.29922
em = 0.04615
atk = 0.00095
hp_ = 0.14358
er = 0.181650
hp = 0.00095
atk_ = 0.14358
def_ = 0
def1 = 0

get_values(CD=1, CR=1, ER=0.77, ATK_=0.47, HP_=0, EM=0.77, Atk=0.1667, Hp=0, DEF_=0, Def=0)

#check the stat name and returns its individual roll value
def check_stat(a):

    if a == "hp_":
        return hp_
    elif a == 'critDMG_':
        return crit_dmg
    elif a == 'critRate_':
        return crit_rate
    elif a == 'enerRech_':
        return er
    elif a == "hp":
        return hp
    elif a == "def_":
        return def_
    elif a == "def":
        return def1
    elif a == "atk":
        return atk
    elif a == "atk_":
        return atk_
    elif a == "eleMas":
        return em  

def get_roll(a):
    result = 0
    for i in a:
        result += check_stat(i['key'])* float(i['value'])
    return result


#the main program to get each artifact's details and put substats into newlines 
def change_values():
    j = 0
    for dict1 in list_of_dicts:
        get_roll(dict1['substats'])
        dict1['substats'] = get_roll(dict1['substats'])
        j += 1
        print(f"{j}st iteration of get values")


change_values()

def get_artifact(a, b=0, c=20):
    new_list_of_dicts = []
    for dict1 in list_of_dicts:
        if dict1['setKey'] == a and dict1['substats'] > b and dict1['level'] <= c:
            new_list_of_dicts.append(dict1)
    return new_list_of_dicts

def change_to_list(a):
    result = [[]]
    for dict1 in a:
        values = [dict1['setKey'], dict1['slotKey'], dict1['rarity'], dict1['mainStatKey'], dict1['level'], dict1['location'], dict1['lock'], dict1['id'], dict1['substats']]
        result.append(values)
        result.append([])
    return result
        


#writing the formated data into a csv file
def write_to_csv():
    with open("calcs\EmblemOfSeveredFate_EM_roll_2.csv", "w", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerow(get_keys())
        writer.writerows(change_to_list(get_artifact('EmblemOfSeveredFate', 2, 4)))
write_to_csv()

