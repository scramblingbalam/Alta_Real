# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:59:51 2017

@author: scram
"""

import cPickle as pickle

event_feature_dic ={}
with open("event_model_dic","r")as modelfile:
    event_feature_dic =pickle.load(modelfile)
    
for thread in event_feature_dic['ebola-essien']:
    print "\n\n",thread,len(thread)
    for i in thread:
        print "\t",i,len(i)