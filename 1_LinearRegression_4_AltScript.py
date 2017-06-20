#!python3

import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import datetime

style.use('ggplot')

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

# Creating numpy array for features and label to be used with sklearn
# Features numpy array
X = np.array(df.drop(['label'], 1))
# Scale features with preprocessing
X = preprocessing.scale(X)
# Forecasting feature set
X_lately = X[-forecast_out:]
# Feature set for training and testing
X = X[:-forecast_out]

# Label numpy array
# Cleaning the data to removing NaN created from above label column shift
#df.dropna(inplace=True)
y = np.array(df['label'])
y = y[:-forecast_out]
# Creating training and test data with cross_validation
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

# LinearRegression
clf = LinearRegression(n_jobs=-1) # Multi-threading the algorithm
clf.fit(X_train, y_train) # Training the classifier
confidence = clf.score(X_test, y_test) # Scoring the classifier
print("LinearRegression: ", confidence)

# Forecasting with trained classifier in X_lately feature set
forecast_set = clf.predict(X_lately)
# Creating a forcast column and filling it with NaN for the current dataframe values/dates
df['Forecast'] = np.nan

# Getting the last date in the data frame and creating next date values
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 24*60*60
next_unix = last_unix - (one_day * forecast_out)
# Populating the dataframe with predicted label values with appropritate future dates and rest as NaN
for i in forecast_set:
	try:
		next_date = datetime.datetime.fromtimestamp(next_unix)
		next_unix += one_day
		#df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]
		df.loc[next_date] = df.loc[next_date].drop(['Forecast']) + [i]
	except:
		pass

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()


