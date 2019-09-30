import sys
from joblib import load
import pandas as pd
import os

clf = load(sys.argv[1])

X_test = pd.read_hdf(sys.argv[2], key='X')
y_test = pd.read_hdf(sys.argv[2], key='y')

score = clf.score(X_test, y_test)

with open(sys.argv[3], 'w') as file:
    file.write('{}'.format(score))
