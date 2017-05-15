# -*- coding: utf-8 -*-
"""

Created on Thu Mar 02 16:32:18 2017

@author: Colin Dryaton cdrayton@umich.edu
"""


import json
#import cPickle as pickle
import twit_token
import unicodedata as uniD
import os
import nltk
import re
from pymongo import MongoClient

#MongoDB credentials and collections
#DBname = 'test-tree'
#DBname = 'test_recurse'
DBname = 'Alta_Real_New'
DBhost = 'localhost'
DBport = 27017
    
# initiate Mongo Client
client = MongoClient()
client = MongoClient(DBhost, DBport)
db = client[DBname]
# this code needs to change for Python 3 to use the function
reply_db = db.replies_to_trump
root_db = db.trump_tweets


#top_path = ferg_1_path 

zub_id_text_dic = {}
twit_id_text_dic = {}

zub_text_list = []
twit_text_list = []

id_list = []


train_dir = "Data/semeval2017-task8-dataset"
train_dic_dir = "traindev"

train_data_dir ="rumoureval-data"
top_path = "/".join([train_dir,train_data_dir])
#top_path = ferg_1_path 

walk = os.walk(top_path)

source_id = ""
reply_id = ""

#get tweets from files
for current_dir in walk:
    last_dir = current_dir[0].split("\\")[-1]
    if last_dir == "source-tweet" or last_dir == "replies":
        for json_path in current_dir[-1]:
            with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
                filedic = json.load(jsonfile)
                
                text =  filedic["text"].lower()
                
                zub_text = " ".join(nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '',text)))
                zub_id_text_dic[filedic["id"]] = zub_text
                zub_text_list.append(zub_text)
                
                text_in = text.replace("\n","N3WL1N3")#+'\r\n'

                twit_text = " ".join(twit_token.ize(text_in))
                twit_id_text_dic[filedic["id"]] = twit_text
                twit_text_list.append(twit_text)

                id_list.append(filedic["id"])

# Get tweets from DB
for tweet in list(root_db.find())+list(reply_db.find()):
    text =  tweet["text"].lower()
                
    zub_text = " ".join(nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '',text)))
    zub_id_text_dic[tweet["id"]] = zub_text
    zub_text_list.append(zub_text)
                
    text_in = text.replace("\n","N3WL1N3")#+'\r\n'

    twit_text = " ".join(twit_token.ize(text_in))
    twit_id_text_dic[tweet["id"]] = twit_text
    twit_text_list.append(twit_text)

    id_list.append(tweet["id"])
                
# I save all the containers I use to create teh doc2vec training file 
# I do this to make sure that debugging doc2vec will be easy and 
# I'll have all the data I need to ask any question I want to

for z_tweet,t_tweet in zip(zub_text_list,twit_text_list[:10]):
    print(z_tweet)
    print(t_tweet,'\n')      
              
doc2vec_dir ="Data/doc2vec/trump_plus"
with open(doc2vec_dir+"twit_id_text_dic.json","w") as picfile:
    json.dump(twit_id_text_dic,picfile)

with open(doc2vec_dir+"twit_text_list.json","w") as picfile:
    json.dump(twit_text_list,picfile)    
    
with open(doc2vec_dir+"twit_doc2vec_train_corpus.txt","wb")as corpusfile:
    corpusfile.writelines([txt.encode("utf8")+"\r\n".encode("utf8") for txt in twit_text_list])



with open(doc2vec_dir+"zub_id_text_dic.json","w") as picfile:
    json.dump(zub_id_text_dic,picfile)

with open(doc2vec_dir+"zub_text_list.json","w") as picfile:
    json.dump(zub_text_list,picfile)    

with open(doc2vec_dir+"zub_doc2vec_train_corpus.txt","wb")as corpusfile:
    corpusfile.writelines([txt.encode("utf8")+"\r\n".encode("utf8") for txt in zub_text_list])



with open(doc2vec_dir+"id_list.json","w") as picfile:
    json.dump(id_list,picfile)     


