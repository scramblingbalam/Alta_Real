# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 16:32:18 2017

@author: Colin Dryaton cdrayton@umich.edu
"""


import json
import os
import pickle
#import cPickle as pickle
import twit_token
import unicodedata as uniD
import nltk
import re


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

structutr_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1,"structure.json"])
source_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_2,"source-tweet","498280126254428160.json"])
ferg_1_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1])
ferg_2_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_2])
ferg_3_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_3])
ferg_4_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_4])
ferg_5_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_5])
ferg_6_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_6])
ferg_7_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_7])

top_path = "/".join([train_dir,train_data_dir])
#top_path = ferg_1_path 

zub_id_text_dic = {}
twit_id_text_dic = {}

zub_text_list = []
twit_text_list = []

id_list = []

walk = os.walk(top_path)

source_id = ""
reply_id = ""

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
                
# I save all the containers I use to create teh doc2vec training file 
# I do this to make sure that debugging doc2vec will be easy and 
# I'll have all the data I need to ask any question I want to
                 
doc2vec_dir ="Data/doc2vec/"
with open(doc2vec_dir+"twit_id_text_dic.cpickle","wb") as picfile:
    pickle.dump(twit_id_text_dic,picfile)

with open(doc2vec_dir+"twit_text_list.cpickle","wb") as picfile:
    pickle.dump(twit_text_list,picfile)    
    
with open(doc2vec_dir+"twit_doc2vec_train_corpus.txt","wb")as corpusfile:
    corpusfile.writelines([txt.encode("utf8")+"\r\n".encode("utf8") for txt in twit_text_list])



with open(doc2vec_dir+"zub_id_text_dic.cpickle","wb") as picfile:
    pickle.dump(zub_id_text_dic,picfile)

with open(doc2vec_dir+"zub_text_list.cpickle","wb") as picfile:
    pickle.dump(zub_text_list,picfile)    

print(zub_text_list[0])    
print(type(zub_text_list[0]))
with open(doc2vec_dir+"zub_doc2vec_train_corpus.txt","wb")as corpusfile:
    corpusfile.writelines([txt.encode("utf8")+"\r\n".encode("utf8") for txt in zub_text_list])



with open(doc2vec_dir+"id_list.cpickle","wb") as picfile:
    pickle.dump(id_list,picfile)     


