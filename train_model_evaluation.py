# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 22:06:20 2017

@author: scram
"""
import numpy as np
from pystruct.models import GraphCRF
import pystruct.learners as learners
import cPickle as pickle
import evaluation
from feature_creation_mongo import translatelabel
from feature_functions import inverse_label
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
feature_list = []
event_feature_dic ={}
with open("event_model_dic","rb")as modelfile:
    feature_list =pickle.load(modelfile)
    
#print type(feature_list)
#print len(feature_list)
feature_string = feature_list[0]
event_feature_dic = feature_list[1]
         


event_target_dic ={}
with open("event_target_dic","rb")as modelfile:
    event_target_dic = pickle.load(modelfile)
  
event_ID_dic = {}  
  
with open("event_ID_dic","rb")as modelfile:
    event_ID_dic = pickle.load(modelfile)

print event_feature_dic.keys() 
print event_target_dic.keys()   
X_train = event_feature_dic['ebola-essien']
y_train = event_target_dic['ebola-essien']


#X_train = event_feature_dic['Big_win_in_the_House_-_ve']
#y_train = event_target_dic['Big_win_in_the_House_-_ve']
#id_train = event_ID_dic['Big_win_in_the_House_-_ve']

#X_train = event_feature_dic['WeeklyAddress\U0001f1fa\U0001f1f8_http']
#y_train = event_target_dic['WeeklyAddress\U0001f1fa\U0001f1f8_http']


model = GraphCRF(directed=True, inference_method="ad3")

ssvm = learners.FrankWolfeSSVM(model=model, max_iter=5000, C=1)
ssvm.fit(X_train, y_train)
y_pred = ssvm.predict(X_train)

for pred, test in zip(y_pred,y_train):
    for p,t in zip(pred,test):
        print inverse_label(p),inverse_label(t) 

y_train_flat = [i for I in y_train for i in I]
y_pred_flat = [i for I in y_pred for i in I]
test_acc = accuracy_score(y_train_flat, y_pred_flat, normalize=True, sample_weight=None)
print test_acc

classifier = 'treecrf'
featurename = feature_string.split("_")

id_preds = {}
id_gts = {}
print(event_ID_dic.keys())
#for k in ['ebola-essien']:
for k in event_target_dic:
    print(k)
    test_event = k 
    train_events = set(event_target_dic.keys()) - set([k])
    X_train = [thread1 for event1 in train_events 
                           for thread1 in event_feature_dic[event1]]
    y_train = [thread2 for event2 in train_events 
                           for thread2 in event_target_dic[event2]]
    ids_train = [thread3 for event3 in train_events 
                             for thread3 in event_ID_dic[event3]]
    
    X_test = event_feature_dic[test_event]
    y_test = event_target_dic[test_event]
    ids_test = event_ID_dic[test_event]
    
    classcounts = [0, 0, 0, 0]
    for tree in y_train:
        bincount = np.bincount(tree)
        for i in range(0, 4):
            if len(bincount) > i:
                classcounts[i] += bincount[i]
                
    classweights = [np.amin(classcounts) / float(x) for x in classcounts]

    model = GraphCRF(directed=True, inference_method="ad3")

    ssvm = learners.FrankWolfeSSVM(model=model, max_iter=5000, C=1)

    ssvm.fit(X_train, y_train)
    y_pred = ssvm.predict(X_test)
    
#    y_pred = y_test

    acc = 0
    items = 0
#    print ids_test[0]
#    print y_test[0]
#    print X_test[0]
    for k, thread_ids in enumerate(ids_test):
#        print k
        thread_gts = y_test[k]
#        print thread_gts
        thread_preds = y_pred[k]
        for m, tweetid in enumerate(thread_ids):
            if not int(tweetid) in id_preds:
                if thread_preds[m] == 4:
                    thread_preds[m] = 3
                
                id_preds[int(tweetid)] = thread_preds[m]
                id_gts[int(tweetid)] = thread_gts[m]
                
                items += 1
                if thread_preds[m] == thread_gts[m]:
                    acc += 1

    if items > 0:
        print(feature_string + ': ' + str(float(acc) / items))

print(feature_list[0],"feature-list")
#print(event_target_dic.keys(),"TARGET_dic")
#print(event_ID_dic.keys(),"ID_dic")
evaluation.evaluate(id_preds, id_gts, classifier, featurename)

joblib.dump(ssvm,"tCRF_"+"_"+classifier+"_"+"_".join(featurename)+".crf_model")