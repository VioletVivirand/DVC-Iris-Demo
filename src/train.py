import sys
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

X_train = pd.read_hdf(sys.argv[1], key='X')
y_train = pd.read_hdf(sys.argv[1], key='y')

clf = RandomForestClassifier(n_estimators=100,
                             max_depth=3,
                             random_state=1337)

clf.fit(X_train, y_train)
dump(clf, os.path.join(sys.argv[2], 'model.joblib'))
