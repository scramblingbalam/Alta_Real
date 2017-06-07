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
    print(tweet.get('label_parent',None),"label_parent")
    sID = tweet['_id']
    if root_tweet == tweet:
        print("\n________________________________________")
        print("Tweet is Root stance to claim")
        collection = db.trump_tweets
    else:
        collection = db.replies_to_trump
        print("\n________________________________________")
        print(root_tweet['_id'])
        print(root_tweet['text'])
    parent_id = tweet.get('in_reply_to_status_id',None)
    parent_not_root = parent_id != root_tweet['_id'] and tweet['user']['screen_name'] != 'realDonaldTrump' 
                        
    
    if parent_not_root:
        parent_tweet = list(db.replies_to_trump.find({'_id':parent_id}))[0]
        print("|\n|")
        print(parent_tweet['_id'])
        print(parent_tweet['text'])
        
#    print("\n")

#   print(tweet['user']['screen_name'])
    text = tweet['text']
    print("|\n|")
    print(sID)
    print(text)
#    print(pred)
#    print(tweet['in_reply_to_status_id'],root_tweet['_id'])
#    print(tweet['user']['screen_name'])
#    print(tweet['created_at'])
    collection.update_one(
            {'_id':sID},
            {'$set':{'predicted':pred}})
    try:
        label=int(input("Stance to Root\n1=support  2=deny  3=query  4=comment\n>>\t"))-1
    except:
        print("EXCEPTION")
        label = None
    if isinstance(label,int):
        if tweet['in_reply_to_screen_name'] == 'realDonaldTrump':
            collection.update(
                    {'text':text},
                    {'$set':{'label':feature.inverse_label(label)}},
                    upsert=False,
                    multi=True
                    )
            collection.update(
                    {'text':text},
                    {'$set':{'label_parent':feature.inverse_label(label)}},
                    upsert=False,
                    multi=True
                    )
        else:
            collection.update_one(
                {'_id':sID},
                {'$set':{'label':feature.inverse_label(label)}})
    print(feature.inverse_label(label))
    time.sleep(0.25)
    if parent_not_root:
        try:
            label_parent=int(input("Stance to Parent\n1=support  2=deny  3=query  4=comment\n>>\t"))-1
        except:
            print("EXCEPTION")
            label_parent = None
    elif parent_id == root_tweet['_id']:
        label_parent = label
    if isinstance(label_parent,int):
        collection.update_one(
                {'_id':sID},
                {'$set':{'label_parent':feature.inverse_label(label_parent)}})
    time.sleep(0.5)
#    print("\n________________________________________")

def label_thread(thread_id,DB): 
    preds = model.predict(event_feature_dic[thread_id])
    preds = map(feature.inverse_label,preds[0])
    root = list(DB.trump_tweets.find({'_id':thread_id}))[0]
    for predicted,sID in zip(preds,sorted(event_ID_dic[thread_id][0])):
        twt = list(DB.replies_to_trump.find({'_id':sID}))
        if not twt:
            twt = list(DB.trump_tweets.find({'_id':sID}))
        twt =twt[0]
#        if not twt.get('label',None) and twt.get('in_reply_to_status_id',None)!= root['_id']:
        if not twt.get('label',None) or not twt.get('label_parent',None):
                label_tweet(twt,root,predicted,DB)
        
    print("THREAD LABELED!!!!")
        

### working list of threads for labeling
train = [
860477328882905089,#Win in house for 16244
860580764944969728,#weekly address 6497
860577873060651008# JOBS, JOBS, JOBS! https://t.co/UR0eetSEnO 9379
]

label_thread(train[0],DB_trump)

