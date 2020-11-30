import collections
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import csv

# Load relevant files into dataFrame
file = 'haha/tryInput2.csv'
# film = pd.read_csv(file)

import chardet
with open(file, 'rb') as rawdata:
    result = chardet.detect(rawdata.read(100000))
result