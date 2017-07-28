# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 12:22:55 2017

@author: scram
"""

from gensim import corpora, models, similarities
import gensim
import json
import os
import pickle
from pymongo import MongoClient
import unicodedata as uniD
import sys
import nltk
import networkx as nx
import numpy as np
import itertools as it
import pprint
import collections as coll
import re
from collections import Counter
import feature_functions as feature
import nested_dict
from functools import reduce
from scipy import spatial
from sklearn.externals import joblib
from Mongo_functions import id2edgelist
pp = pprint.PrettyPrinter(indent=0)




def translatelabel(label):
    if label == 'supporting'or label == 'support':
        return 0
    if label == 'denying'or label == 'deny':
        return 1
    if label == 'appeal-for-more-information'or label == 'query':
        return 2
    if label == 'comment' or label == '0':
        return 3
    if label =='imp-denying':
        return 4

id_target_dic = {}



    
label_list =[]

event_target_dic = {}  
event_ID_dic = {}
unlabeled_thread_list=[]
thread_list=[]

def files_to_mongo(root_path,label_dict,db):
    """ Moves tweets from their file structure to mongo
    """
    walk = os.walk(root_path)
    threads_errors = []
    root_errors = []
    replies_errors = []
    for current_dir in walk:
        if 'structure.json' in current_dir[-1]:
            event = current_dir[0].split("\\")[-2]
        last_dir = current_dir[0].split("\\")[-1]
        if last_dir == "replies":
            json_list =[]
            root_tweet = {}
            rep_path =current_dir[0]
            root_path = rep_path.split("\\")
            with open("\\".join(root_path[:-1])+"\\"+'structure.json',"r")as jsonfile:
                structure = json.load(jsonfile)
    
            source_path = root_path
            source_path[-1]="source-tweet"
            source_path = "\\".join(source_path)
            root =os.listdir(source_path)[0]
            with open(source_path+"\\"+root,"r")as jsonfile:
                root_tweet = json.load(jsonfile)
            for json_path in current_dir[-1]:
                with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
                    json_list.append(json.load(jsonfile))
            thread_list = list(map(lambda x: x.get("id_str"),json_list))
            root_id = root_tweet['id']
            thread_list.append(str(root_id))
            structure = nested_dict.subset_by_key(structure, thread_list)
            edge_list = nested_dict.to_edge_list(nested_dict.map_keys(int,structure))
            fields = ["parent","child"]
            mongo_update = {"_id":root_id,
                            "id_str":str(root_id),
                            "event":event,
                            "edge_list":nested_dict.vecs_to_recs(edge_list,fields)}
            try:
                db.edge_list.insert_one(mongo_update).inserted_id
            except Exception as err:
#                print(err)
                threads_errors.append(root_id)
            for twt in json_list:
                twt["_id"] = twt["id"]
                twt['label'] = label_dict[int(twt['id'])]
                try:
                    db.replies_to_trump.insert_one(twt).inserted_id
                except Exception as err:
#                    print(err)
                    replies_errors.append(twt["id"])
            root_tweet["_id"] = root_id
            root_tweet["label"] = label_dict[int(root_id)]
            try:
                db.trump_tweets.insert_one(root_tweet)
            except Exception as err:
#                print(err)
                root_errors.append(root_id)
    return threads_errors, root_errors, replies_errors

def get_labeled_thread_tweets(thread,db=MongoClient('localhost', 27017).Alta_Real_New):
    root_id = thread['_id']
    thread_tweets = list(db.trump_tweets.find({'_id':root_id}))
    thread_ids = set()
    thread_edge_list =[]
#    print(root_id)
#    print( thread_tweets[0]['text'])
    thread
    for edg in thread['edge_list']:
        parent = edg['parent']
        child = edg['child']
        thread_edge_list.append((parent,child))
        thread_ids.add(child)
        thread_ids.add(parent)
    thread_ids = list(thread_ids)
    
    thread_tweets += list(db.replies_to_trump.find({'_id':{'$in':thread_ids},'label':{'$exists':True}}))
    thread_ids = [i['id'] for i in thread_tweets]
    print(root_id in thread_ids)
    print(root_id)
    print(len(thread_edge_list))
    print(thread_ids)
    print(len(thread_ids))
#    print(thread_ids)
    thread_edge_list = list(filter(lambda x: x[0] in thread_ids and x[1] in thread_ids, thread_edge_list))
    thread_ids = [root_id] + thread_ids
#    print( len(thread_tweets))
    return thread_tweets,thread_edge_list,thread_ids

def labels_to_train(db,db_source,labels_dic):
    """ checks the Alta_Real database and creates sub-trees for any labeld tweets 
    """
    threads_errors = []
    root_errors = []
    replies_errors = []
    print(db_source)
    roots = list(db_source.trump_tweets.find({"label":{"$exists":True}}))
    print("LENGTH ROOTS",len(roots))
    # put labels to DB from target label file
    for labeled_id in labels_dic:
        tweet = list(db_source.replies_to_trump.find({'_id':labeled_id}))
        if tweet:
            tweet = tweet[0]
            if not tweet.get('label',None):
                db_source.replies_to_trump.update_one(
                        {"_id":labeled_id},
                        {"$set": 
                            {"label":labels_dic[labeled_id]}
                        }
                    )

    for root_tweet in roots:
        root_id = root_tweet['id']
        thread_edges = list(db_source.edge_list.find({"_id":root_id}))[0]
        json_list,edge_list,thread_list = get_labeled_thread_tweets(thread_edges,db_source)
        thread_list.append(str(root_id))
        fields = ["parent","child"]
        event_text = root_tweet['text']
#        event_text = event_text.replace('/','').replace(':','').replace('-','').replace('#','')
        if len(event_text) >20:
            event = event_text.replace(" ","_")[:20]
        else:
            event = event_text.replace(" ","_")
        
        mongo_update = {"_id":root_id,
                        "id_str":str(root_id),
                        "event":event,
                        "edge_list":nested_dict.vecs_to_recs(edge_list,fields)}
#        print(mongo_update)
        try:
            db.edge_list.insert_one(mongo_update).inserted_id
        except Exception as err:
#               print(err)
            threads_errors.append(root_id)
        for twt in json_list:
            twt["_id"] = twt["id"]
            if not twt['label']:
                print(twt['id'])
                print(twt['label'])
                print(bool(twt['label']))
            try:
                db.replies_to_trump.insert_one(twt).inserted_id
            except Exception as err:
#                    print(err)
                replies_errors.append(twt["id"])
        root_tweet["_id"] = root_id
        try:
            db.trump_tweets.insert_one(root_tweet)
        except Exception as err:
#              print(err)
            root_errors.append(root_id)
    return threads_errors, root_errors, replies_errors

def process_tweet(tweet):
    feature_vector =[]
    if tweet.get("full_text",None):
        text =tweet['full_text']
    else:
        text =tweet['text']
    ID = tweet['id_str']
    thread_list.append(event)
    if ID in id_target_dic:
        label_list.append(id_target_dic[ID])               
#       print id_target_dic[root_id.split(".")[0]]
    attribute_paths = [[u'entities',u'media'],
                       [u'entities',u'urls'],
                       [u'in_reply_to_screen_name']]
    format_binary_vec = list(feature.attribute_binary_gen(tweet, attribute_paths))
    feature_vector += format_binary_vec
    punc_vec = list(feature.punc_binary_gen(text,punc_list))
    feature_vector += punc_vec
    if token_type == "zub":
        cap_ratio = feature.zub_capital_ratio(text)
#       print "Twit & Zub using same Capitalization Ratio\n\tIs this desirable?"
    elif token_type == "twit":
        cap_ratio = feature.zub_capital_ratio(text)
#       print "Twit & Zub using same Capitalization Ratio\n\tIs this desirable?"
    feature_vector += cap_ratio
    word_char_count = feature.word_char_count(id_text_dic[ID])
    feature_vector += word_char_count
    swear_bool = feature.word_bool(text,swear_list)
    feature_vector += swear_bool
    neg_bool = feature.word_bool(text,negationwords)
    feature_vector += neg_bool
    if ID in id_pos_dic_full:
        pos_vec = id_pos_dic_full[tweet["id"]]
    else:
        pos_vec = id_pos_dic[tweet["id"]]
    feature_vector += feature.pos_vector(pos_vec)
            
    d2v_text = D2V_id_text_dic[ID]
    if embed_type == "word2vec":
        embed_vector = feature.mean_W2V_vector(d2v_text,D2Vmodel)   
    elif embed_type == "doc2vec":
        embed_vector = D2Vmodel.docvecs[ID]
    feature_vector = np.concatenate((embed_vector,
                                     np.array(feature_vector)))
#    thread_id_list.append(ID)
#    thread_dic[ID] = feature_vector
    return int(ID), feature_vector

def get_thread_tweets(thread,db=MongoClient('localhost', 27017).Alta_Real_New):
    root_id = thread['_id']
    thread_tweets = list(db.trump_tweets.find({'_id':root_id}))
    thread_ids = set()
    thread_edge_list =[]
    for edg in thread['edge_list']:
        parent = edg['parent']
        child = edg['child']
        thread_ids.add(child)
        thread_edge_list.append((parent,child))
    thread_ids = list(thread_ids)
    thread_tweets += list(db.replies_to_trump.find({'_id':{'$in':thread_ids}}))
    thread_ids = [root_id] + thread_ids
    return thread_tweets,thread_edge_list,thread_ids
    



#### RUN FUNCTIONS TO CREATE FEATURES 
if __name__ == '__main__':
### Import if python 2
    if sys.version_info[0] < 3:
        import cPickle as pickle
        
    # Global Variables 
    dims =str(300)
    #token_type = "zub"
    embed_type = "word2vec"
    token_type = "twit"
    embed_type = "doc2vec"
        
    id_text_dic = {}
    text_list = []
    id_list = []
        
    POS_dir ="Data\\twitIE_pos\\"
    doc2vec_dir = "Data\\doc2vec\\trump_plus"
    
    ids_around_IDless_tweets=[136,139,1085,1087]
        
    pos_file_path1 = POS_dir+token_type+"_semeval2017"+"_twitIE_POS"
    pos_file_path2 = POS_dir+token_type+"_Alta_Real_New"+"_twitIE_POS"
    pos_file_path3 = POS_dir+token_type+"_Alta_Real_New"+"_twitIE_POS_FULL_TEXT"
    pos_file_path = [pos_file_path1, pos_file_path2,pos_file_path3]
    id_pos_dic, index_pos_dic = feature.pos_extract(pos_file_path)

#    pos_file_path1 = POS_dir+token_type+"_semeval2017"+"_twitIE_POS_FULL"
    pos_file_path_full = POS_dir+token_type+"_Alta_Real_New"+"_twitIE_POS_FULL_TEXT"
    pos_file_path_full = [pos_file_path_full]
    id_pos_dic_full, index_pos_dic_full = feature.pos_extract(pos_file_path_full)
        
    swear_path = "Data\\badwords.txt"
    swear_list=[]
    with open(swear_path,"r")as swearfile:
        swear_list = swearfile.readlines()
    
    
    id_text_dic ={}
    with open(doc2vec_dir+token_type+"_"+"id_text_dic.json",'r')as textDicFile:
        id_text_dic = json.load(textDicFile)
    
    
    negationwords = ['not', 'no', 'nobody', 'nothing', 'none', 
                     'never', 'neither', 'nor', 'nowhere', 'hardly', 
                     'scarcely', 'barely', 'don*', 'isn*', 'wasn*', 
                     'shouldn*', 'wouldn*', 'couldn*', 'doesn*',
                     'don', 'isn', 'wasn', 'nothin',
                     'shouldn', 'wouldn', 'couldn', 'doesn']
    
    punc_list = [u"?",u"!",u"."]
    attribute_paths = [[u'entities',u'media'],
                       [u'entities',u'urls'],
                       [u'in_reply_to_screen_name']]
    
    doc2vec_dir ="Data/doc2vec/"
    doc2vec_dir ="Data/doc2vec/trump_plus"
    D2Vmodel = models.Doc2Vec.load(doc2vec_dir+token_type+"_"+'rumorEval_doc2vec_set'+dims+'.model')
    print(D2Vmodel.most_similar('black'),"\n")
    
    doc2vec_id = []
    with open(doc2vec_dir+"id_list.json","r") as picfile:
        doc2vec_id_key={str(twtID):str(key) for key,twtID in enumerate(json.load(picfile))} 
    
    D2V_id_text_dic ={}
    with open(doc2vec_dir+token_type+"_"+"id_text_dic.json", "r")as d2vtextfile:
        D2V_id_text_dic = json.load(d2vtextfile)
    
    err_dic = {}
    
    graph_root_id = ""
    graph_event = ""
    graph_size = 0
    graph_2_vis =[]
    
    thread_dic = {}
    event_target_dic = {}
    root_id = 0
    event_model_dic = {}
    #MongoDB credentials and collections
#    DBname = 'test-tree'
#    DBname = 'test_recurse'
    DBname = 'Alta_Real_New'
    DBhost = 'localhost'
    DBport = 27017
    DBname_t = 'Train'
    
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB_trump = client[DBname]
    DB_train = client[DBname_t]
    # collection where SemEval data is stored
    dev = "rumoureval-subtaskA-dev.json"
    train = "rumoureval-subtaskA-train.json"
    train_dic_dir = "traindev"
    train_data_dir ="rumoureval-data"
    train_dir = "Data\\semeval2017-task8-dataset"
    target_path = "\\".join([train_dir,train_dic_dir,train])
    with open(target_path,"r")as targetfile:
        id_target_dic = {int(k):v for k,v in json.load(targetfile).items()} 
        
    target_path = "\\".join([train_dir,train_dic_dir,dev])
    with open(target_path,"r")as targetfile:
        id_target_dic.update({int(k):v for k,v in json.load(targetfile).items()})
    with open("kats_label_dict","r")as targetfile:
        id_target_dic.update({int(k):v for k,v in json.load(targetfile).items()})
        
    if not DB_train.edge_list.find_one():
        top_path = "\\".join([train_dir,train_data_dir])
        posted = files_to_mongo(top_path,id_target_dic,DB_train)
        transfered = labels_to_train(DB_train,DB_trump,id_target_dic)
        train_threads, train_roots, train_replies = posted
    else:
        DB_train.edge_list.find_one()
        top_path = "\\".join([train_dir,train_data_dir])
        posted = files_to_mongo(top_path,id_target_dic,DB_train)
        transfered = labels_to_train(DB_train,DB_trump,id_target_dic)
        train_threads, train_roots, train_replies = posted
        print("No_New_Threads",set(train_threads)==set(DB_train.edge_list.distinct("_id")))
        print("No_New_Roots",set(train_roots)==set(DB_train.trump_tweets.distinct("_id")))
        print("No_New_Replies",set(train_replies)==set(DB_train.replies_to_trump.distinct("_id")))
    ######## Sets 'event' field in main DB to the root_id for that thread
    if not DB_trump.edge_list.distinct('event'):
        for thrd in list(DB_trump.edge_list.find()):
            DB_trump.edge_list.update_one(
                                    {'_id':thrd['_id']},
                                    {'$set':
                                        {'event':thrd['_id'],
                                        'id_str':str(thrd['_id'])}
                                        }
                                    )
    
    big_win_edge = list(DB_train.edge_list.find({'event':'Big_win_in_the_House'}))[0]
    print(len(big_win_edge['edge_list']))