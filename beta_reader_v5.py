#a = substat
b = {'setKey': 'ObsidianCodex', 'slotKey': 'flower', 'rarity': 5, 'mainStatKey': 'hp', 'level': 20, 'substats': [{'key': 'critRate_', 'value': 3.9}, {'key': 'hp_', 'value': 21.6}, {'key': 'critDMG_', 'value': 6.6}], 'location': '', 'lock': True, 'id': 0}

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
    

#gets teh roll value of individual substats to predict num of possible rolls




def predict(artifact, threshold, threshold_probability):
    a = artifact['substats']
    substat_list = []
    individual_rolls = []
    possible_individual_rolls = []
    threshold_list = []
    #getting number of substats and storing its value in a dict
    initial_roll_value = 0
    for i in a:
        substat = i['key']
        substat_list.append(substat)
        b = get_roll_substat_key(substat)
        individual_rolls.append(b)
        initial_roll_value += b
    
    print(substat_list)
    print(individual_rolls)

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
                            possible_individual_rolls.append(n)

        
        for i in possible_individual_rolls:
            if i>= threshold:
                threshold_list.append(i)
        probability = len(threshold_list)/len(possible_individual_rolls)
        possible_individual_rolls.sort(reverse = True)
        probable_value = possible_individual_rolls[len(possible_individual_rolls)//2]
        plausible_ceiling =  possible_individual_rolls[round(len(possible_individual_rolls)*threshold_probability)]
        result = [probability,probable_value, plausible_ceiling]
    return result



#elif num ==2:
    #op
#elif num ==1:
    #op
    


def update_roll_values(a, b):
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
    
    print(substat_list)
    print(individual_rolls)

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




def main():
    update_roll_values("ObsidianCodex", 1)
    a = []
    main_stat_chance = 0.05
    print(new_predict(b, 2, 1/(5*300*main_stat_chance)))        #Flower		Feather		Sans		Goblet		Circlet
                                                            #0.20		0.20		0.05		0.01		0.04

main()