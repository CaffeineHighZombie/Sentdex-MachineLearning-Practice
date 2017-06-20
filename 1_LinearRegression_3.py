#!python3

import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

# Getting google's daily stock prices from quandl as a dataframe
df = quandl.get("WIKI/GOOGL")

# Feature selection and engineering
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

# Defining forecast column and cleaning the data
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(df)))

# Creating label column with forecast_out based future value
df['label'] = df[forecast_col].shift(-forecast_out)
# Cleaning the data to removing NaN created from above label column shift
df.dropna(inplace=True)

# Creating numpy array for features and label to be used with sklearn
# Features numpy array
X = np.array(df.drop(['label'], 1))
# Scale features with preprocessing
X = preprocessing.scale(X)
# Label numpy array
y = np.array(df['label'])

# Creating training and test data with cross_validation
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

# Training and scoring with both LinearRegression and svm.SVR (and its contituent kernels) 
# for comparison of model accuracy and also, to see how easy it is to switch between classifiers in Scikit-Learn
# LinearRegression
clf = LinearRegression(n_jobs=-1) # Multi-threading the algorithm
clf.fit(X_train, y_train) # Training the classifier
confidence = clf.score(X_test, y_test) # Scoring the classifier
print("LinearRegression: ", confidence)
# Support Vector Regression
for k in ['linear', 'poly', 'rbf', 'sigmoid']:
	clf = svm.SVR(kernel=k)
	clf.fit(X_train, y_train)
	confidence = clf.score(X_test, y_test)
	print("SupportVectorRegression - ", k, ": ", confidence)

