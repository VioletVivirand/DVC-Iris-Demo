import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import os

iris = pd.read_hdf(sys.argv[1], key='data')

split = 0.8

X = iris.iloc[:, :-1]
y = iris.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=1337)

X_train.to_hdf(os.path.join(sys.argv[2], 'train.h5'), key='X')
X_test.to_hdf(os.path.join(sys.argv[2], 'test.h5'), key='X')
y_train.to_hdf(os.path.join(sys.argv[2], 'train.h5'), key='y')
y_test.to_hdf(os.path.join(sys.argv[2], 'test.h5'), key='y')
