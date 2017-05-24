# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 18:07:03 2017

@author: scram
"""

from gensim import corpora, models, similarities
import gensim
import json
import os
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

import feature_functions as feature
import nested_dict
from scipy import spatial
pp = pprint.PrettyPrinter(indent=0)

### Import if python 2
if sys.version_info[0] < 3:
    import cPickle as pickle


# Global Variables 
dims =str(300)
#token_type = "zub"
embed_type = "word2vec"
token_type = "twit"
#embed_type = "doc2vec"


train_dir = "Data\\semeval2017-task8-dataset"
train_dic_dir = "traindev"

train_data_dir ="rumoureval-data"


top_path = "\\".join([train_dir,train_data_dir])


id_text_dic = {}
text_list = []
id_list = []

walk = os.walk(top_path)


POS_dir ="Data\\twitIE_pos\\"
doc2vec_dir ="Data\\doc2vec\\"

ids_around_IDless_tweets=[136,139,1085,1087]


#non_english_event =[]

pos_file_path =POS_dir+"corpus_twitIE_POS"
id_pos_dic, index_pos_dic = feature.pos_extract(pos_file_path)


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
D2Vmodel = models.Doc2Vec.load(doc2vec_dir+token_type+"_"+'rumorEval_doc2vec_set'+dims+'.model')
print(D2Vmodel.most_similar('black'),"\n")

doc2vec_id = []
with open(doc2vec_dir+"id_list.json","r") as picfile:
    doc2vec_id_key={str(twtID):str(key) for key,twtID in enumerate(json.load(picfile))} 

D2V_id_text_dic ={}
with open(doc2vec_dir+token_type+"_"+"id_text_dic.json", "r")as d2vtextfile:
    D2V_id_text_dic = json.load(d2vtextfile)



#print "KeyError: u'552790281276628992'"
#print structure.keys(),"\n"
#pp.pprint(structure) 


graph_root_id = ""
graph_event = ""
graph_size = 0
graph_2_vis =[]

thread_dic = {}

root_id = 0
event_model_dic = {}


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

train_dir 
train_dic_dir 
dev = "rumoureval-subtaskA-dev.json"
train = "rumoureval-subtaskA-train.json"
target_path = "\\".join([train_dir,train_dic_dir,train])
with open(target_path,"r")as targetfile:
    id_target_dic = json.load(targetfile) 
    
label_list =[]

event_target_dic = {}  
event_ID_dic = {}
unlabeled_thread_list=[]
thread_list=[]
#for current_dir in walk:
#    adj_mat = np.array([])
##    print "\nEVENT",event
##    print "CURRENT_DIR",current_dir
#    if 'structure.json' in current_dir[-1]:
##        print current_dir[0].split("\\")[-2]
#        event = current_dir[0].split("\\")[-2]
##        print "##############\n",event
###        if adj_mat.any():
###            G = nx.from_numpy_matrix(np.array(adj_mat)) 
###            nx.draw(G, with_labels=True)
#    last_dir = current_dir[0].split("\\")[-1]
#    if last_dir == "replies":
#        thread_id_list = []
#        feature_vector =[]
#        json_list =[]
#        rep_path =current_dir[0]
##        print "REPLIES_DIR",rep_path ,"\n"
#        root_path = rep_path.split("\\")
##        print root_path
#        with open("\\".join(root_path[:-1])+"\\"+'structure.json',"r")as jsonfile:
##            print structure
#            structure = json.load(jsonfile)
#
#        source_path = root_path
#        source_path[-1]="source-tweet"
#        source_path = "\\".join(source_path)
##        print list(os.listdir(source_path))
#        root_id =os.listdir(source_path)[0]
##        if root_id.split(".")[0] in id_target_dic.keys():
#        with open(source_path+"\\"+root_id,"r")as jsonfile:
#            json_list.append(json.load(jsonfile))
#        for json_path in current_dir[-1]:
#            with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
#                json_list.append(json.load(jsonfile))
##        print "\n", root_id
#        for filedic in json_list:
#            feature_vector =[]
#            text =filedic['text']
#            ID = filedic['id_str']
#            thread_list.append(event)
#            if event != "germanwings-crash":
#                label_list.append(id_target_dic[ID])               
##                print id_target_dic[root_id.split(".")[0]]
#            attribute_paths = [[u'entities',u'media'],
#                               [u'entities',u'urls'],
#                               [u'in_reply_to_screen_name']]
#            format_binary_vec = list(feature.attribute_binary_gen(filedic, attribute_paths))
#            feature_vector += format_binary_vec
#            punc_vec = list(feature.punc_binary_gen(text,punc_list))
#            feature_vector += punc_vec
#            if token_type == "zub":
#                cap_ratio = feature.zub_capital_ratio(text)
##                print "Twit & Zub using same Capitalization Ratio\n\tIs this desirable?"
#            elif token_type == "twit":
#                cap_ratio = feature.zub_capital_ratio(text)
##                print "Twit & Zub using same Capitalization Ratio\n\tIs this desirable?"
#            feature_vector += cap_ratio
#            word_char_count = feature.word_char_count(id_text_dic[ID])
#            feature_vector += word_char_count
#            swear_bool = feature.word_bool(text,swear_list)
#            feature_vector += swear_bool
#            neg_bool = feature.word_bool(text,negationwords)
#            feature_vector += neg_bool
#            pos_vec = id_pos_dic[filedic["id"]]
#            feature_vector += feature.pos_vector(pos_vec)
#            
#            d2v_text = D2V_id_text_dic[ID]
#            if embed_type == "word2vec":
#                embed_vector = feature.mean_W2V_vector(d2v_text,D2Vmodel)
#            elif embed_type == "doc2vec":
#                embed_vector = D2Vmodel.docvecs[ID]
#            feature_vector = np.concatenate((embed_vector,
#                                             np.array(feature_vector)))
#
#            thread_id_list.append(ID)
#            thread_dic[ID] = feature_vector
#        structure = nested_dict.subset_by_key(structure, thread_dic.keys())
#        size = len(nested_dict.all_keys(structure))
#        edge_list = nested_dict.to_edge_list(structure)
#        if 60>size>graph_size:
#            graph_2_vis = edge_list
#            graph_size = size
#            graph_event = event
#            graph_root_id =root_id
#            
#        id_dic = feature.id_index_dic(edge_list)
#        id_order = [i[0] for i in sorted(id_dic.items(),key=lambda x:(x[1],x[0]))]
#        # create an array for each thread an append to the event_target_dic        
#        if event != "germanwings-crash":
#            thread_target_vector = [np.array(map(translatelabel, 
#                                                [id_target_dic[i] 
#                                                            for i in id_order]))]
#
#            if event in event_model_dic:
#                event_target_dic[event] += thread_target_vector
#            else:
#                event_target_dic[event] = thread_target_vector
#   
##        pp.pprint(structure)
#        edge_vector = np.array([np.array([id_dic[Id] for Id in edge]) 
#                                                        for edge in edge_list])
#
#        n_feats = np.array([thread_dic[i] for i in id_order])
#        X_train = [np.array([n_feats,edge_vector])]
#        if event in event_model_dic:
#            event_model_dic[event] += X_train
#        else:
#            event_model_dic[event] = X_train
#        
#        if event in event_ID_dic:
#            event_ID_dic[event] += [thread_id_list]
#        else:
#            event_ID_dic[event] = [thread_id_list]
#        thread_dic = {}





def process_tweet(tweet):
    feature_vector =[]
    text =tweet['text']
    ID = tweet['id_str']
    thread_list.append(event)
    if event != "germanwings-crash":
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
    return ID, feature_vector

if __name__ == '__main__':
    #MongoDB credentials and collections
#    DBname = 'test-tree'
#    DBname = 'test_recurse'
    DBname = 'Alta_Real_New'
    DBhost = 'localhost'
    DBport = 27017
    
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB = client[DBname]
    for current_dir in walk:
        adj_mat = np.array([])
    #    print "\nEVENT",event
    #    print "CURRENT_DIR",current_dir
        if 'structure.json' in current_dir[-1]:
    #        print current_dir[0].split("\\")[-2]
            event = current_dir[0].split("\\")[-2]
    #        print "##############\n",event
    ##        if adj_mat.any():
    ##            G = nx.from_numpy_matrix(np.array(adj_mat)) 
    ##            nx.draw(G, with_labels=True)
        last_dir = current_dir[0].split("\\")[-1]
        if last_dir == "replies":
            thread_id_list = []
            feature_vector =[]
            json_list =[]
            rep_path =current_dir[0]
    #        print "REPLIES_DIR",rep_path ,"\n"
            root_path = rep_path.split("\\")
    #        print root_path
            with open("\\".join(root_path[:-1])+"\\"+'structure.json',"r")as jsonfile:
    #            print structure
                structure = json.load(jsonfile)
    
            source_path = root_path
            source_path[-1]="source-tweet"
            source_path = "\\".join(source_path)
    #        print list(os.listdir(source_path))
            root_id =os.listdir(source_path)[0]
    #        if root_id.split(".")[0] in id_target_dic.keys():
            with open(source_path+"\\"+root_id,"r")as jsonfile:
                json_list.append(json.load(jsonfile))
            for json_path in current_dir[-1]:
                with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
                    json_list.append(json.load(jsonfile))
    #        print "\n", root_id
    ######## Process each tweet to create a feature vector
            for tweet in json_list:
                twt_ID, feat_vector = process_tweet(tweet)
                thread_id_list.append(twt_ID)
                thread_dic[twt_ID] = feat_vector
            structure = nested_dict.subset_by_key(structure, thread_dic.keys())
            size = len(nested_dict.all_keys(structure))
            edge_list = nested_dict.to_edge_list(structure)
            if 60>size>graph_size:
                graph_2_vis = edge_list
                graph_size = size
                graph_event = event
                graph_root_id =root_id
                
            id_dic = feature.id_index_dic(edge_list)
            id_order = [i[0] for i in sorted(id_dic.items(),key=lambda x:(x[1],x[0]))]
            # create an array for each thread an append to the event_target_dic        
            if event != "germanwings-crash":
                thread_target_vector = [np.array(map(translatelabel, 
                                                    [id_target_dic[i] 
                                                                for i in id_order]))]
    
                if event in event_model_dic:
                    event_target_dic[event] += thread_target_vector
                else:
                    event_target_dic[event] = thread_target_vector
       
    #        pp.pprint(structure)
            edge_vector = np.array([np.array([id_dic[Id] for Id in edge]) 
                                                            for edge in edge_list])
    
            n_feats = np.array([thread_dic[i] for i in id_order])
            X_train = [np.array([n_feats,edge_vector])]
            if event in event_model_dic:
                event_model_dic[event] += X_train
            else:
                event_model_dic[event] = X_train
            
            if event in event_ID_dic:
                event_ID_dic[event] += [thread_id_list]
            else:
                event_ID_dic[event] = [thread_id_list]
            thread_dic = {}

    event_model_dic = ["_".join([token_type,embed_type,dims]),event_model_dic]
    
    with open("event_model_dic","w")as modelfile:
        pickle.dump(event_model_dic,modelfile)
    
    with open("event_target_dic","w")as modelfile:
        pickle.dump(event_target_dic,modelfile)
    
    with open("event_ID_dic","w")as modelfile:
        pickle.dump(event_ID_dic,modelfile)
    
    print( event_ID_dic.keys())
    #print graph_size
    #print graph_event, graph_root_id
    print(graph_2_vis) 
    #DG=nx.DiGraph()
    #DG.add_edges_from(graph_2_vis)
    #nx.draw_random(DG, with_labels=False)
    
    
    #from networkx.drawing.nx_agraph import graphviz_layout
    #
    ##nx.draw_spectral(DG, with_labels=False)
    ##pos=nx.graphviz_layout(DG, prog='dot')
    #pos=graphviz_layout(DG, prog='dot')
    #nx.draw(DG, pos, with_labels=False, arrows=False)
    #from networkx.drawing.nx_pydot import to_pydot
    
    #import pydot_ng as pydot
    ##import graphviz
    #Gp = pydot.graph_from_edges(graph_2_vis)
    #Gp.write_png('example1_graph.png')
    
    
    #nx.draw_graphviz(DG)
    #plt.show()
    #label_count = coll.Counter(label_list)
    #print label_count
