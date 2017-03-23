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
import collections as coll
import re
import feature_functions as feature
import nested_dict
pp = pprint.PrettyPrinter(indent=0)



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
#top_path = "\\".join([train_dir,train_data_dir,rumor_dirs["charlie_hebdo"]])

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
with open(doc2vec_dir+token_type+"id_text_dic.json",'r')as textDicFile:
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
model = models.Doc2Vec.load(doc2vec_dir+token_type+'rumorEval_doc2vec_set'+dims+'.model')
print model.most_similar('black'),"\n"
print model["black"]


#structure ={"553548567420628992":{"553549149787140096":{"553550408346779648":{"553551840428949504":{"553552036915335169":{"553553247953514496":{"553553754424115200":{"553554620229115905":{"553555066754695168":{"553555725084270593":[]}}}}},"553552100417110017":[]}}},"553551001077424128":[],"553552287889494017":[],"553552395704082432":[],"553552625724301314":[],"553553255255781376":[],"553554289835376643":[],"553559162018611201":{"553560292635189248":{"553561410920521729":{"553562623200210944":{"553565149790224387":[]}}}},"553559527216656385":[]}}
#
#adj_list,id_dic = dic2mat.dic_2_node_lists(structure)
#
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
        with open(source_path+"\\"+root_id,"r")as jsonfile:
            json_list.append(json.load(jsonfile))
        for json_path in current_dir[-1]:
            with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
                json_list.append(json.load(jsonfile))
        for filedic in json_list:
            text =filedic['text']
            ID = filedic['id_str']
            attribute_paths = [[u'entities',u'media'],
                               [u'entities',u'urls'],
                               [u'in_reply_to_screen_name']]
            format_binary_vec = list(feature.attribute_binary_gen(filedic, attribute_paths))
            feature_vector += format_binary_vec
            punc_vec = list(feature.punc_binary_gen(text,punc_list))
            feature_vector += punc_vec
            if token_type == "zub_":
                cap_ratio = feature.zub_capital_ratio(text)
            elif token_type == "twit_":
                print "ERROR write a better captial ratio function"
                break
            feature_vector += cap_ratio
            word_char_count = feature.word_char_count(id_text_dic[ID])
            feature_vector += word_char_count
            swear_bool = feature.word_bool(text,swear_list)
            feature_vector += swear_bool
            neg_bool = feature.word_bool(text,negationwords)
            feature_vector += neg_bool
            pos_vec = id_pos_dic[filedic["id"]]
            feature_vector += feature.pos_vector(pos_vec)
            thread_dic[ID] = feature_vector
        structure = nested_dict.subset_by_key(structure, thread_dic.keys())
        size = len(nested_dict.all_keys(structure))
        edge_list = np.array(nested_dict.to_edge_list(structure))
        if 103>size>graph_size:
            graph_2_vis = edge_list
            graph_size = size
            graph_event = event
            graph_root_id =root_id
        id_dic = feature.id_index_dic(edge_list)
        
        id_order = [i[0] for i in sorted(id_dic.items(),
                                            key=lambda (k,v):(v,k))]
#        pp.pprint(structure)

        feats = [np.array([thread_dic[i] for i in id_order])]
        if event in event_model_dic:
            event_model_dic[event] += feats
        else:
            event_model_dic[event] = feats
        
        thread_dic = {}


print type(event_model_dic['ebola-essien'])
with open("event_model_dic","w")as modelfile:
    pickle.dump(event_model_dic,modelfile)

print graph_size
print graph_event, graph_root_id
print graph_2_vis 
DG=nx.DiGraph()
DG.add_edges_from(graph_2_vis)
nx.draw(DG, with_labels=False)

#nx.draw_graphviz(DG)
#plt.show()