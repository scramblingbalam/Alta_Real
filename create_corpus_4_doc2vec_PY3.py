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

id_text_dic = {}
text_list = []
id_list = []

walk = os.walk(top_path)

source_id = ""
reply_id = ""

#grah_up_dic = {}
#graph_down_dic = {}
#graph_tup = ()

for current_dir in walk:
    last_dir = current_dir[0].split("\\")[-1]
    if last_dir == "source-tweet" or last_dir == "replies":
        for json_path in current_dir[-1]:
            with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
                filedic = json.load(jsonfile)
                if filedic["lang"] =="en":
                    # the two conditionals below will be used to build the tree structure
    #                if last_dir == "source-tweet":
    #                    source_id = current_dir[0].split(".")[0]
    #                if last_dir == "replies":
                    text_in = filedic["text"].replace("\n","N3WL1N3")#+'\r\n'
                    print(text_in)
                    encoded_text = " ".join(twit_token.ize(text_in))
                    id_text_dic[filedic["id"]] = encoded_text
                    text_list.append(encoded_text)
                    id_list.append(filedic["id"])
                
# I save all the containers I use to create teh doc2vec training file 
# I do this to make sure that debugging doc2vec will be easy and 
# I'll have all the data I need to ask any question I want to
                 
doc2vec_dir ="Data/doc2vec/"
with open(doc2vec_dir+"id_text_dic.cpickle","wb") as picfile:
    pickle.dump(id_text_dic,picfile)

with open(doc2vec_dir+"text_list.cpickle","wb") as picfile:
    pickle.dump(text_list,picfile)    
    
with open(doc2vec_dir+"id_list.cpickle","wb") as picfile:
    pickle.dump(id_list,picfile)     


with open(doc2vec_dir+"doc2vec_train_corpus.txt","wb")as corpusfile:
#    for txt in text_list:
#        print(txt,file=corpusfile)
    corpusfile.writelines([txt.encode("utf8")+"\r\n".encode("utf8") for txt in text_list])


#test_dic = {}    
#with open(doc2vec_dir+"id_text_dic.cpickle","rb") as picfile:
#    test_dic = pickle.load(picfile)
#
#for k,v in test_dic.items():
#    print k
#    print v
#    print "\n"

print(uniD.name(u"Å").split()[0] == "LATIN")
#print uniD.name(u"😱")