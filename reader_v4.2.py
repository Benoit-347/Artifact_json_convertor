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

def update_stat_values(a, b):  #'EmblemOfSeveredFate'  "ScrollOfTheHeroOfCinderCity"   "ObsidianCodex"  "GoldenTroupe"
    
    CD      =0
    CR      =0
    ER      =0
    ATK_    =0
    HP_     =0
    EM      =0
    Atk     =0
    Hp      =0
    DEF_    =0
    Def     =0
    if a == 'EmblemOfSeveredFate':
        if b:
            em = 0.77
        else:
            em = 0
        CD=1
        CR=1
        ER=0.77
        ATK_=0.47
        HP_=0
        EM=em
        Atk=0.1667
        Hp=0
        DEF_=0
        Def=0

    elif a == "ObsidianCodex":
        if b:
            em = 0.91
        else:
            em = 0
        CD=1
        CR=0.99
        ER=0
        ATK_=0
        HP_=0.71
        EM=em
        Atk=0
        Hp=0.24
        DEF_=0
        Def=0

    elif a == "ScrollOfTheHeroOfCinderCity":
        pass

    elif a == "GoldenTroupe":
        pass
    get_values(CD, CR, ER, ATK_, HP_, EM, Atk, Hp, DEF_, Def)

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
    return round(result, 2)


#the part to get each artifact's details and put substats into newlines 
def change_values():
    for dict1 in list_of_dicts:
        get_roll(dict1['substats'])
        dict1['substats'] = get_roll(dict1['substats'])
    else:
        print(f"\nDone analysis and change of substat values\n")

#filtering:
def filter_get_artifact(a, name, main_stat, c=0, d=20):

    # Names: "flower", "plume", "sands", "goblet", "circlet"

    new_list_of_dicts = []
    for dict1 in list_of_dicts:
        if dict1['setKey'] == a and dict1['slotKey'] == name and dict1['substats'] > c and dict1['level'] <= d and dict1['mainStatKey'] in main_stat:
            new_list_of_dicts.append(dict1)

    print(f"Done Filtering artifacts from list of dicts\n")
    if new_list_of_dicts == []:
        return [{'setKey': a, 'slotKey': name, 'rarity': '', 'mainStatKey': '', 'level': '', 'substats': '', 'location': '', 'lock': "", 'id': ''}]
    return new_list_of_dicts

def change_to_list(a):
    result = []
    for dict1 in a:
        values = [dict1['setKey'], dict1['slotKey'], dict1['rarity'], dict1['mainStatKey'], dict1['level'], dict1['location'], dict1['lock'], dict1['id'], dict1['substats']]
        result.append(values)
    print(f"Done conversion of dicts to lists\n")
    sorted_result = sorted(result, key=lambda x: x[8], reverse=True)
    print(f"Sorting of lists successfull\n")
    return sorted_result
        


#writing the formated data into a csv file

def combine_write_to_csv(artifact_name, rolls_1, level_1, rolls_2, level_2, sans, goblet, circlet, EM, nuance=0):

    if nuance:
        a = "_nuance"
    else:
        a = ""
    if EM:
        file_name = "calcs\\" + artifact_name + a + "_EM" + ".csv"
    else:
        file_name = "calcs\\" + artifact_name + a + ".csv"

    with open(file_name, "w", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerow(get_keys())
        final = [[]]
        print(f"\n--*--Starting 1st data import--*--\n\n")
        final.extend(change_to_list(filter_get_artifact(artifact_name, "flower", ['hp'], rolls_1, level_1)))
        final.append([])
        final.extend(change_to_list(filter_get_artifact(artifact_name, "flower", ['hp'] ,rolls_2, level_2)))
        final.extend([[],[]])

        print(f"\n--*--Starting 2st data import--*--\n\n")
        final.extend(change_to_list(filter_get_artifact(artifact_name, "plume", ['atk'], rolls_1, level_1)))
        final.append([])
        final.extend(change_to_list(filter_get_artifact(artifact_name, "plume", ['atk'], rolls_2, level_2)))
        final.extend([[],[]])
        
        print(f"\n--*--Starting 3st data import--*--\n\n")
        final.extend(change_to_list(filter_get_artifact(artifact_name, "sands", sans, rolls_1-0.72, level_1)))
        final.append([])
        final.extend(change_to_list(filter_get_artifact(artifact_name, "sands", sans, 4, level_2)))
        final.extend([[],[]])

        print(f"\n--*--Starting 4st data import--*--\n\n")
        final.extend(change_to_list(filter_get_artifact(artifact_name, "goblet", goblet, 4, level_1)))
        final.append([])
        final.extend(change_to_list(filter_get_artifact(artifact_name, "goblet", goblet, rolls_2-1, level_2)))
        final.extend([[],[]])

        print(f"\n--*--Starting 5st data import--*--\n\n")
        final.extend(change_to_list(filter_get_artifact(artifact_name, "circlet", circlet, 4, level_1))) 
        final.append([])
        final.extend(change_to_list(filter_get_artifact(artifact_name, "circlet", circlet, 4, level_2)))
        final.extend([[],[]])

        print(f"\n--*--Starting write operation--*--\n")
        writer.writerows(final) 
        print(f"\n-----*-----Program execution Successful-----*-----\n")
    import os
    os.startfile(file_name)

def main():
    artifact_name = 'EmblemOfSeveredFate'   #'EmblemOfSeveredFate'  "ScrollOfTheHeroOfCinderCity"   "ObsidianCodex"  "GoldenTroupe"
    rolls_1 = 1.5
    level_1 = 7
    rolls_2 = 6
    level_2 = 20
    EM = 0

    update_stat_values(artifact_name, EM)
    change_values()
    combine_write_to_csv(artifact_name, rolls_1, level_1, rolls_2, level_2,['atk_',  'enerRech_', 'eleMas'], ['hydro_dmg_', 'electro_dmg_',  'pyro_dmg_'], ['critDMG_', 'critRate_'] , EM, 0)   #sans: hp_  atk_  enerRech_  eleMas
                                                                #obsidian:  ['hp_', 'eleMas'], ['hydro_dmg_', 'hp_'], ['critDMG_']         #gob: electro_dmg_  hydro_dmg_,  pyro_dmg_  
                                                                #EmblemOfSeveredFate:   ['atk_',  'enerRech_', 'eleMas'], ['hydro_dmg_', 'electro_dmg_',  'pyro_dmg_'], ['critDMG_', 'critRate_']  #circlet: critDMG_  critRate_

main()