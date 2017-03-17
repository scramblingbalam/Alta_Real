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
import cPickle as pickle
import sys
# Open the file (make sure its in the same directory as this file)
        

"""created the model with the below code"""
args = sys.argv
if len(args) > 1:
    dims = int(args[1])
else:
    dims = 300



doc2vec_dir ="Data/doc2vec/"

token_type = "zub_"
sentences = models.doc2vec.TaggedLineDocument(doc2vec_dir+token_type+"doc2vec_train_corpus.txt")#yelp_data_small(words="sent_doc2vec", labels="label_doc2vec")
model_zub = models.Doc2Vec(sentences, size=dims, window=8, min_count=0, workers=4)
dims = str(dims)
model_zub.save(doc2vec_dir+token_type+"doc2vec10k"+dims+".model")
model_zub.init_sims(replace=True)
model_zub.save(doc2vec_dir+token_type+"doc2vec10k_set"+dims+".model")


dims =int(dims)
token_type = "twit_"
sentences = models.doc2vec.TaggedLineDocument(doc2vec_dir+token_type+"doc2vec_train_corpus.txt")#yelp_data_small(words="sent_doc2vec", labels="label_doc2vec")
model_twit = models.Doc2Vec(sentences, size=dims, window=8, min_count=0, workers=4)
dims = str(dims)
model_twit.save(doc2vec_dir+token_type+"doc2vec10k"+dims+".model")
model_twit.init_sims(replace=True)
model_twit.save(doc2vec_dir+token_type+"doc2vec10k_set"+dims+".model")

print "\n"
print model_zub.most_similar('black')
print "\n"
print model_twit.most_similar('black')

