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
# Open the file (make sure its in the same directory as this file)
        

"""created the model with the below code"""


sentences = models.doc2vec.LabeledLineSentence("10k_reviews_doc2vec.txt")#yelp_data_small(words="sent_doc2vec", labels="label_doc2vec")
model = models.Doc2Vec(sentences, size=100, window=8, min_count=0, workers=4)
model.save('doc2vec10k')
model.init_sims(replace=True)
model.save('doc2vec10k_set')

print model.most_similar('chinese')
print model['chinese']
