# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 14:40:17 2017

@author: scram
"""
import json
import cPickle as pickle
from pymongo import MongoClient
from feature_creation_mongo import translatelabel
import feature_functions as feature
from sklearn.externals import joblib
from collections import Counter
import time
### open borwser
import webbrowser
import subprocess
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
feature_list = []
event_feature_dic ={}
#with open("event_model_dic","rb")as modelfile:
#    feature_list =pickle.load(modelfile)
feature_list = joblib.load("event_model_dic.jonlib")
    
#print type(feature_list)
#print len(feature_list)
feature_string = feature_list[0]
event_feature_dic = feature_list[1]
doc2vec_dir ="Data/doc2vec/not_trump"
classifier = 'treecrf'
featurename = feature_string.split("_")
token_type = featurename[0]

### get pos tags # commented out since I'm getting urls from tweet json
#POS_dir ="Data\\twitIE_pos\\"        
#pos_file_path1 = POS_dir+token_type+"_semeval2017"+"_twitIE_POS"
#pos_file_path2 = POS_dir+token_type+"_Alta_Real_New"+"_twitIE_POS"
#pos_file_path = [pos_file_path1, pos_file_path2]
#id_pos_dic, index_pos_dic = feature.pos_extract(pos_file_path) 

event_target_dic ={}
#with open("event_target_dic","rb")as modelfile:
#    event_target_dic = pickle.load(modelfile)
event_target_dic = joblib.load("event_target_dic.jonlib")  
event_ID_dic = {}  
  
#with open("event_ID_dic","rb")as modelfile:
#    event_ID_dic = pickle.load(modelfile)
event_ID_dic = joblib.load("event_ID_dic.jonlib")

with open(doc2vec_dir+token_type+"_"+"id_text_dic.json",'r')as corpfile:
    sent_dic = json.load(corpfile)

import httplib
import urlparse

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url


DBname = 'Alta_Real_New'
DBhost = 'localhost'
DBport = 27017
DBname_t = 'semeval2017'
    
# initiate Mongo Client
client = MongoClient()
client = MongoClient(DBhost, DBport)
DB_trump = client[DBname]
DB_train = client[DBname_t]

def image_lookup(photo_url):
    filePath =photo_url
#    filePath = '/mnt/Images/test.png'
    searchUrl = "https://www.google.com/searchbyimage?&image_url="
#    searchUrl = 'http://www.google.hr/searchbyimage/upload'
#    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
#    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    request = searchUrl+photo_url
    print(request)
    response = requests.get(request, allow_redirects=False)
    fetchUrl = response.headers['Location']
    webbrowser.open(fetchUrl)

def print_tweet(Tweet):
        tweet_info = str(Tweet['_id'])+"  "+Tweet['user']['screen_name']+"  "+str(Tweet.get('label',''))
        print(tweet_info)
        text = Tweet['text']
        print(text)
#        pos = map(lambda x:index_pos_dic[x],id_pos_dic[Tweet['_id']])
        if Tweet.get('entities',None):
#            time.sleep(3)
            if Tweet['entities'].get('media',None):
                for num,media in enumerate(Tweet['entities']['media']):
                    print(media['type'])
                    if num == 0:
                        time.sleep(2)
                    else:
                        time.sleep(4)
                    webbrowser.open_new(media['media_url_https'])
            if Tweet['entities'].get('urls',None):
                for num,URL in enumerate(Tweet['entities']['urls']):
                    print(URL['display_url'])
                    if num == 0:
                        time.sleep(2)
                    else:
                        time.sleep(4)
                    webbrowser.open_new(URL['expanded_url'])  
        
#        if u'URL' in pos:
#            url_count = Counter(pos)['URL']
#            index = pos.index(u'URL')
#            url = text.split()[index]
#            print(unshorten_url(url))
#            webbrowser.open_new(url)
#            print("URLS")
#            print Tweet['entities']['urls']
#            print("media")
#            if Tweet['entities']['media']:
#                for media in Tweet['entities']['media']:
#                    print("MEDIA_TYPE",media['type'])
#                    if media['type'] == 'photo':
#                        image_lookup(media['media_url_https'])
#                    
#            print Tweet['entities']['media']
            
#            p = subprocess.Popen(["firefox", url])
#            time.sleep(5) #delay of 10 seconds
#            p.kill()
#            driver = webdriver.Chrome()
#            driver.get(url)
#            time.sleep(3)
#            driver.close()
            
model = joblib.load("tCRF_"+"_"+classifier+"_"+"_".join(featurename)+".crf_model")
test_id = 856172056932700164L#862135824745467905L

def label_tweet(tweet,root_tweet,pred,db,Done_prec):
#    print(tweet.get('predicted',None),"predicted")
#    print(tweet.get('label',None),"label")
#    print(tweet.get('label_parent',None),"label_parent")
    sID = tweet['_id']
    if root_tweet == tweet:
        print("\n________________________________________")
        print("Tweet is Root stance to claim")
        collection = db.trump_tweets
    else:
        collection = db.replies_to_trump
        print("\n________________________________________")
        print_tweet(root_tweet)
    parent_id = tweet.get('in_reply_to_status_id',None)
    parent_not_root = parent_id != root_tweet['_id'] and tweet['user']['screen_name'] != 'realDonaldTrump' 
                        
    
    if parent_not_root:
        parent_tweet = list(db.replies_to_trump.find({'_id':parent_id}))[0]
        if parent_tweet["in_reply_to_status_id"] != root_tweet['id']:
            print("|\n||||||||||||||||\n|")
        else:
            print("|\n|")
        print_tweet(parent_tweet)
#    print("\n")

#   print(tweet['user']['screen_name'])
    print("|\n|")
    print_tweet(tweet)
#    print(pos_tweet.index('url'))
#    print(pred)
#    print(tweet['in_reply_to_status_id'],root_tweet['_id'])
#    print(tweet['user']['screen_name'])
#    print(tweet['created_at'])
    collection.update_one(
            {'_id':sID},
            {'$set':{'predicted':pred}})
    try:
        label=int(input("\nStance to Root\n1=support  2=deny  3=query  4=comment\n>>\t"))-1
    except:
        print("EXCEPTION")
        label = None
    if isinstance(label,int):
        if tweet['in_reply_to_screen_name'] == 'realDonaldTrump':
            collection.update_many(
                    {'text':tweet['text']},
                    {'$set':{'label':feature.inverse_label(label)}},
                    )
            collection.update_many(
                    {'text':tweet['text']},
                    {'$set':{'label_parent':feature.inverse_label(label)}},
                    )
        else:
            collection.update_one(
                {'_id':sID},
                {'$set':{'label':feature.inverse_label(label)}})
    output = feature.inverse_label(label)+"  "+str(Done_prec)+"%"
    print(output)
    time.sleep(0.5)
    if parent_not_root:
        try:
            label_parent=int(input("\nStance to Parent\n1=support  2=deny  3=query  4=comment\n>>\t"))-1
        except:
            print("EXCEPTION")
            label_parent = None
    elif parent_id == root_tweet['_id']:
        label_parent = label
    else:
        label_parent = None
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
    total = float(len(preds))
    done = 0.0
    for predicted,sID in zip(preds,sorted(event_ID_dic[thread_id][0])):
        twt = list(DB.replies_to_trump.find({'_id':sID}))
        if not twt:
            twt = list(DB.trump_tweets.find({'_id':sID}))
        twt =twt[0]
#        if not twt.get('label',None) and twt.get('in_reply_to_status_id',None)!= root['_id']:
        done +=1
        if not twt.get('label',None) or not twt.get('label_parent',None):
                done_perc = (done/total)*100
                print(twt['_id'])
                label_tweet(twt,root,predicted,DB,done_perc)
        
    print("THREAD LABELED!!!!")
     

### working list of threads for labeling
train = [
860477328882905089,#Win in house for 16244
860580764944969728,#weekly address 6497
860577873060651008# JOBS, JOBS, JOBS! https://t.co/UR0eetSEnO 9379
]

#label_thread(train[0],DB_trump)

def dump_thread_labels(thread_id,DB): 
    preds = model.predict(event_feature_dic[thread_id])
    preds = map(feature.inverse_label,preds[0])
    root = list(DB.trump_tweets.find({'_id':thread_id}))[0]
    label_dic = {}
    parent_label_dic ={}
    for predicted,sID in zip(preds,sorted(event_ID_dic[thread_id][0])):
        twt = list(DB.replies_to_trump.find({'_id':sID}))
        if not twt:
            twt = list(DB.trump_tweets.find({'_id':sID}))
        twt =twt[0]
#        if not twt.get('label',None) and twt.get('in_reply_to_status_id',None)!= root['_id']:
        if twt.get('label',None):# or twt.get('label_parent',None):
            label_dic[twt['id']] = twt['label']
            parent_label_dic[twt['id']] = twt['label_parent']
    with open("train_labels_thread_"+str(thread_id)+".json","w") as labelfile:
        json.dump(label_dic,labelfile)
    with open("parent_labels_thread_"+str(thread_id)+".json","w") as parentfile:
        json.dump(parent_label_dic,parentfile)
    for k,v in zip(sorted(label_dic.items()),sorted(parent_label_dic.items())):
        print k[0],k[1],v[1]
    print len(parent_label_dic)
    print len(label_dic)
        
    


#dump_thread_labels(train[0],DB_trump)

def update_thread_labels(thread_id,DB):
    label_dic = {}
    parent_label_dic ={}
    parent_updated = 0
    label_updated = 0
#    print(DB)
#    print( list(DB.replies_to_trump.find({'_id':860583926263238656})) )
    with open("train_labels_thread_"+str(thread_id)+".json","r") as labelfile:
        label_dic = json.load(labelfile)
    with open("parent_labels_thread_"+str(thread_id)+".json","r") as parentfile:
        parent_label_dic = json.load(parentfile)
    for sID,label in label_dic.items():
#        print(sID)
#        print(type(sID))
        twt = list(DB.replies_to_trump.find({'_id':int(sID)}))
#        print(twt)
        collection = DB.replies_to_trump
#        print(twt)
        if not twt:
#            print("NOT TWT")
            twt = list(DB.trump_tweets.find({'_id':int(sID)}))
            collection = DB.trump_tweets
        twt =twt[0]
        if not twt.get('label',None):
            try:
                collection.update_many(
                    {'id':int(sID)},
                    {'$set':{'label':feature.inverse_label(label)}},
                    )
                label_updated += 1
            except Exception as err:
                print(err)
                print(sID)
        else:
            if twt['label'] != label:
                print("Tweet with ID "+str(sID)+" has two Labels")
                print("current label "+twt['label'])
                print("new label " + label)
            
        if not twt.get('label_parent',None):
            try:
                collection.update_many(
                    {'id':int(sID)},
                    {'$set':{'label_parent':feature.inverse_label( parent_label_dic[sID])}},
                    )
                parent_updated += 1
            except Exception as err:
                print(err)
                print(sID)
        else:
            if twt['label_parent'] != parent_label_dic[sID]:
                print("Tweet with ID "+str(sID)+" has two Parent labels")
                print("current label "+twt['label_parent'])
                print("new label " + parent_label_dic[sID])
    
    print("Labels Updated"+str(label_updated))    
    print("Parent Labels Updated"+str(parent_updated))
            



def get_full_text(s_id,collection):
    twet = list(collection.find({'id':s_id}))[0]
    if twet["truncated"] == True:
        try:
            text_url = twet['entities']['urls'][0]['expanded_url']
            response = requests.get(text_url, allow_redirects=False)
#            print response
#            print response.status_code
            if response.status_code == 200:
#                print "YES"
                soup = BeautifulSoup(response.text)
                tweet = soup.findAll('meta', {'property':"og:description"})
                reg = re.findall('(?<=<meta content=").+\s*.*(?=" )',str(tweet[0]))
                return reg[0]
            else:
#                print "NO"
                return twet['text']
        except:
            return twet['text']
            print text_url
            print tweet[0]
    
 

truc_tweets = [860592723413348352,860592674838953984,860592669222981633,
               860592484287729664,860592429707255810,860592373398511616,
               860592245250154496,860592221623648257,860592117722349572,
               860592110411681793,860592087569485825,860592042493321216]

#get_full_text(862739199014969348)
#get_full_text(860592723413348352)
#for twt_id in truc_tweets:
#    full_text = get_full_text(twt_id)
#    DB_trump.replies_to_trump.update_one(
#        {'id':int(twt_id)},
#        {'$set':{'full_text':full_text}},
#        )    

#for tweet in list(DB_trump.replies_to_trump.find())[:10]
#    get_full_text(twt_id)

collection = DB_trump.replies_to_trump
#for tweet_id in list(collection.distinct('id',{"full_text":{"$exists":False}})):
#    full_text = get_full_text(tweet_id,collection)
#    DB_trump.replies_to_trump.update_one(
#        {'id':int(tweet_id)},
#        {'$set':{'full_text':full_text}},
#        )  

collection = DB_trump.trump_tweets
for tweet_id in list(collection.distinct('id',{"full_text":{"$exists":False}})):
    full_text = get_full_text(tweet_id,collection)
    DB_trump.trump_tweets.update_one(
        {'id':int(tweet_id)},
        {'$set':{'full_text':full_text}},
        )  