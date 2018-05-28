import pandas as pd
import numpy as np

af = pd.read_csv("../Sample Data/Affinity.csv", header = None)
pp = pd.read_csv("../Sample Data/Parent and Popularity.csv")
grouped = pp.groupby('Parent')

n_affinity = 4
n_popular = 3
n_random = 1
n_calculator = 1


# group = grouped.get_group(27)
# print group
# group = group.sort_values('Visits', ascending = False)
# print group


f = open("./output.csv", "w+")
f.write("id,Title,Recommendation\n")


for index, row in pp.iterrows():
    if np.isnan(row['id']):
        continue

    try:
        group = grouped.get_group(row['Parent'])    # get the group with the same parent
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

        if len(list_affinity) > n_affinity: # randomly choose n_affinity number of articles
            list_affinity = np.random.choice(list_affinity, n_affinity)

        list_affinity = np.array(list_affinity)
        group_remain = group_remain[~group_remain['id'].isin(list_affinity)]    # remove affinity from group_remain so it won't be included in list_popular and list_random
        
        # calculate a list for popular
        list_popular = []
        group_remain = group_remain.sort_values('Visits', ascending = False)    # sort group_remain by Visits to get the most popular pages
        group_remain_length = len(group_remain)

        if group_remain_length <= n_popular:
            list_popular = group_remain['id'].values
        else:
            list_popular = group_remain['id'].values[ : n_popular]

        group_remain = group_remain[~group_remain['id'].isin(list_popular)] # remove popular from group_remain so it won't be in list_random

        # calculate a list for random
        list_random = []
        group_remain_length = len(group_remain)

        if group_remain_length <= n_random:
            list_random = group_remain['id'].values
        else:
            list_random = np.random.choice(group_remain['id'].values, n_random, replace = False)

        group_remain = group_remain[~group_remain['id'].isin(list_random)]


        # write row to file
        recommendations = str(list_affinity.astype(int)) + ',' + str(list_popular.astype(int)) + ',' + str(list_random.astype(int))

        f.write('%s,"%s","%s"\n' % (str(int(row['id'])), row['Title'], recommendations))
    except KeyError as err:
        print 'Could not find parent for article id ' + str(int(row['id']))
        f.write('%s,"%s","Missing parent id"\n' % (str(int(row['id'])), row['Title']))
 
f.close()