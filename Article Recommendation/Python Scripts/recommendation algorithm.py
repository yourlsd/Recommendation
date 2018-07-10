import pandas as pd
import numpy as np

af = pd.read_csv("../Sample Data/Affinity.csv", header = None)
pp = pd.read_csv("../Sample Data/performance and parent7_10.csv")
ca = pd.read_csv("../Sample Data/Calculators7_10.csv")

n_total = 9
n_affinity = 3
n_popular = 2
#n_random = 3
n_calculator = 1


# group = grouped.get_group(27)
# print group
# group = group.sort_values('score', ascending = False)
# print group

secondary = []

for index, row in pp.iterrows():
    if row['Parent Slug'] == 'boat':
        secondary.append('auto/powersport') 
    elif row['Parent Slug'] == 'home':
        secondary.append('home/mortgage') 
    elif row['Parent Slug'] == 'bankruptcy':
        secondary.append('credit-repair') 
    elif row['Parent Slug'] == 'debt-relief':
        secondary.append('debt-consolidation') 
    elif row['Parent Slug'] == 'home/usda':
        secondary.append('home/mortgage')
    elif row['Parent Slug'] == 'home/usda/eligibility':
        secondary.append('home/mortgage')    
    elif row['Parent Slug'].find('/') == -1: 
        secondary.append(row['Parent Slug'])
    else:
        secondary.append(row['Parent Slug'].rpartition('/')[0])

pp['secondary'] = secondary

pp['count'] = [0] * len(pp)

grouped = pp.groupby('Parent Slug')

f = open("./output.csv", "w+")
f.write("id,Title,Recommendation\n")

for index, row in pp.iterrows():
    if np.isnan(row['id']):
        continue
    try:
        group = grouped.get_group(row['Parent Slug'])    # get the group with the same parent
        group_remain = group[group['id'] != row['id']] #remove current article from the group

        # calculate a list for affinity
        list_affinity = []
        affinity = af[af[0] == row['id']]
        if len(affinity) > 0:
            line = affinity.iloc[0]
            for i in range(1, len(line) - 1):
                if np.isnan(line[i]):
                    break
                else:
                    list_affinity.append(line[i])
        
        list_affinity = list(set(list_affinity) & set(pp['id'].values)) #list_affinity = list_affinity intersect with ppid
    
        if len(list_affinity) > n_affinity: # randomly choose n_affinity number of articles
            list_affinity = np.random.choice(list_affinity, n_affinity, replace = False)

        list_affinity = np.array(list_affinity)
        group_remain = group_remain[~group_remain['id'].isin(list_affinity)]    # remove affinity from group_remain so it won't be included in list_popular and list_random

        # calculate a list for popular
        list_popular = []
        group_remain = group_remain.sort_values('score', ascending = False)    # sort group_remain by score to get the most popular pages
        group_remain_length = len(group_remain)

        if group_remain_length <= n_popular:
            list_popular = group_remain['id'].values
        else:
            list_popular = group_remain['id'].values[ : n_popular]

        group_remain = group_remain[~group_remain['id'].isin(list_popular)] # remove popular from group_remain so it won't be in list_random


        # pick calculator
        list_calculator = []
        calculator_group = ca[ca['Parent'] == row['Parent']]
        
        if len(calculator_group) <= n_calculator:
            list_calculator = calculator_group['id'].values
        else:
            list_calculator = np.random.choice(calculator_group['id'].values, n_calculator, replace = False)

        # calculate plist_random
        plist_random = []
        n_random = n_total - len(list_affinity) - len(list_popular) - len(list_calculator)
        group_remain_length = len(group_remain)

        if group_remain_length <= n_random:
            plist_random = group_remain['id'].values
        else:
            group_remain = group_remain.sort_values('count', ascending = True)
            plist_random = group_remain['id'].values[ : n_random]
            # plist_random = np.random.choice(group_remain['id'].values, n_random, replace = False)

        group_remain = group_remain[~group_remain['id'].isin(plist_random)]

        #calculate slist_random
        slist_random = []
        if n_random-len(plist_random) > 0:
            sgroup = grouped.get_group(row['secondary'])
            sgroup_remain = sgroup[sgroup['id'] != row['id']]
            sgroup_remain = sgroup_remain[~sgroup_remain['id'].isin(list_affinity)]
            sgroup_remain = sgroup_remain[~sgroup_remain['id'].isin(list_popular)]
            sgroup_remain = sgroup_remain[~sgroup_remain['id'].isin(plist_random)]

            if n_random-len(plist_random) >= len(sgroup_remain): 
                slist_random = sgroup_remain['id'].values
            else:
                sgroup_remain = sgroup_remain.sort_values('count', ascending = True)
                slist_random = sgroup_remain['id'].values[ : n_random - len(plist_random)]
                # slist_random = np.random.choice(sgroup_remain['id'].values, n_random - len(plist_random) , replace = False)
            
        slist_random = np.array(slist_random)

        # update count
        pp.loc[pp['id'].isin(list_affinity), 'count'] += 1
        pp.loc[pp['id'].isin(list_popular), 'count'] += 1
        pp.loc[pp['id'].isin(plist_random), 'count'] += 1
        pp.loc[pp['id'].isin(slist_random), 'count'] += 1

        # write row to file
        recommendations = str(list_affinity.astype(int)) + ',' + str(list_popular.astype(int)) + ',' + str(plist_random.astype(int)) + ',' + str(slist_random.astype(int)) + ',' + str(list_calculator.astype(int))

        f.write('%s,"%s","%s"\n' % (str(int(row['id'])), row['Title'], recommendations))
    except KeyError as err:
        print 'Could not find parent for article id ' + str(int(row['id']))
        f.write('%s,"%s","Missing parent id"\n' % (str(int(row['id'])), row['Title']))
f.close()

pp.to_csv('check.csv')