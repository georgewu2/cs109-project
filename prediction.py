import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.ensemble import RandomForestClassifier

def main():
    train = pickle.load(open('train.pckl', 'rb'))
    lookup_table2 = pickle.load(open('lookuptable2.pckl', 'rb'))
    position_pairs = pickle.load(open('position_pairs.pckl', 'rb'))
    train_reduced = pickle.load(open('train_reduced.pckl', 'rb'))
    champion_data = pickle.load(open('championData.pckl','rb'))
    trim_lookup2 = lookup_table2[lookup_table2['Matches'] >= 5].reset_index(drop=True)
    X = train_reduced.as_matrix()
    Y = np.array(train['Winner']) 
    forest_train = RandomForestClassifier(n_estimators=18).fit(X, Y)
    print "Enter the champions for team 1. Do not include spaces or apostrophes in the spelling, but keep uppercase and lowercase consistent. For example, Lee Sin should be inputted as LeeSin, and Kog'Maw should be inputted as KogMaw."
    top1 = raw_input("Please enter the champion that will go top: ")
    while top1 not in champion_data.values():
        top1 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that will go top: ")
    jug1 = raw_input("Please enter the champion that will jungle: ")
    while jug1 not in champion_data.values():
        jug1 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that will jungle: ")
    mid1 = raw_input("Please enter the champion that will go middle: ")
    while mid1 not in champion_data.values():
        mid1 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that will go middle: ")
    adc1 = raw_input("Please enter the champion that be the attack damage carry: ")
    while adc1 not in champion_data.values():
        adc1 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that be the attack damage carry: ")
    sup1 = raw_input("Please enter the champion that be the support: ")
    while sup1 not in champion_data.values():
        sup1 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes \nPlease enter the champion that be the support: ")

    print "Enter the champions for team 2. Do not include spaces or apostrophes in the spelling, but keep uppercase and lowercase consistent. For example, Lee Sin should be inputted as LeeSin, and Kog'Maw should be inputted as KogMaw."
    top2 = raw_input("Please enter the champion that will go top: ")
    while top2 not in champion_data.values():
        top2 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that will go top: ")
    jug2 = raw_input("Please enter the champion that will jungle: ")
    while jug2 not in champion_data.values():
        jug2 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that will jungle: ")
    mid2 = raw_input("Please enter the champion that will go middle: ")
    while mid2 not in champion_data.values():
        mid2 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that will go middle: ")
    adc2 = raw_input("Please enter the champion that be the attack damage carry: ")
    while adc2 not in champion_data.values():
        adc2 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes. \nPlease enter the champion that be the attack damage carry: ")
    sup2 = raw_input("Please enter the champion that be the support: ")
    while sup2 not in champion_data.values():
        sup2 = raw_input("The champion you have entered does not exist in the database. Please be sure that there are no spaces and apostrophes \nPlease enter the champion that be the support: ")

    team1 = [top1,jug1,mid1,adc1,sup1]
    team2 = [top2,jug2,mid2,adc2,sup2]

    prediction(team1,team2,trim_lookup2,position_pairs,forest_train)

"""
Finds all possible combinations of pairs/triples for each team in each match
Input:
    team1: column names for team 1
    team2: column names for team 2
Output:
    data: dataframe of combinations
"""
def create_pairs(matches):
    team1 = ['top1', 'jun1', 'mid1', 'adc1', 'sup1']
    team2 = ['top2', 'jun2', 'mid2', 'adc2', 'sup2']
    title = ['champ1', 'champ2', 'W', 'ID']
    # number of matches in data set
    rows = []
    print 'Processing Team 1 Pairs'
    for p in range(0, len(matches)): 
        for i in range(0,len(team1)):
            for j in range(i+1, len(team1)):
                row = []
                row.append(sorted([matches[team1[i]][p], matches[team1[j]][p]])[0])
                row.append(sorted([matches[team1[i]][p], matches[team1[j]][p]])[1])
                row.append(matches['Winner'][p] == 1)
                row.append(team1[i]+team1[j])
                rows.append(row)
        if (p % 5000 == 0):
            print str(p+1) + ' matches processed...'
    print 'Processing Team 2 Pairs'
    for p in range(0, len(matches['top1'])): 
        for i in range(0,len(team2)):
            for j in range(i+1, len(team2)):
                row = []
                row.append(sorted([matches[team2[i]][p], matches[team2[j]][p]])[0])
                row.append(sorted([matches[team2[i]][p], matches[team2[j]][p]])[1])
                row.append(matches['Winner'][p] == 0)
                row.append(team2[i]+team2[j])
                rows.append(row)
        if (p % 5000 == 0):
            print str(p+1) + ' matches processed...'
    data = pd.DataFrame(rows,columns=title)
    return data

def create_trips(matches):
    team1 = ['top1', 'jun1', 'mid1', 'adc1', 'sup1']
    team2 = ['top2', 'jun2', 'mid2', 'adc2', 'sup2']
    title = ['champ1','champ2','champ3','W','ID']
    num = len(matches)
    data = pd.DataFrame(index=range(0, 20*num), columns=title)
    champ1_list = []
    champ2_list = []
    champ3_list = []
    win = []
    ids = []
    for p in range(0, len(matches['top1'])): 
        for i in range(0,len(team1)):
            for j in range(i+1, len(team1)):
                for k in range(j+1, len(team1)):
                    temp = sorted([matches[team1[i]][p], matches[team1[j]][p], matches[team1[k]][p]])
                    champ1_list.append(temp[0])
                    champ2_list.append(temp[1])
                    champ3_list.append(temp[2])
                    win.append(matches['Winner'][p] == 1)
                    ids.append(team1[i]+team1[j]+team1[k])
        if (p % 5000 == 0):
            print str(p+1) + ' matches processed...'
    for p in range(0, len(matches['top1'])): 
        for i in range(0,len(team2)):
            for j in range(i+1, len(team2)):
                for k in range(j+1, len(team2)):
                    temp = sorted([matches[team2[i]][p], matches[team2[j]][p], matches[team2[k]][p]])
                    champ1_list.append(temp[0])
                    champ2_list.append(temp[1])
                    champ3_list.append(temp[2])
                    win.append(matches['Winner'][p] == 0)
                    ids.append(team2[i]+team2[j]+team2[k])
        if (p % 5000 == 0):
            print str(p+1) + ' matches processed...'
    data['champ1'] = champ1_list
    data['champ2'] = champ2_list
    data['champ3'] = champ3_list
    data['W'] = win
    data['ID'] = ids
    return data


# define function to calculate historical win percentage of each pair
"""
Creates a lookup table that determines the win percentage of each pair/triples of champions
Input
    champ_pairs: output from create_pairs/create_trips
    cutoff: 
Output
    data: the lookup table
"""
def pair_winpercent(champ_pairs, cutoff=0):
    pairlist = pd.DataFrame(champ_pairs)
    pairlist = pairlist.drop_duplicates(subset=['champ1', 'champ2']).reset_index(drop=True)
    pairlist['Wins'] = ''
    pairlist['Matches'] = ''
    pairlist['Win_percent'] = ''
    for i in range(0, len(pairlist)):
        if (i % 4000 == 0):
            print str(i) + ' unique pairs processed'
        filteredlist = champ_pairs[(champ_pairs['champ1'] == pairlist['champ1'][i]) & (champ_pairs['champ2'] == pairlist['champ2'][i])]
        pairlist['Wins'][i] = len(filteredlist[filteredlist['W'] == True])
        pairlist['Matches'][i] = len(filteredlist)
        pairlist['Win_percent'][i] = np.round(1.0*pairlist['Wins'][i]/pairlist['Matches'][i], 2)
    pairlist = pairlist.drop('W', 1).drop('ID', 1).sort(columns='champ2').sort(columns='champ1').reset_index(drop=True)
    return pairlist[pairlist['Matches'] >= cutoff].reset_index(drop=True)

def triple_winpercent(champ_triples, cutoff=0):
    triplelist = pd.DataFrame(champ_triples)
    triplelist = triplelist.drop_duplicates(subset=['champ1', 'champ2', 'champ3']).reset_index(drop=True)
    triplelist['Wins'] = ''
    triplelist['Matches'] = ''
    triplelist['Win_percent'] = ''
    for i in range(0, len(triplelist)):
        if (i % 4000 == 0):
            print str(i) + ' unique triples processed'
        filteredlist = champ_triples[(champ_triples['champ1'] == triplelist['champ1'][i]) & (champ_triples['champ2'] == triplelist['champ2'][i]) & (champ_triples['champ3'] == triplelist['champ3'][i])]
        triplelist['Wins'][i] = len(filteredlist[filteredlist['W'] == True])
        triplelist['Matches'][i] = len(filteredlist)
        triplelist['Win_percent'][i] = np.round(1.0*triplelist['Wins'][i]/triplelist['Matches'][i], 2)
    triplelist = triplelist.drop('W', 1).drop('ID', 1).sort(columns='champ3').sort(columns='champ2').sort(columns='champ1').reset_index(drop=True)
    return triplelist[triplelist['Matches'] >= cutoff].reset_index(drop=True)



"""

Input
    champ_pairs: create_pairs output
    pairlist: lookup table
    final_comb: list of column names
    num: number of matches
Output
    pos_comb: table of probabilities for each game
"""
def create_prob(champ_pairs, pairlist, final_comb, num):
    count_x = 0
    count_y = 0
    pos_comb = pd.DataFrame(index=range(0,num), columns=final_comb)
    for i in range(0, len(final_comb)):
        if (i % 5 == 0):
            print str(i) + ' fields processed'
        filtered = champ_pairs[champ_pairs['ID'] == final_comb[i]].reset_index(drop=True)  
        array = []
        for j in range(0, len(filtered)):
            temp = pairlist[(pairlist['champ1'] == filtered['champ1'][j]) & (pairlist['champ2'] == filtered['champ2'][j])].reset_index(drop=True)['Win_percent']
            if (len(temp) > 0):
                array.append(temp[0])
                count_x += 1
                count_y += 1
            else:
                array.append(0.5)
                count_y += 1
        pos_comb[final_comb[i]] = array
    return pos_comb


def create_prob_full(champ_pairs, champ_triples, pairlist, triplelist, final_comb, num):
    count_x = 0
    count_y = 0
    pos_comb = pd.DataFrame(index=range(0,num), columns=final_comb)
    for i in range(0, len(final_comb)):
        if (i % 5 == 0):
            print str(i) + ' fields processed'
        if (len(final_comb[i]) == 8):
            filtered = champ_pairs[champ_pairs['ID'] == final_comb[i]].reset_index(drop=True)
        else:
            filtered = champ_triples[champ_triples['ID'] == final_comb[i]].reset_index(drop=True)
        array = []
        for j in range(0, len(filtered)):
            if (len(final_comb[i]) == 8):
                temp = pairlist[(pairlist['champ1'] == filtered['champ1'][j]) & (pairlist['champ2'] == filtered['champ2'][j])].reset_index(drop=True)['Win_percent']
            else:
                temp = triplelist[(triplelist['champ1'] == filtered['champ1'][j]) & (triplelist['champ2'] == filtered['champ2'][j]) & (triplelist['champ3'] == filtered['champ3'][j])].reset_index(drop=True)['Win_percent']
            if (len(temp) > 0):
                array.append(temp[0])
                count_x += 1
                count_y += 1
            else:
                array.append(0.5)
                count_y += 1               
        pos_comb[final_comb[i]] = array
    return pos_comb

def prediction(array1, array2,trim_lookup2,position_pairs,forest_train):
    tracker = 0
    
    if (array1[0] > array2[0]):
        temp = array1
        array1 = array2
        array2 = temp
        tracker = 1

    categ = ['top1', 'jun1', 'mid1', 'adc1', 'sup1', 'top2', 'jun2', 'mid2', 'adc2', 'sup2', 'Winner']
    entry = pd.DataFrame(index=range(0, 1), columns=categ)
    merge = array1 + array2 + ['N']
    entry.loc[0]  = merge
    pairings_test = create_pairs(entry)
    test_data = create_prob(pairings_test, trim_lookup2, position_pairs, len(entry))
    X_test = test_data.as_matrix()
    

    predicted = forest_train.predict(X_test)
    if (((list(predicted)[0] == 1) & (tracker ==0)) | ((list(predicted)[0] == 0) & (tracker ==1))):
        print 'Prediction Results: Team 1 Wins'
        return 1
    else:
        print 'Prediction Results: Team 2 Wins'
        return 2

if __name__ == "__main__":
    main()

