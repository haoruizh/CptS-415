import collections
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import csv

# Load relevant files into dataFrame
file1 = 'tryInput1.csv'
film = pd.read_csv(file1)
#film.columns = ['number', 'title']
file2 = 'tryInput.csv'
rating = pd.read_csv(file2)
#rating.columns = ['number', 'title', 'avg_rating', 'customer']

# Created a nested dictionary of each user with the itemid and the ratings they provided
gettedItem = collections.defaultdict(dict)
for i in rating.values.tolist():
    gettedItem[i[0]][i[1]] = i[2]

# Create a pivot table with index as userId, columns as itemid, values as rating
rating_pivot = rating.pivot(index='customer', columns = 'number',\
                    values='avg_rating').fillna(0)
# Convert the pivot table into a sparse matrix
rating_matrix = csr_matrix(rating_pivot.values)

# Initialise k nearest neighbours
knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
knn.fit(rating_matrix)

k = 20

while True:
    # Get user input for the user id
    user = int(input('User id:'))
    user_index = user - 1

    # Find nearest neighbours
    distances, indices = knn.kneighbors(rating_pivot.iloc[user_index, :]\
                        .values.reshape(1, -1), n_neighbors = k)

    # items the user has getted before
    user_getted = set(gettedItem[rating_pivot.index[user_index]])

    neighbours_getted = {}

    # Print neighbours and their distance from the user
    for i in range(0, len(distances.flatten())):
        if i == 0:
            print('Closest users to user {}:\n'.format(rating_pivot.index[user_index]))

        else:
            print('{0}: {1} - distance: {2}'.format(i, rating_pivot.index[indices.flatten()[i]], distances.flatten()[i]))

        neighbours_getted[rating_pivot.index[indices.flatten()[i]]] = gettedItem[rating_pivot.index[indices.flatten()[i]]].copy()

        # Save information in order to calculate predicted rating
        for key, v in neighbours_getted[rating_pivot.index[indices.flatten()[i]]].items():
            neighbours_getted[rating_pivot.index[indices.flatten()[i]]][key] = [1 - distances.flatten()[i], v]
    print('----\n')

    ungetted_items = []
    for u in neighbours_getted:
        a = neighbours_getted[u].keys() - user_getted.intersection(neighbours_getted[u].keys())
        for f in a:
            ungetted_items.append(f)

    # Find didnt getted itmes that are common among neighbours
    common_ungetted = [item for item, count in collections.Counter(ungetted_items).items() if count > 1]

    # Predict rating the user would give for the didnt getted items
    common_ungetted_rating = []
    for f in common_ungetted:
        i = []
        g = []

        for u in neighbours_getted:
            if neighbours_getted[u].get(f) is not None:
                i.append(neighbours_getted[u].get(f)[0]*neighbours_getted[u].get(f)[1])
                g.append(neighbours_getted[u].get(f)[0])

        common_ungetted_rating.append([np.sum(i)/np.sum(g), f])
    common_ungetted_rating = sorted(common_ungetted_rating, reverse=True)

    print('10 best recommendations based on what similar users liked:\n')
    for f in common_ungetted_rating[:10]:
        print('{0} - {1} - {2:.2f}'.format(f[1], film.loc[film['number'] == f[1]]['title'].values[0], f[0]))
    print('-----\n')