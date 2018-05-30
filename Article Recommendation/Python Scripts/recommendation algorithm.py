import pandas as pd
import numpy as np

af = pd.read_csv("../Sample Data/Affinity.csv", header = None)
pp = pd.read_csv("../Sample Data/Parent and Popularity.csv")
ca = pd.read_csv("../Sample Data/Calculators.csv")

n_total = 9
n_affinity = 3
n_popular = 2
#n_random = 3
n_calculator = 1


# group = grouped.get_group(27)
# print group
# group = group.sort_values('Visits', ascending = False)
# print group
# pp.loc[pp['Parent Slug'] == 'boat', ['Parent Slug']] = 'auto/powersport'
# pp.loc[pp['Parent Slug'] == 'home', ['Parent Slug']] = 'home/mortgage'
# pp.loc[pp['Parent Slug'] == 'bankruptcy', ['Parent Slug']] = 'credit-repair'
# pp.loc[pp['Parent Slug'] == 'debt-relief', ['Parent Slug']] = 'debt-consolidation'
# print pp.head(10)

grandparent = []

for index, row in pp.iterrows():
    if row['Parent Slug'].find('/') == -1: 
        grandparent.append(row['Parent Slug'])
    if row['Parent Slug'] == 'boat':
        row['Parent Slug'] = 'auto/powersport'
        grandparent.append('auto') 
    elif row['Parent Slug'] == 'home':
        row['Parent Slug'] = 'home/mortgage'
        grandparent.append('home') 
    elif row['Parent Slug'] == 'bankruptcy':
        row['Parent Slug'] = 'credit-repair'
        grandparent.append('credit-repair') 
    elif row['Parent Slug'] == 'debt-relief':
        row['Parent Slug'] = 'debt-consolidation'
        grandparent.append('debt-consolidation') 
    elif row['Parent Slug'] == 'home/usda':
        row['Parent Slug'] = 'home/mortgage'
        grandparent.append('home')
    elif row['Parent Slug'] == 'home/usda/eligibility':
        row['Parent Slug'] = 'home/mortgage'
        grandparent.append('home')    
    else:
        grandparent.append(row['Parent Slug'].rpartition('/')[0])

pp['grandparent'] = grandparent



grouped = pp.groupby('Parent')
ggrouped = pp.groupby('grandparent')
print ggrouped.head()

f = open("./output.csv", "w+")
f.write("id,Title,Recommendation\n")

for index, row in pp.iterrows():
    if np.isnan(row['id']):
        continue
    try:
        group = grouped.get_group(row['Parent'])    # get the group with the same parent
        ggroup = ggrouped.get_group(row['grandparent'])  # get the group with the same grandparent
        group_remain = group[group['id'] != row['id']] #remove current article from the group
        ggroup_remain = ggroup[ggroup['id'] != row['id']] #remove current article from the ggroup
        #print(ggroup_remain)

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
        ggroup_remain = ggroup_remain[~ggroup_remain['id'].isin(list_affinity)]    # remove affinity from ggroup_remain so it won't be included in list_popular and list_random

        # calculate a list for popular
        list_popular = []
        group_remain = group_remain.sort_values('Visits', ascending = False)    # sort group_remain by Visits to get the most popular pages
        group_remain_length = len(group_remain)

        if group_remain_length <= n_popular:
            list_popular = group_remain['id'].values
        else:
            list_popular = group_remain['id'].values[ : n_popular]

        group_remain = group_remain[~group_remain['id'].isin(list_popular)] # remove popular from group_remain so it won't be in list_random
        ggroup_remain = ggroup_remain[~ggroup_remain['id'].isin(list_popular)] # remove popular from ggroup_remain so it won't be in list_random


        # pick calculator
        list_calculator = []
        calculator_group = ca[ca['Parent'] == row['Parent']]
        
        if len(calculator_group) <= n_calculator:
            list_calculator = calculator_group['id'].values
        else:
            list_calculator = np.random.choice(calculator_group['id'].values, n_calculator, replace = False)

        # calculate a list for random
        list_random = []
        plist_random = []
        glist_random = []

        n_random = n_total - len(list_affinity) - len(list_popular) - len(list_calculator)
        group_remain_length = len(group_remain)

        if group_remain_length <= n_random:
            plist_random = group_remain['id'].values
            glist_random = np.random.choice(ggroup_remain['id'].values, n_random - group_remain_length)
            list_random = plist_random + glist_random
        else:
            list_random = np.random.choice(group_remain['id'].values, n_random, replace = False)

        group_remain = group_remain[~group_remain['id'].isin(list_random)]
        ggroup_remain = ggroup_remain[~ggroup_remain['id'].isin(list_random)]

        # write row to file
        recommendations = str(list_affinity.astype(int)) + ',' + str(list_popular.astype(int)) + ',' + str(list_random.astype(int)) + ',' + str(list_calculator.astype(int))

        f.write('%s,"%s","%s"\n' % (str(int(row['id'])), row['Title'], recommendations))
    except KeyError as err:
        print 'Could not find parent for article id ' + str(int(row['id']))
        f.write('%s,"%s","Missing parent id"\n' % (str(int(row['id'])), row['Title']))
f.close()

