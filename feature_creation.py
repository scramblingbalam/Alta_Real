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

structure = {}
 
A = np.zeros((len(id_list),len(id_pos_dic)),dtype=np.int)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return it.chain.from_iterable(listOfLists)

def deep_dic2adj_mat(dic,key_list=None,adj_mat=None):
    print key_list
    if key_list:
        print len(key_list)
    for k,v in dic.items():
        parent = k
        if v:
            children = v.keys()
            if adj_mat == None:
                adj_mat =[[0]]
                for child in children:
                    adj_mat[0].append(1)
                for child in children:
                    adj_mat.append([1]+[0]*len(children))
            elif key_list:
                len(key_list)
                
            if not key_list:
                key_list = [parent]
                for child in children:
                    key_list.append(child)
            else:
                for child in children:
                    key_list.append(child)
                
            deep_dic2adj_mat(v,key_list,adj_mat)
        else:
            return key_list,adj_mat
        
        
def reach(travel_dict, x, visited=None):
    if visited is None:
        visited = set() # see note
    visited.add(x)
    for y in travel_dict.get(x, []):
        if y not in visited:
            yield y
            for z in reach(travel_dict, y, visited):
                yield z
                
#for y in reach(travel_dict, x):
#    print("you can go to", y)
    


def deep_dic2adj_mat(dic):
    if isinstance(dic,dict):
        for k,v in dic.items():
            if isinstance(v,dict):
                children = v.keys()
                for child in children:
                    yield (k,child)
#                for i in deep_dic2adj_mat(v):
#                    yield list(i)
            else:
                yield deep_dic2adj_mat(v)
    else:
        yield deep_dic2adj_mat(dic)   
#def dicts(t): return {k: dicts(t[k]) for k in t}

def get_child_perms(self, folder, request, perm_list):
    # Folder contains other folders
    children =  folder.get_children()
    if children:
        # For every sub-folder
        return [self.get_child_perms(subfolder, request, perm_list)
                for subfolder in children]
        
    return [folder.has_read_permission(request)]

def deep_dic2adj_mat(dic, memo = [], parent = None):
    if parent == None:
        for k, v in dic.items():
            if isinstance(v,dict):
                memo += [(k,child) for child in v.keys()]
                return memo + [deep_dic2adj_mat(v,memo, chi) for chi in v.keys()]
            else:
                return memo + []
    else:
        for k, v in dic.items():
            if isinstance(v,dict):
                memo += [(k,child) for child in v.keys()]
                return memo + [deep_dic2adj_mat(v,memo, chi) for chi in v.keys()]
            else:
                return memo + [parent]
            
#def deep_dic2adj_mat(dic, parent = None):
#    if not isinstance(dic,dict):
#        pass
#    if parent == None:
#        for k, v in dic.items():
#            if isinstance(v,dict):
#                for child in v.keys():
#                    yield (k,child)
#    else:
#        


           
#def deep_dic2adj_mat(dic, tup=None):
#    for k,v in dic.items(): 
#        print v,"V"
#        if not isinstance(v,dict):
#            return [(k,tup)]
#        else:
#            for child in v.keys():
#                print k,"PArent"
#                print child,"Child"
#                tup = (k,child)
#                return [tup] + deep_dic2adj_mat(v,child)

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
 
print"\n"
for current_dir in walk:
    if 'structure.json' in current_dir[-1]:
        if A.any():
            G = nx.from_numpy_matrix(np.array(A)) 
            nx.draw(G, with_labels=True)
        root_id = long(current_dir[0].split("\\")[-1])
#        print root_id, "root",root_id in id_list
        with open(current_dir[0]+"\\"+'structure.json',"r")as jsonfile:
                structure = json.load(jsonfile)
#        for k,v in structure.items():
#                print structure
#                print k
#                print v.keys()
#   
        if len(structure.keys()) >1:
            print current_dir
            pp.pprint(structure)
            print "\n##################################"
#        print "\n"
#        test =[]
#        for k,v in structure.items():
#            test.append(k)
#            test += v.keys()
#            for k1,v1 in v.items():
#                test.append(k1)
#                if v1:
#                    test += v1.keys()
#                for k2,v2 in structure.items():
#                    test.append(k2)
#                    if v2:
#                        test += v2.keys()
##        print test
#        struc =deep_dic2adj_mat(structure)
#        print struc,"\n"
#        for i in struc:
#            print i,"I"
#            for j in i:
#                print j

                
#        for i in [(k,v) for k,V in structure.items() for v in V.keys()]:
#            print i

#for current_dir in walk:
#    if 'structure.json' in current_dir[-1]:
#        if A.any():
#            G = nx.from_numpy_matrix(np.array(A)) 
#            nx.draw(G, with_labels=True)
#        root_id = long(current_dir[0].split("\\")[-1])
##        print root_id, "root",root_id in id_list
#        with open(current_dir[0]+"\\"+'structure.json',"r")as jsonfile:
#                structure = json.load(jsonfile)
#    last_dir = current_dir[0].split("\\")[-1]
#    if last_dir == "source-tweet" or last_dir == "replies":
#        for json_path in current_dir[-1]:
##            print "#########\n",current_dir[0],json_path,"######\n"
#            with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
#                filedic = json.load(jsonfile)
#                if filedic["lang"] =="en":
#                    # the two conditionals below will be used to build the tree structure
#    #                if last_dir == "source-tweet":
#    #                    source_id = current_dir[0].split(".")[0]
#    #                if last_dir == "replies":
#                    encoded_text = filedic["text"].replace("\n","").encode("UTF-8")
#                    twt_id = filedic["id"]
#                    print "\t",twt_id,"id"
#                    print structure
#                    print structure[str(root_id)][twt_id]
##                    print encoded_text,"\n"
#                    tokenizer = nltk.RegexpTokenizer(r'\w+|[^\w\s]+')
##                    tokenizer = nltk.RegexpTokenizer(u'\w+|[^\w\s\\U]+')
##                    print [tok for tok in nltk.word_tokenize(filedic["text"].replace("\n",""))],"\n"
##                    print " ".join(tokenizer.tokenize(filedic["text"].replace("\n",""))),"\n########################\n"
#                    id_text_dic[twt_id] = encoded_text
#                    text_list.append(encoded_text)
#                    id_list.append(twt_id)


                
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