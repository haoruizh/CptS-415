import collections
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import csv

# Load relevant files into dataFrame
file1 = 'ID_TITLE.csv'
itemsf = pd.read_csv(file1)
#itemsf.columns = ['number', 'title']
file2 = 'ID_USERID_RATING.csv'
rating = pd.read_csv(file2)
#rating.columns = ['number', 'title', 'avg_rating', 'customer']

# Created a nested dictionary of each user with the itemid and the ratings they provided
gettedItem = collections.defaultdict(dict)
for i in rating.values.tolist():
    gettedItem[i[0]][i[1]] = i[2]

# Create a pivot table with index as userId, columns as itemid, values as rating
rate_P = rating.pivot(index='userID', columns = 'Id', values='ratings').fillna(0)
# Convert the pivot table into a sparse matrix
matr_rate = csr_matrix(rate_P.values)

# Initialise k nearest neighbours
k_n_n = NearestNeighbors(metric = 'cosine', algorithm = 'auto')
k_n_n.fit(matr_rate)

k = 20

while True:
    # Get user input for the user id
    user = int(input('User id:'))
    user_index = user - 1

    # Find nearest neighbours, get distance and indices
    distance, ids = k_n_n.kneighbors(rate_P.iloc[user_index, :].values.reshape(1, -1), n_neighbors = k)

    # items the user has getted before
    user_getted = set(gettedItem[rate_P.index[user_index]])

    nb_getted = {}

    # Print neighbours and their distance from the user
    for i in range(0, len(distance.flatten())):
        # if i == 0:
        #     print('Closest users to user {}:\n'.format(rate_P.index[user_index]))

        # else:
        #     print('{0}: {1} - distance: {2}'.format(i, rate_P.index[ids.flatten()[i]], distance.flatten()[i]))

        nb_getted[rate_P.index[ids.flatten()[i]]] = gettedItem[rate_P.index[ids.flatten()[i]]].copy()

        # Save information in order to calculate predicted rating
        for key, v in nb_getted[rate_P.index[ids.flatten()[i]]].items():
            nb_getted[rate_P.index[ids.flatten()[i]]][key] = [1 - distance.flatten()[i], v]
    print('----\n')

    notgetted_items = []
    for u in nb_getted:
        a = nb_getted[u].keys() - user_getted.intersection(nb_getted[u].keys())
        for f in a:
            notgetted_items.append(f)

    # Find didnt getted itmes that are common among neighbours
    recom_notGet = [item for item, count in collections.Counter(notgetted_items).items() if count > 1]

    # Predict rating the user would give for the didnt getted items
    recom_notGet_rate = []
    for f in recom_notGet:
        i = []
        g = []

        for u in nb_getted:
            if nb_getted[u].get(f) is not None:
                i.append(nb_getted[u].get(f)[0]*nb_getted[u].get(f)[1])
                g.append(nb_getted[u].get(f)[0])

        recom_notGet_rate.append([np.sum(i)/np.sum(g), f])
    recom_notGet_rate = sorted(recom_notGet_rate, reverse=True)

    print('10 best recommendations based on what similar users liked:\n')
    for f in recom_notGet_rate[:10]:
        #itemid and title 
        print('{0} - {1} - {2:.2f}'.format(f[1], itemsf.loc[itemsf['Id'] == f[1]]['title'].values[0], f[0]))
    print('-----\n')