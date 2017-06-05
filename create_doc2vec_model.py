# -*- coding: utf-8 -*-
"""

Created on Thu Mar 02 16:32:18 2017

@author: Colin Dryaton cdrayton@umich.edu
"""

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
import gensim
#import json
#import pandas as pd
#from glob import glob
#import re
import sys
import json
# Open the file (make sure its in the same directory as this file)
        

"""created the model with the below code"""
args = sys.argv
if len(args) > 1:
    dims = int(args[1])
else:
    dims = 300


LabeledSentence = gensim.models.doc2vec.LabeledSentence
doc2vec_dir ="Data/doc2vec/not_trump"

token_type = "zub_"
#sentences = []
#with open(doc2vec_dir+token_type+"doc2vec_train_corpus.txt",'r')as corpfile:
#    sentences=[sent.split() for sent in corpfile.readlines()]


with open(doc2vec_dir+token_type+"id_text_dic.json",'r')as corpfile:
    sent_dic = json.load(corpfile)
sentences = [LabeledSentence(v.split(),[str(k)]) for k,v in sent_dic.items()]
#sentences = models.doc2vec.TaggedLineDocument(doc2vec_dir+token_type+"doc2vec_train_corpus.txt")#yelp_data_small(words="sent_doc2vec", labels="label_doc2vec")
model_zub = models.Doc2Vec(sentences, size=dims, window=8, min_count=0, workers=4)
dims = str(dims)
model_zub.save(doc2vec_dir+token_type+"rumorEval_doc2vec"+dims+".model")
model_zub.init_sims(replace=True)
model_zub.save(doc2vec_dir+token_type+"rumorEval_doc2vec_set"+dims+".model")

    

dims =int(dims)
token_type = "twit_"
sentences = []
with open(doc2vec_dir+token_type+"id_text_dic.json",'r')as corpfile:
    sent_dic = json.load(corpfile)
sentences = [LabeledSentence(v.split(),[str(k)]) for k,v in sent_dic.items()]
#sentences = models.doc2vec.TaggedLineDocument(doc2vec_dir+token_type+"doc2vec_train_corpus.txt")#yelp_data_small(words="sent_doc2vec", labels="label_doc2vec")
model_twit = models.Doc2Vec(sentences, size=dims, window=8, min_count=0, workers=4)
dims = str(dims)
model_twit.save(doc2vec_dir+token_type+"rumorEval_doc2vec"+dims+".model")
model_twit.init_sims(replace=True)
model_twit.save(doc2vec_dir+token_type+"rumorEval_doc2vec_set"+dims+".model")

print("\n")
print(model_zub.most_similar('sad'))
print(model_zub.docvecs.most_similar("552783667052167168"))
#print(model_twit.docvecs.most_similar('155014799909064704'))
print("\n")
#print model_twit.most_similar('black')

#for i in sentences[1130]:
#    print i

#print len(sentences_twit)
#print sentences_twit[0]
#print len(sentences_twit)