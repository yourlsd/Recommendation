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


f = open("./output.txt", "w+")
f.write("id,Title,Recommendation\n")


for index, row in pp.iterrows():
    if np.isnan(row['id']):
        continue

    try:
        group = grouped.get_group(row['Parent'])    # get the group with the same parent
        group = group[group['id'] != row['id']] #remove current article from the group

        group_length = len(group.index.values)

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

        
        # calculate a list for popular
        group_remain = group[~group['id'].isin(list_affinity)]
        group_remain = group_remain.sort_values('Visits', ascending = False)
        group_remain_length = len(group_remain)
        
        list_remain = []

        if group_remain_length < n_popular + n_random:#+n_affinity + n_calculator
            list_popular = group_remain['id'].values
        else:
            popular_index = group_remain.index.values[ : n_popular]
            random_index = np.random.choice(group_remain.index.values[n_popular : ], n_random, replace = False)

            list_remain.append(popular_index.astype(int))
            list_remain.append(random_index.astype(int))
            # for idx in popular_index:
            #     list_remain = 

            # for idx in random_index:
            #     recommendations += str(int(group[group.index == idx]['id'])) + ','

        recommendations = str(np.array(list_affinity).astype(int)) + ','
        for idx in list_remain:
            recommendations += str(idx) + ','
        # for idx in list_remain:
        #     recommendations += str(idx) + ','

        f.write('%s,"%s","%s"\n' % (str(int(row['id'])), row['Title'], recommendations[0 : -1]))
    except KeyError as err:
        print 'Could not find parent for article id ' + str(int(row['id']))
        f.write('%s,"%s","Missing parent id"\n' % (str(int(row['id'])), row['Title']))
 
f.close()