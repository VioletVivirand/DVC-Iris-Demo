import sys
import pandas as pd
from sklearn import preprocessing
import os

# Load Iris dataset
iris = pd.read_csv(sys.argv[1])

# Build Label Encoder
le = preprocessing.LabelEncoder()
le.fit(['setosa', 'versicolor', 'virginica'])
# Transform Target
iris['Species'] = le.transform(iris['Species'])

# Export to /data/features/iris.data
iris.to_hdf(sys.argv[2], key='data')
