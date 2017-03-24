# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 18:07:03 2017

@author: scram
"""
import json
#import pickle
#import twit_token
import nltk
import numpy as np
import re
import collections as coll
import pprint
pp = pprint.PrettyPrinter(indent=0)

def mean_W2V_vector(text,model):
    return np.mean(np.vstack([model[word] for word in text.split()]),0)

def pos_extract(path):
    pos_tweets = []
    with open(path,"r")as POSfile:
        pos_tweets = [json.loads(twt) for twt in POSfile.readlines()]
    #create set of all used POS tags
    pos_tag_set = set([pos['category'] for twt in pos_tweets for pos in twt[u'entities'][u'Token']])

    #create dictionary of POS_Tags and vector indicies
    pos_index_dic = {pos:num for num,pos in enumerate(pos_tag_set)}
    #create inverse lookup dictionary
    i_p_dic = {num:pos for num,pos in enumerate(pos_tag_set)}
    # create dictionary of POS tag lists for keyed by ID 
    dic = {twt['id']:twt[u'entities'][u'Token'] for twt in pos_tweets if 'id' in twt}
    id_p_dic ={}
    for K,V in dic.items():
        vector = []
        for v in V:
            vector.append(pos_index_dic[v['category']])
        id_p_dic[K]=vector
    id_p_dic = {K:[pos_index_dic[v['category']] for v in V] for K,V in dic.items()}
    return id_p_dic, i_p_dic

def pos_vector(index_vector):
    count = coll.Counter(index_vector)
    return [count[i] if i in count else 0 for i in range(49)]

def word_bool(text,word_list,cont="*"):
    if cont:
        word_list = [string.replace("\n","") for string in word_list]
        word_list = [s.replace(cont,"")+" " if s[-1] != "*" else s for s in word_list]
        word_list = [" "+s.replace(cont,"") if s[0] != "*" else s for s in word_list]
    
    bad_list= [swear for swear in word_list if swear in text]
    return [int(bool(bad_list))]
        

def word_char_count(text):
    return [len(text.split()),len(text)]


def zub_capital_ratio(text):
    alpha_text = " ".join(nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '', text )))
    return [float(sum([char.isupper() for char in alpha_text]))/float(len(alpha_text))]


def punc_binary_gen(text,puncs):
    for punc in puncs:
        yield int(np.array([char==punc for char in text]).any())

        
def entitiy_binary_gen(tweet_dic,key_list):
    """ Takes a tweets json dic and a list of keys from the entities attribute
        possible keys are
        [u'user_mentions', u'media', u'hashtags', u'symbols', u'trends', u'urls']
    """
    for key in key_list:
        if key in tweet_dic['entities']:
            yield int(bool(tweet_dic['entities'][key]))
        else:
            yield int(False)


def dic_path_recurse(dic, path):
    key = path.pop(0)
    try:
        out = dic[key]
        if out and isinstance(out,dict):
            return dic_path_recurse(out,path)
        else:
            return out
    except:
        return False

    
def attribute_binary_gen(tweet_dic,path_list):
    """ Takes a tweets json dic and a list of keys from the entities attribute
            possible top level keys:
        [u'favorited', u'retweet_count', u'in_reply_to_user_id', u'contributors', 
        u'truncated', u'retweeted', u'in_reply_to_status_id_str', u'coordinates',
        u'filter_level', u'in_reply_to_status_id', u'place', u'favorite_count',
        u'extended_entities', u'in_reply_to_screen_name', u'metadata', u'geo', 
        u'in_reply_to_user_id_str', u'possibly_sensitive', u'possibly_sensitive_appealable']
        Note: [u'filter_level', u'extended_entities', u'metadata'] can be absent
            possible keys are for 'entity'
        [u'user_mentions', u'media', u'hashtags', u'symbols', u'trends', u'urls']
        Note: [u'media'] can be absent and recursion raises exception & returns False
    """
    for path in path_list:
            yield int(bool(dic_path_recurse(tweet_dic, path)))


def id_index_dic(edge_list):
    out = [ID for edge in edge_list for ID in edge]
    unique_out =[]
    out_set = set()
    for i in out:
        if i not in out_set:
            unique_out.append(i)
            out_set.add(i)   
    id_dic = {ID:num for num,ID in enumerate(unique_out)}
    return id_dic




