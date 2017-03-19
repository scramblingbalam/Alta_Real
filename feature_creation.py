# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 18:07:03 2017

@author: scram
"""
dims =str(300)
token_type = "zub_"
from gensim import corpora, models, similarities
import gensim
import json
import os
import pickle
import cPickle as pickle
#import pickle
#import twit_token
import unicodedata as uniD
import nltk
import networkx as nx
import numpy as np
import itertools as it
import pprint
import deep_dict_2_adj_matrix as dic2mat
import collections as coll
import re
pp = pprint.PrettyPrinter(indent=0)


doc2vec_dir ="Data/doc2vec/"
model = models.Doc2Vec.load(doc2vec_dir+token_type+'rumorEval_doc2vec_set'+dims+'.model')
print model.most_similar('black'),"\n"

train_dir = "Data\\semeval2017-task8-dataset"
train_dic_dir = "traindev"

train_data_dir ="rumoureval-data"
rumor_dirs =    {"charlie_hebdo": "charliehebdo",
                 "ebola-essien": "ebola-essien",
                 "ferguson": "ferguson",
                 "germanwings-crash": "germanwings-crash",
                 "ottawa_shooting": "ottawashooting",
                 "prince-toronto": "prince-toronto",
                 "putinmissing": "putinmissing",
                 "sydney_siege": "sydneysiege" 
                }

ferguson_1 = "498280126254428160"
ferguson_2 = "498430783699554305"
ferguson_3 = "499366666300846081"
ferguson_4 = "499368931367608320"
ferguson_5 = "499456140044824576"
ferguson_6 = "499530130487017472"
ferguson_7 = "499612545909415938"

structutr_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1,"structure.json"])
source_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_2,"source-tweet","498280126254428160.json"])
ferg_1_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1])
ferg_2_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_2])
ferg_3_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_3])
ferg_4_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_4])
ferg_5_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_5])
ferg_6_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_6])
ferg_7_path = "\\".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_7])

top_path = "\\".join([train_dir,train_data_dir])
#top_path = ferg_2_path 

id_text_dic = {}
text_list = []
id_list = []

walk = os.walk(top_path)


POS_dir ="Data\\twitIE_pos\\"
doc2vec_dir ="Data\\doc2vec\\"

ids_around_IDless_tweets=[136,139,1085,1087]


def pos_extract(path):
    pos_tweets = []
    with open(path,"r")as POSfile:
        pos_tweets = [json.loads(twt) for twt in POSfile.readlines()]
    #create set of all used POS tags
    pos_tag_set = set([pos['category'] for twt in pos_tweets for pos in twt[u'entities'][u'Token']])

    #create dictionary of POS_Tags and vector indicies
    pos_index_dic = {pos:num for num,pos in enumerate(pos_tag_set)}
    #create inverse lookup dictionary
    i_p_dic = {num:pos for num,pos in enumerate(pos_tag_set)}
    # create dictionary of POS tag lists for keyed by ID
    dic = {twt['id']:twt[u'entities'][u'Token'] for twt in pos_tweets if 'id' in twt}
    id_p_dic ={}
    for K,V in dic.items():
        vector = []
        for v in V:
            vector.append(pos_index_dic[v['category']])
        id_p_dic[K]=vector
    id_p_dic = {K:[pos_index_dic[v['category']] for v in V] for K,V in dic.items()}
    return id_p_dic, i_p_dic




#text_list = []
#with open(doc2vec_dir+token_type+"text_list.json","r") as picfile:
#    text_list = json.load(picfile)    
#    
#id_list = []
#with open(doc2vec_dir+"id_list.json","rb") as picfile:
#    id_list = json.load(picfile)
#id_dic = {ID:i for i,ID in enumerate(id_list)}
#
#fail_id_list =[]
#structure = {}
#
#current_event = ""
#current_line_dic = {}
#lang_event_csv = []
#lang_list=[]
#non_english_event =[]

pos_file_path =POS_dir+"corpus_twitIE_POS"
id_pos_dic, index_pos_dic = pos_extract(pos_file_path)
swear_path = "Data\\badwords.txt"
swear_list=[]
with open(swear_path,"r")as swearfile:
    swear_list = swearfile.readlines()
    
negationwords = ['not', 'no', 'nobody', 'nothing', 'none', 
                 'never', 'neither', 'nor', 'nowhere', 'hardly', 
                 'scarcely', 'barely', 'don*', 'isn*', 'wasn*', 
                 'shouldn*', 'wouldn*', 'couldn*', 'doesn*',
                 'don', 'isn', 'wasn', 'nothin',
                 'shouldn', 'wouldn', 'couldn', 'doesn']

id_text_dic ={}
with open(doc2vec_dir+token_type+"id_text_dic.json",'r')as textDicFile:
    id_text_dic = json.load(textDicFile)


def word_bool(text,word_list,cont="*"):
    if cont:
        word_list = [string.replace("\n","") for string in word_list]
        word_list = [s.replace(cont,"")+" " if s[-1] != "*" else s for s in word_list]
        word_list = [" "+s.replace(cont,"") if s[0] != "*" else s for s in word_list]
    
    bad_list= [swear for swear in word_list if swear in text]
    if bad_list:
        print bad_list
    return bool(bad_list)
        
def word_char_count(text):
    return len(text.split()),len(text)
#for i,i1,i2 in zip(swear_list,swear_list1,swear_list2):
#        print i,i1,i2
#    swear_list = swearfile.readlines()

def zub_capital_ratio(text):
    alpha_text = " ".join(nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '', text )))
    return float(sum([char.isupper() for char in alpha_text]))/float(len(alpha_text))


for current_dir in walk:
    adj_mat = np.array([])
    if 'structure.json' in current_dir[-1]:
        en_id = []
#        if adj_mat.any():
#            G = nx.from_numpy_matrix(np.array(adj_mat)) 
#            nx.draw(G, with_labels=True)
        root_id = long(current_dir[0].split("\\")[-1])
#        print root_id, "root",root_id in id_list
        with open(current_dir[0]+"\\"+'structure.json',"r")as jsonfile:
                structure = json.load(jsonfile)
                adj_mat,id_dic  = dic2mat.dic_2_adj_mat(structure)
                # pp.pprint(structure)
                id_set =set(k for k,v in id_dic.items())
    last_dir = current_dir[0].split("\\")[-1]
    if last_dir == "source-tweet" or last_dir == "replies":
#        print id_set
        for json_path in current_dir[-1]:
#            print "#########\n",current_dir[0],json_path,"######\n"
            with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
                filedic = json.load(jsonfile)
                text =filedic['text']
                ID = filedic['id_str']
                print text
                if token_type == "zub_":
                    cap_ratio = zub_capital_ratio(text)
                elif token_type == "twit_":
                    print "ERROR write a better captial ratio function"
                    break 
                print cap_ratio                   
                word_count,char_count = word_char_count(id_text_dic[ID])
                swear_bool = word_bool(text,swear_list)
                neg_bool = word_bool(text,negationwords)
                pos_vec = id_pos_dic[filedic["id"]],"\n"
                
#print swear_list
#
#print coll.Counter(non_english_event)
#print coll.Counter(lang_list)
#                
