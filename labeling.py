# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 14:40:17 2017

@author: scram
"""
import json
import numpy as np
from pystruct.models import GraphCRF
import pystruct.learners as learners
import cPickle as pickle
import evaluation
from pymongo import MongoClient
from feature_creation_mongo import translatelabel
import feature_functions as feature
from sklearn.externals import joblib
from collections import Counter
import time
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

doc2vec_dir ="Data/doc2vec/not_trump"
classifier = 'treecrf'
featurename = feature_string.split("_")
token_type = featurename[0]
with open(doc2vec_dir+token_type+"_"+"id_text_dic.json",'r')as corpfile:
    sent_dic = json.load(corpfile)


DBname = 'Alta_Real_New'
DBhost = 'localhost'
DBport = 27017
DBname_t = 'semeval2017'
    
# initiate Mongo Client
client = MongoClient()
client = MongoClient(DBhost, DBport)
DB_trump = client[DBname]
DB_train = client[DBname_t]


model = joblib.load("tCRF_"+"_"+classifier+"_"+"_".join(featurename)+".crf_model")
test_id = 856172056932700164L#862135824745467905L
def label_tweet(tweet,root_tweet,pred,db):
    print(tweet.get('predicted',None),"predicted")
    print(tweet.get('label',None),"label")
    sID = tweet['_id']
    if root_tweet == tweet:
        print("Is tweet supporting or denying claim")
        collection = db.trump_tweets
    else:
        collection = db.replies_to_trump
        print(root_tweet['text'])
    print("\n")
    print(sID)
#   print(tweet['user']['screen_name'])
    text = tweet['text']
    print(text)
    print(pred)
    collection.update_one(
            {'_id':sID},
            {'$set':{'predicted':pred}})
    try:
        label=int(input("1=support  2=deny  3=query  4=comment\n>>\t"))-1
    except:
        print("EXCEPTION")
        label = None
    if isinstance(label,int):
        collection.update_one(
                {'_id':sID},
                {'$set':{'label':feature.inverse_label(label)}})
    print(feature.inverse_label(label))
    time.sleep(0.25)
    print("\n_____________________")

def label_thread(thread_id,DB): 
    preds = model.predict(event_feature_dic[thread_id])
    preds = map(feature.inverse_label,preds[0])
    root = list(DB.trump_tweets.find({'_id':thread_id}))[0]
    for predicted,sID in zip(preds,event_ID_dic[thread_id][0]):
        twt = list(DB.replies_to_trump.find({'_id':sID}))
        if not twt:
            twt = list(DB.trump_tweets.find({'_id':sID}))
        twt =twt[0]
        if not twt.get('label',None):
            label_tweet(twt,root,predicted,DB)
        
    print("THREAD LABELED!!!!")

label_thread(test_id,DB_trump)
        

### working list of threads for labeling
train =[
860477328882905089,#Win in house for 16244
860580764944969728,#weekly address 6497
860577873060651008# JOBS, JOBS, JOBS! https://t.co/UR0eetSEnO 9379
]


