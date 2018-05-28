import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/slu/Desktop/Recommendation.csv")
grouped = df.groupby('Parent')
n_popular = 2
n_random = 7
#n_popular = 3
#n_random = 1
#n_affinity = 4
#n_calculator = 1


group = grouped.get_group(25)
affinity = [22542, 22558, 12345]
print group[~group['id'].isin(affinity)]



# f = open("C:/Users/slu/Desktop/output.txt", "w+")
# f.write("id,Title,Recommendation\n")


# for index, row in df.iterrows():
#     if np.isnan(row['id']):
#         continue

#     i = 0
#     try:
#         group = grouped.get_group(row['Parent'])
#         group = group[group['id'] != row['id']] #remove current article from the group

#         recommendations = ''
#         group_length = len(group.index.values)
#         if group_length < n_popular + n_random:#+n_affinity + n_calculator
#             for id, recommendation in group.iterrows():
#                 recommendations += str(int(recommendation['id'])) + ','
#         else:
#             popular_index = group.index.values[ : n_popular]
#             random_index = np.random.choice(group.index.values[n_popular : ], n_random, replace = False)

#             for idx in popular_index:
#                 recommendations += str(int(group[group.index == idx]['id'])) + ','

#             for idx in random_index:
#                 recommendations += str(int(group[group.index == idx]['id'])) + ','

#         f.write('%s,"%s","%s"\n' % (str(int(row['id'])), row['Title'], recommendations[0 : -1]))
#     except KeyError as err:
#         print 'Could not find parent for article id ' + str(int(row['id']))
#         f.write('%s,"%s","Missing parent id"\n' % (str(int(row['id'])), row['Title']))
 
# f.close()