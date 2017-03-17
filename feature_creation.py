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
pp = pprint.PrettyPrinter(indent=0)


doc2vec_dir ="Data/doc2vec/"
model = models.Doc2Vec.load(doc2vec_dir+token_type+'rumorEval_doc2vec_set'+dims+'.model')
print model.most_similar('black')

train_dir = "Data/semeval2017-task8-dataset"
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

source_id = ""
reply_id = ""


POS_dir ="Data/twitIE_pos/"
#grah_up_dic = {}
#graph_down_dic = {}
#graph_tup = ()
pos_tweets = []
with open(POS_dir+"corpus_twitIE_POS","r")as POSfile:
    pos_tweets = [json.loads(twt) for twt in POSfile.readlines()]

ids_around_IDless_tweets=[136,139,1085,1087]        

id_pos_dic = {twt['id']:twt for twt in pos_tweets if 'id' in twt and twt["lang"]=='en'}

languages =[u'fr', u'en', u'und', u'es', u'pt']

doc2vec_dir ="Data/doc2vec/"
#id_text_dic = {}
#with open(doc2vec_dir+token_type+"id_text_dic.cpickle","rb") as picfile:
#    id_text_dic = pickle.load(picfile)

text_list = []
with open(doc2vec_dir+token_type+"text_list.json","r") as picfile:
    text_list = json.load(picfile)    
    
id_list = []
with open(doc2vec_dir+"id_list.json","rb") as picfile:
    id_list = json.load(picfile)
id_dic = {ID:i for i,ID in enumerate(id_list)}

fail_id_list =[]
structure = {}

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
                if filedic['lang'] =='en':
                    en_id.append(filedic['id'])
                    tokenizer = nltk.RegexpTokenizer(r'\w+|[^\w\s]+')
#                    tokenizer = nltk.RegexpTokenizer(u'\w+|[^\w\s\\U]+')
#                    print [tok for tok in nltk.word_tokenize(filedic["text"].replace("\n",""))],"\n"
#                    print " ".join(tokenizer.tokenize(filedic["text"].replace("\n",""))),"\n########################\n"
    
#        print en_id
#        print id_set
#        print len(en_id),"en"
#        print len(id_set),"set"
        if id_set and len(en_id) ==0:
            print current_dir
#        print"\n"


                
# I save all the containers I use to create teh doc2vec training file 
# I do this to make sure that debugging doc2vec will be easy and 
# I'll have all the data I need to ask any question I want to
                 
    
#    
#with open(doc2vec_dir+"doc2vec_train_corpus.txt","wb")as corpusfile:
#    for num,txt in enumerate(text_list):
#        if num != 0:
#            corpusfile.write("\n")
#        corpusfile.write(txt)
#        