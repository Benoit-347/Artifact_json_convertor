#This program reads the csv file containing artifact data with substat values and creates a new file which containes rows of artifact id and total value of roll 
#The value of each roll can be set with unit being per 1% or for flat per 1 unit
import csv

#check the stat name and returns its individual roll value
def check_stat(a):

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

# reads csv file and creates a list containing list of Id and roll
def calc_csv():
    with open ("data.csv") as file1:
        reader = csv.reader(file1)
        flag = 0
        a = 0
        j = -3
        b = [["ID", "Roll Value"]]
        for line in reader:
            j+=1
            if j %8 == 0:
                c = []
                id = line[7]
                c.append(id)
            if len(line) != 0:
                if line[0] == "key":
                    flag = 4
                    continue
                if flag >0:
                    a += check_stat(line[0])* float(line[1])
                    flag -= 1
                    if flag == 0:
                        c.append(round(a, 1))
                        b.append(c)
                        a = 0
    return b

#write the calculated data obtained into a file 
def write_calculated():
    with open ("calculated.csv", "w+", newline= "") as file1:
        writer = csv.writer(file1)
        writer.writerows(calc_csv())

write_calculated()