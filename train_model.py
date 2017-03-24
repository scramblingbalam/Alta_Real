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
    
#for thread in event_feature_dic['ebola-essien']:
#    print "\n\n",thread,len(thread)
#    for i in thread:
#        print "\t",i,type(i),len(i)
  
event_target_dic ={}
with open("event_target_dic","r")as modelfile:
    event_target_dic =pickle.load(modelfile)
      
for k in event_target_dic:
    print k
    
X_train = event_feature_dic["ferguson"]
y_train = event_target_dic["ferguson"]

model = GraphCRF(directed=True, inference_method="ad3")

ssvm = learners.FrankWolfeSSVM(model=model, max_iter=5000, C=1)
ssvm.fit(X_train, y_train)
y_pred = ssvm.predict(X_train)

for pred, test in zip(y_pred,y_train):
    print pred,test,"pred"

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