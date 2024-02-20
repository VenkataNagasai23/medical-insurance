# -*- coding: utf-8 -*-
"""insurance.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bCelyUJrXm8qEycCyLZ20IX_ovBmztsp
"""

# first machine learning model with sklearn tutorial
from numpy import loadtxt
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import numpy as np

# load the dataset
dataset = pd.read_csv("insurance.csv")
from sklearn.preprocessing import LabelEncoder

for c in dataset.columns:
    if dataset[c].dtype=='object':
        lbl = LabelEncoder()
        lbl.fit(list(dataset[c].values))
        dataset[c] = lbl.transform(dataset[c].values)


X = dataset.drop(['charges','region'], axis = 1)
y= dataset['charges']


display(dataset.head())

dataset.info()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=42)



X_train

sex = {'male': 1,'female': 2}

from sklearn import preprocessing

le = preprocessing.LabelEncoder()
dataset.smoker = le.fit_transform(dataset.smoker)
dataset.sex = le.fit_transform(dataset.sex)
dataset.region = le.fit_transform(dataset.region)
dataset

dataset

from sklearn.preprocessing import Normalizer
from sklearn.linear_model import LinearRegression


normalizer = Normalizer()
X = normalizer.fit_transform(X_train)
model = LinearRegression().fit(X, y_train)
X1=normalizer.fit_transform(X_test)

dataset

print ("R squared score on training data: ", model.score(X, y_train))
print ("R squared score on test data: ", model.score(X1, y_test))

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

lr = LinearRegression()
dt= DecisionTreeRegressor(max_depth = 3)
rf= RandomForestRegressor(max_depth = 3, n_estimators=500)
xgb= XGBRegressor(max_depth = 3, n_estimators=50, learning_rate =.2)
regressors= [('Linear Regression', lr),('Decision Tree', dt), ('Random Forest', rf), ('XGBoost', xgb)]

from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
for regressor_name, regressor in regressors:

    regressor.fit(X_train, y_train)


    y_pred = regressor.predict(X_test)
    accuracy = round(r2_score(y_test,y_pred),2)*100



    print('{:s} : {:.0f} %'.format(regressor_name, accuracy))
    plt.rcParams["figure.figsize"] = (20,8)
    plt.bar(regressor_name,accuracy)

from sklearn.metrics import r2_score, f1_score
import matplotlib.pyplot as plt

for regressor_name, regressor in regressors:
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    r2_acc = round(r2_score(y_test, y_pred), 2) * 100
    f1_acc = round(f1_score(y_test > 0, y_pred > 0), 2) * 100
    print('{:s} - R2 score: {:.0f}%, F1 score: {:.0f}%'.format(regressor_name, r2_acc, f1_acc))
    plt.rcParams["figure.figsize"] = (20, 8)
    plt.bar(regressor_name, r2_acc, label='R2 score')
    plt.bar(regressor_name, f1_acc, label='F1 score')
    plt.legend()

from sklearn.model_selection import GridSearchCV

# Define hyperparameters for each regressor
lr_params = {'fit_intercept': [True, False]}
dt_params = {'max_depth': [3, 5, 7]}
rf_params = {'max_depth': [3, 5, 7], 'n_estimators': [100, 500, 1000]}
xgb_params = {'max_depth': [3, 5, 7], 'n_estimators': [50, 100, 500], 'learning_rate': [0.1, 0.2, 0.3]}

# Create a dictionary of regressors and their respective hyperparameters
regressors = {'Linear Regression': (LinearRegression(), lr_params),
              'Decision Tree': (DecisionTreeRegressor(), dt_params),
              'Random Forest': (RandomForestRegressor(), rf_params),
              'XGBoost': (XGBRegressor(), xgb_params)}

# Iterate through each regressor and find the best hyperparameters using GridSearchCV
for regressor_name, (regressor, params) in regressors.items():
    grid = GridSearchCV(regressor, params, cv=5, scoring='r2')
    grid.fit(X_train, y_train)
    best_params = grid.best_params_
    print(regressor_name, "best parameters:", best_params)

    # Fit the regressor with the best hyperparameters
    best_regressor = regressor.set_params(**best_params)
    best_regressor.fit(X_train, y_train)
    y_pred = best_regressor.predict(X_test)
    accuracy = round(r2_score(y_test,y_pred),2)*100
    print('{:s} : {:.0f} %'.format(regressor_name, accuracy))
    plt.rcParams["figure.figsize"] = (20,8)
    plt.bar(regressor_name,accuracy)

import os
import sys
import pickle

projectabspathname = os.path.abspath('insurance.pickle')
print(projectabspathname)
projectname = 'insurance.ipynb'
projectpickle = open(str(projectabspathname),'wb')
pickle.dump(projectname, projectpickle)
projectpickle.close()

from joblib import dump, load

# Save the model
dump(model, 'insurance.joblib')

# Load the model
model = load('insurance.joblib')

