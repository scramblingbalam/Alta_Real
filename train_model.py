# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:59:51 2017

@author: scram
"""
import numpy as np
from pystruct.models import GraphCRF
import pystruct.learners as learners
import cPickle as pickle

event_feature_dic ={}
with open("event_model_dic","r")as modelfile:
    event_feature_dic =pickle.load(modelfile)

            
print len(event_feature_dic['ebola-essien'])
  
thread = event_feature_dic['ebola-essien'][0]
feats = thread[0]
edges = thread[1]
print feats.shape
print feats
print edges.shape

event_target_dic ={}
with open("event_target_dic","r")as modelfile:
    event_target_dic =pickle.load(modelfile)
      
for k in event_target_dic:
    print k
    
X_train = event_feature_dic['ebola-essien']
y_train = event_target_dic['ebola-essien']

model = GraphCRF(directed=True, inference_method="ad3")

ssvm = learners.FrankWolfeSSVM(model=model, max_iter=5000, C=1)
ssvm.fit(X_train, y_train)
y_pred = ssvm.predict(X_train)

for pred, test in zip(y_pred,y_train):
    for p,t in zip(pred,test):
        print p,t

#X_train = [featuregeneration.tree2featuresfromfile(th, dataset, features) for th in train_threads]
#y_train = [featuregeneration.tree2labels(th) for th in train_threads]
#ids_train = [featuregeneration.tree2ids(th) for th in train_threads]
#
#X_test = [featuregeneration.tree2featuresfromfile(th, dataset, features) for th in test_threads]
#y_test = [featuregeneration.tree2labels(th) for th in test_threads]
#ids_test = [featuregeneration.tree2ids(th) for th in test_threads]
#
#model = GraphCRF(directed=True, inference_method="ad3")
#
#ssvm = learners.FrankWolfeSSVM(model=model, max_iter=5000, C=1)
#ssvm.fit(X_train, y_train)
#y_pred = ssvm.predict(X_test)