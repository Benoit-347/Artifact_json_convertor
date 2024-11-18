#This program reads the json file returned from inventory kamera app and creates a csv file such that it is formated with artifact headings and rows as substats
# added values later to have stat
import csv
from copy import deepcopy
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
    
    global CD, CR, ER, ATK_, HP_, EM, Atk, Hp, DEF_, Def


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
def change_values(the_list):
    for dict1 in the_list:
        a = get_roll(dict1['substats'])
        dict1['substats'] = a
    else:
        print(f"\nDone analysis and change of substat values\n")
        return the_list
#filtering:
def filter_get_artifact(a, slotkey, main_stat, c=0, d=20):

    # slotkey: "flower", "plume", "sands", "goblet", "circlet"

    new_list_of_dicts = []
    for dict1 in list_of_dicts:
        if dict1['setKey'] == a and dict1['slotKey'] == slotkey and get_roll(dict1['substats']) > c and dict1['level'] <= d and dict1['mainStatKey'] in main_stat:
            it = deepcopy(dict1)
            new_list_of_dicts.append(it)

    print(f"Done Filtering artifacts from list of dicts\n")
    if new_list_of_dicts == []:
        return [{'setKey': a, 'slotKey': slotkey, 'rarity': '', 'mainStatKey': '', 'level': '', 'substats': '', 'location': '', 'lock': "", 'id': ''}]
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

def combine_write_to_csv(artifact_name, rolls_1, level_1, rolls_2, level_2, sans, goblet, circlet, EM, threshold, nuance=0):

    if nuance:
        a = "_nuance"
    else:
        a = ""
    if EM:
        file_name = "calcs\\" + artifact_name + a + "_EM" + "beta" + ".csv"
    else:
        file_name = "calcs\\" + artifact_name + a + "beta" + ".csv"

    with open(file_name, "w", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerow(get_keys())
        final = [[]]
        print(f"\n--*--Starting 1st data import--*--\n\n")
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "flower", ['hp'], rolls_1 + 0.38, level_1))))
        final.append([])
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "flower", ['hp'] ,rolls_2, level_2))))
        final.extend([[],[]])

        print(f"\n--*--Starting 2st data import--*--\n\n")
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "plume", ['atk'], rolls_1 + 0.38, level_1))))
        final.append([])
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "plume", ['atk'], rolls_2, level_2))))
        final.extend([[],[]])
        
        print(f"\n--*--Starting 3st data import--*--\n\n")
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "sands", sans, rolls_1-0.19, level_1))))
        final.append([])
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "sands", sans, 4, level_2))))
        final.extend([[],[]])

        print(f"\n--*--Starting 4st data import--*--\n\n")
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "goblet", goblet, rolls_1-0.19, level_1))))
        final.append([])
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "goblet", goblet, 4, level_2))))
        final.extend([[],[]])

        print(f"\n--*--Starting 5st data import--*--\n\n")
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "circlet", circlet, rolls_1-0.19, level_1))))
        final.append([])
        final.extend(change_to_list(change_values(filter_get_artifact(artifact_name, "circlet", circlet, 4, level_2))))
        final.extend([[],[]])

        print(f"\n--*--Starting write operation--*--\n")
        writer.writerows(final) 
        print(f"\n-----*-----Program execution Successful-----*-----\n")
    import os
    os.startfile(file_name)


def get_roll_substat_key(a):
    if a == "hp_":
        return Hp
    elif a == 'critDMG_':
        return CD
    elif a == 'critRate_':
        return CR
    elif a == 'enerRech_':
        return ER
    elif a == "hp":
        return Hp
    elif a == "def_":
        return DEF_
    elif a == "def":
        return Def
    elif a == "atk":
        return Atk
    elif a == "atk_":
        return ATK_
    elif a == "eleMas":
        return EM 

#gets the roll value of individual substats to predict possible total roll values



def get_weighted(substat_list):
    all_substats = ['critDMG_','critRate_',"atk_","hp_","def_",'enerRech_',"atk","def","hp", "eleMas"]
    return list(set(all_substats) - set(substat_list))

def get_4_stat_chance(substat_list, substat):

    weighted = get_weighted(substat_list)

    CD      =3
    CR      =3
    ER      =4
    ATK_    =4
    HP_     =4
    EM      =4
    Atk     =6
    Hp      =6
    DEF_    =4
    Def     =6

    weight = get_roll_substat_key(substat)
    total_weight = 0
    for i in weighted:
        total_weight += get_roll_substat_key(i)
    chance = weight/total_weight
    return chance


def new_predict(artifact, threshold, threshold_probability):
    a = artifact['substats']
    substat_list = []
    individual_rolls = []
    possible_individual_rolls = []
    threshold_list = []
    new_possible_individual_rolls = []
    initial_roll_value = 0
    for i in a:
        substat = i['key']
        substat_list.append(substat)
        b = get_roll_substat_key(substat)
        individual_rolls.append(b)
        initial_roll_value += b
    
    if len(substat_list) ==4:
        #Q) there exists 4 values: a, b, c, d such that a = 1, b = 0.5, c = 0.1, d = 0.
        #If one among them is picked 5 times consequtively with repititions find:
        # 1. The probability of the total value being above x.

        # 2. (The probable value) i.e. The total value when its probability is 50% 

        # 3. The highest possible value beyond a certain probability
        for i in individual_rolls :
            for j in individual_rolls:
                for k in individual_rolls:
                    for l in individual_rolls:
                        for m in individual_rolls:
                            n = i+j+k+l+m+b
                            new_possible_individual_rolls.append(n)


    elif len(substat_list) ==3:
        weighted = get_weighted(substat_list)
        for i in weighted:
            chance = get_4_stat_chance(substat_list, i)
            new_individual_rolls = individual_rolls
            possible_individual_rolls = []
            new_individual_rolls.append(get_roll_substat_key(i))
            for i in individual_rolls :
                for j in individual_rolls:
                    for k in individual_rolls:
                        for l in individual_rolls:
                            n = i+j+k+l+b
                            possible_individual_rolls.append(n)
            unit = 100
            chance = round(chance*unit)
            buffer = possible_individual_rolls*chance
            new_possible_individual_rolls.extend(buffer)


    for i in new_possible_individual_rolls:
        if i>= threshold:
            threshold_list.append(i)
    probability = len(threshold_list)/len(new_possible_individual_rolls)
    new_possible_individual_rolls.sort(reverse = True)
    probable_value = new_possible_individual_rolls[len(new_possible_individual_rolls)//2]
    plausible_ceiling =  new_possible_individual_rolls[round(len(new_possible_individual_rolls)*threshold_probability)]
    result = [probability,probable_value, plausible_ceiling]


    return result

def get_main_stat_chance(a):
        
    if a == "flower":
        return 0.20
    elif a == "plume":
        return 0.20
    elif a == "sands":
        return 0.05
    elif a == "goblet":
        return 0.01
    elif a == "circlet":
        return 0.04


def main():
    artifact_name = "ObsidianCodex"   #'EmblemOfSeveredFate'  "ScrollOfTheHeroOfCinderCity"   "ObsidianCodex"  "GoldenTroupe"
    rolls_1 = 1
    level_1 = 7
    rolls_2 = 6
    level_2 = 20
    EM = 1
    threshold = rolls_2 + 0.5
    update_stat_values(artifact_name, EM)

    combine_write_to_csv(artifact_name, rolls_1, level_1, rolls_2, level_2,['atk_',  'enerRech_', 'eleMas'], ['hydro_dmg_', 'electro_dmg_',  'pyro_dmg_'], ['critDMG_', 'critRate_'] , EM, threshold , 0)   #sans: hp_  atk_  enerRech_  eleMas
                                                                #obsidian:  ['hp_', 'eleMas'], ['hydro_dmg_', 'hp_'], ['critDMG_']         #gob: electro_dmg_  hydro_dmg_,  pyro_dmg_  
                                                                #EmblemOfSeveredFate:   ['atk_',  'enerRech_', 'eleMas'], ['hydro_dmg_', 'electro_dmg_',  'pyro_dmg_'], ['critDMG_', 'critRate_']  #circlet: critDMG_  critRate_


main()