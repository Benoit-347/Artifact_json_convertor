#This program reads the json file returned from inventory kamera app and creates a csv file such that it is formated with artifact headings and rows as substats
#Added feature of getting total roll values for each artifact

import csv

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
er = 0
hp = 0.00095
atk_ = 0.14358
def_ = 0
def1 = 0
get_values(CD=1, CR=1, ER=0.77, ATK_=0.47, HP_=0, EM=0, Atk=0.1667, Hp=0, DEF_=0, Def=0)

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

# reads csv file, while reading every subsequent artifact data, it stores the data in a list and appends total roll value such that it is returned next line of substats
def calc_csv():
    with open ("data.csv") as file1:
        reader = csv.reader(file1)
        flag = 0    #to return total roll value when using past iterations
        total_rolls = 0   
        results = []    #the data storage that stores  for each artifact
        temp = []
        j = 0
        for line in reader:
            print(j := j+ 1)
            temp.append(line)   #re-store
            if len(line) != 0:  
                if line[0] == "key":    #to start obatiing roll values
                    flag = 4        #only 4 subs per artifact
                    continue
                if flag >0:
                    total_rolls += check_stat(line[0])* float(line[1])  #adding roll values
                    flag -= 1
                    if flag == 0:
                        temp[1].extend(["Total Rolls:", round(total_rolls, 1)]) #Add the line of total rolls
                        total_rolls = 0
                        results.extend(temp)
                        temp = []

            else:
                if flag > 0:
                    flag = 0
                    temp[1].extend(["Total Rolls:", round(total_rolls, 1)]) #Add the line of total rolls
                    total_rolls = 0
                    temp.pop()
                    results.extend(temp)
                    temp = [[]]
    return results

#writes the updated data into a new csv file
def write_calculated():
    with open ("calcs/rolls_imported.csv", "w+", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerows(calc_csv())

write_calculated()