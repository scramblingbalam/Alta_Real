# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 17:31:59 2017

@author: scram
"""
import feature_functions as feature
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import feature_functions as feature
import itertools as it
from gensim.models.doc2vec import Doc2Vec
from collections import Counter
from sklearn.externals import joblib
import sys
import json
from pymongo import MongoClient
if sys.version_info[0] < 3:
    import cPickle as pickle

from nested_dict import flatXn
from scipy.stats import pearsonr
#def flatXn(deeplist,n):
#    while n != 0:
#        n -= 1
#        return flatXn(it.chain.from_iterable(deeplist),n)
#    return list(deeplist)

results = []
ids = []
with open("results/treecrf-twit-doc2vec-300",'r') as resultfile:
    resultlines = resultfile.readlines()
    ids = list(map(lambda x: int(x.split()[0]), resultlines))
    results = list(map(lambda x: list(map( int,x.split()[1:])), resultlines))
    trans_results = list(map(lambda x: list(map( lambda y: feature.inverse_label(int(y)),x.split()[1:])), resultlines))




print(results[:5])
print(trans_results[:5])
print(ids[:5])
print("\n")

results_df = pd.DataFrame(results, index=ids, columns=['Predicted','Expected'])
results_label_df = pd.DataFrame(trans_results, index=ids, columns=['Predicted','Expected'])

print(results_label_df[:5])
print(results_df[:5])

feature_list = []
with open("event_model_dic","rb")as modelfile:
    feature_list =pickle.load(modelfile)
    
#feature_list = joblib.load("event_model_dic.joblib")
feature_string = feature_list[0]
event_feature_dic = feature_list[1]
          
event_ID_dic = {}    
with open("event_ID_dic","rb")as modelfile:
    event_ID_dic = pickle.load(modelfile)
    
print(event_ID_dic.keys())    
test_event = 'ottawashooting'
print("\n")
#print event_ID_dic[test_event][0][0]
#print event_feature_dic[test_event][0][0][0]
model_ids = flatXn([v for k,v in event_ID_dic.items()],2)
model_vecs = flatXn(flatXn([v for k,v in event_feature_dic.items()],2)[0::2],1)

model_df = pd.DataFrame(model_vecs, index=model_ids)

token_type = feature_string.split('_')[0]+'_'
dims = feature_string.split('_')[-1]
doc2vec_dir = "Data\\doc2vec\\trump_plus\\"
#doc2vec_dir ="Data\\doc2vec\\not_trump\\"
model = Doc2Vec.load(doc2vec_dir+token_type+"rumorEval_doc2vec_set"+dims+".model")

DBname = 'Alta_Real_New'
DBhost = 'localhost'
DBport = 27017
DBname_t = 'Train'
    
    # initiate Mongo Client
client = MongoClient()
client = MongoClient(DBhost, DBport)
DB_trump = client[DBname]
DB_train = client[DBname_t]

print(len(model_df.index.values))

#tweets = list(DB_train.replies_to_trump.find()) + list(DB_train.trump_tweets.find())
tweets = list(DB_train.replies_to_trump.find({'_id':{'$in':model_ids}}))
tweets += list(DB_train.trump_tweets.find({'_id':{'$in':model_ids}}))
print(len(tweets))

results_df['Hit'] = list(map(int,results_df['Predicted'] == results_df['Expected']))

#num_result_model_df = pd.concat([results_num_df,model_df])
result_model_df = results_df.join(model_df)

print(result_model_df[:2])
#print(results_num_df[:2])
#print(model_df[:2])
print(len(result_model_df))
print(len(set(result_model_df.index.values)))

feat_index = []
pearson = []
for i in range(300,360):
    feat_index.append(i)
    pearson.append(pearsonr(result_model_df['Hit'],result_model_df[i]))
    
print(pearson[:10])



id_text_dic ={}
with open(doc2vec_dir+token_type+"id_text_dic.json",'r')as textDicFile:
    id_text_dic = json.load(textDicFile)
swear_path = "Data\\badwords.txt"
swear_list=[]
with open(swear_path,"r")as swearfile:
    swear_list = swearfile.readlines()

feat_names = [u"entities.media_BooL",u"entities.urls_Bool",u"in_reply_to_screen_name_Bool",
              u"?_Bool",u"!_Bool",u"._Bool",u"capital_ratio",u"word_count",u"char_count",
              u"swear_Bool",u"negation_Bool",u"POS_NNS_Count",u"POS_VBG_Count",u"POS_IN_Count",
              u"POS_._Count",u"POS_(_Count",u"POS_RBS_Count",u"POS_CC_Count",u"POS_JJ_Count",
              u"POS_X_Count",u"POS_URL_Count",u"POS_UH_Count",u"POS_DT_Count",u"POS_PRP$_Count",
              u"POS_$_Count",u"POS_VBD_Count",u"POS_PRP_Count",u"POS_RBR_Count",u"POS_NNPS_Count",
              u"POS_:_Count",u"POS_MD_Count",u"POS_VB_Count",u"POS_WP_Count",u"POS_WRB_Count",
              u"POS_WDT_Count",u"POS_POS_Count",u"POS_RT_Count",u"POS_WP$_Count",u"POS_RB_Count",
              u"POS_CD_Count",u"POS_EX_Count",u"POS_NN_Count",u"POS_BES_Count",u"POS_FW_Count",
              u"POS_#_Count",u"POS_JJR_Count",u"POS_PDT_Count",u"POS_``_Count",u"POS_RP_Count",
              u"POS_GW_Count",u"POS_SYM_Count",u"POS_,_Count",u"POS_NNP_Count",u"POS_HT_Count",
              u"POS_TO_Count",u"POS_VBP_Count",u"POS_USR_Count",u"POS_''_Count",u"POS_VBZ_Count",
              u"POS_JJS_Count",#result_model_df.loc[test_id][359] returns this
              ]

pearson_df = pd.DataFrame(pearson,index=feat_names, columns=['negative','positive'])
print("________________________________\nMost Negativly correlated features")
print(pearson_df.sort_values('negative'))
print("________________________________\nMost Positivly correlated features")
print(pearson_df.sort_values('positive',ascending =False))

#

#print model.docvecs[str(model_ids[0])]
#print len(model.docvecs[str(model_ids[0])])
#for n,i in enumerate(map(list,model_vecs)):
#    try:
#        print i.index(model.docvecs[str(model_ids[0])][0])
#        print n
#    except:
#        pass
    
    
    