# -*- coding: utf-8 -*-
"""Soft SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u_0B63co7b6NSPx9eGqupN30R4aQhj2m
"""

import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

#reading sample dataset
df = pd.read_csv("Iris.csv")

#extracting the features from dataset
features = df.iloc[:,1:-1].replace(math.nan,0)

#extracting labels 
labels = df.iloc[:,-1:].replace(0,-1)

#converting features and labels to matrix form
fvector = np.array(features)
lvector = np.array(labels)

#calculating number of features per example
featuresSize = features.shape[1]

#data split into test and training data
splitPercent = [0.3,0.2,0.1]

print("Enter the value of regularisation parameter: ")
c = float(input())

for percent in splitPercent:
  xtrain, xtest, y_train, y_test = train_test_split(fvector, lvector, test_size= percent,shuffle= True)

  #feature scaling for test and training inputs
  
  sc_x = StandardScaler() 
  X_train = sc_x.fit_transform(xtrain)  
  X_test = sc_x.transform(xtest)

  classifier = SVC(kernel='rbf') 
  classifier.fit(X_train, y_train.ravel())

  y_pred = classifier.predict(X_test)
 # print("indices of support vectors: ",classifier.support_)
  print("number of support vectors: ",classifier.support_.shape[0])

  misclassified=0
  for i in range(0,y_test.shape[0]):
    if y_test[i][0] != y_pred[i]:
      misclassified+= 1

  totalCases=X_test.shape[0]
  print("Efficiency for",int((1-percent)*100),":",
        int(percent*100),"split is: ",round((1-misclassified/totalCases)*100,2),"%")
