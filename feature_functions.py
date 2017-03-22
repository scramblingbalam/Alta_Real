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
import itertools as it
import pprint
pp = pprint.PrettyPrinter(indent=0)


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


ID_ORDER = [u'553588178687655936', u'553593923659382784']
structure = {u'553588178687655936': {u'553588358044483584': [],
                       u'553588472330452992': [],
                       u'553588570368532480': [],
                       u'553588750207680512': [],
                       u'553588869409832960': [],
                       u'553589038196981760': [],
                       u'553589124125323264': [],
                       u'553589955029512192': [],
                       u'553590627343302657': [],
                       u'553591897458237440': [],
                       u'553593015416008704': [],
                       u'553593923659382784': []}}

ID_ORDER = [u'553588178687655936', u'553593923659382784']
structure_test = {u'553588178687655936': {u'test':{u'553588358044483584': []},
                       u'553588472330452992': [],
                       u'553588570368532480': [],
                       u'553588750207680512': [],
                       u'553588869409832960': [],
                       u'553589038196981760': [],
                       u'553589124125323264': [],
                       u'553589955029512192': [],
                       u'553590627343302657': [],
                       u'553591897458237440': [],
                       u'553593015416008704': [],
                       u'553593923659382784': []}}

ID_ORDER2 =[u'553587013409325058',
            
            u'553587193772793856',
            
            u'553587135274815488', 
            
            u'553587609759666177',
            
            u'553587377835614209', u'553587741720854528',
            
            u'553587387889373186',u'553587794686513153',
            
            u'553587285074386944',
            
            u'553587435511484416',u'553587810859757569',u'553588214859325440',
                                    u'553588069610569729',
            
            u'553587599856906241',
            
            u'553587582962253824', u'553587246516174849', u'553587589417304065', 
            u'553587134838620160', u'553587586241794050', u'553587103922020352', 
            u'553587395942420480', u'553587551131283458', u'553587383397253120', 
            u'553587422445846529', u'553587160088338432',  
             u'553647665695956992', u'553588737750605825', 
            u'553587882741747713', u'553588653562150912', u'553588971864084481', 
               
            u'553588091433537536', u'553587912949121024', u'553588640052674560', 
            u'553589243583672320', u'553589959937257472']

structure2 ={u'553587013409325058': {u'553587103922020352': [],
                       u'553587134838620160': [],
                       u'553587135274815488': [],
                       u'553587160088338432': [],
                       u'553587193772793856': [],
                       u'553587246516174849': [],
                       u'553587285074386944': [],
                       u'553587377835614209': {u'553587741720854528': []},
                       u'553587383397253120': {u'553587912949121024': {u'553588640052674560': {u'553589243583672320': {u'553589959937257472': []}}},
                                              u'553588091433537536': []},
                       u'553587387889373186': {u'553587794686513153': [],
                                              u'553587882741747713': [],
                                              u'553588653562150912': [],
                                              u'553588737750605825': [],
                                              u'553588971864084481': [],
                                              u'553647665695956992': []},
                       u'553587395942420480': [],
                       u'553587422445846529': [],
                       u'553587435511484416': {u'553587810859757569': {u'553588214859325440': []},
                                              u'553588069610569729': []},
                       u'553587551131283458': [],
                       u'553587582962253824': [],
                       u'553587586241794050': [],
                       u'553587589417304065': [],
                       u'553587599856906241': [],
                       u'553587609759666177': []}}
                       

ALLKEYS2 =[u'553587013409325058',u'553587103922020352',u'553587134838620160',
           u'553587135274815488',u'553587160088338432',u'553587193772793856',
           u'553587246516174849',u'553587285074386944',u'553587377835614209',
           u'553587741720854528',u'553587383397253120',u'553587912949121024',
           u'553588640052674560',u'553589243583672320',u'553589959937257472',
           u'553588091433537536',u'553587387889373186',u'553587794686513153',
           u'553587882741747713',u'553588653562150912',u'553588737750605825',
           u'553588971864084481',u'553647665695956992',u'553587395942420480',
           u'553587422445846529',u'553587435511484416',u'553587810859757569',
           u'553588214859325440',u'553588069610569729',u'553587551131283458',
           u'553587582962253824',u'553587586241794050',u'553587589417304065',
           u'553587599856906241',u'553587609759666177']
                       

THREAD_KEYS2=[u'553587013409325058', u'553587609759666177', u'553587377835614209',
             u'553587794686513153', u'553587387889373186', u'553647665695956992',
             u'553588737750605825', u'553587586241794050', u'553587741720854528', 
             u'553588653562150912', u'553587882741747713', u'553587395942420480', 
             u'553588971864084481', u'553587589417304065', u'553587422445846529', 
             u'553587160088338432']

TooDEL2 = [u'553587193772793856', u'553587383397253120', u'553587810859757569', 
       u'553588069610569729', u'553587135274815488', u'553587435511484416', 
       u'553587582962253824', u'553589243583672320', u'553587246516174849', 
       u'553587912949121024', u'553587285074386944', u'553589959937257472', 
       u'553587103922020352', u'553588640052674560', u'553587551131283458', 
       u'553588214859325440', u'553587134838620160', u'553588091433537536', 
       u'553587599856906241']
Delout2=[u'553587193772793856', u'553587135274815488'] 
STRUCToutKEYS = [u'553587013409325058',u'553587609759666177',u'553587377835614209',
                 u'553587741720854528',u'553587387889373186',u'553587794686513153',
                 u'553647665695956992',u'553588737750605825',u'553587882741747713',
                 u'553588653562150912',u'553588971864084481',u'553587285074386944',
                 u'553587435511484416',u'553587810859757569',u'553588214859325440',
                 u'553588069610569729',u'553587599856906241',u'553587582962253824',
                 u'553587246516174849',u'553587589417304065',u'553587134838620160',
                 u'553587586241794050',u'553587103922020352',u'553587395942420480',
                 u'553587551131283458',u'553587383397253120',u'553588091433537536',
                 u'553587912949121024',u'553588640052674560',u'553589243583672320',
                 u'553589959937257472',u'553587422445846529',u'553587160088338432']
print len(STRUCToutKEYS),len(TooDEL2),len(THREAD_KEYS2)
# GOOD: No keys in KEYS_2_KEEP where DELETED
# BAD: KEYS that shoudl have been deleted where not marked with ### 
NEWstructure2 ={u'553587013409325058': {553587103922020352: [],
                         553587134838620160 : [],
                       553587135274815488 : [],#!!
                       u'553587160088338432': [],
                       553587193772793856 : [],
                         553587246516174849 : [],
                         553587285074386944 : [],###
                       u'553587377835614209': {u'553587741720854528': []},
                         553587383397253120 : {  553587912949121024 : {553588640052674560: {553589243583672320: {553589959937257472: []}}},
                                                 553588091433537536 : []},
                       u'553587387889373186': {u'553587794686513153': [],
                                               u'553587882741747713': [],
                                               u'553588653562150912': [],
                                               u'553588737750605825': [],
                                               u'553588971864084481': [],
                                               u'553647665695956992': []},
                       u'553587395942420480': [],
                       u'553587422445846529': [],
                         553587435511484416 : { 553587810859757569 : { 553588214859325440: []},
                                                553588069610569729 : []},
                         553587551131283458 : [],
                         553587582962253824 : [],
                       u'553587586241794050': [],
                       u'553587589417304065': [],
                         553587599856906241 : [],
                       u'553587609759666177': []}}


deltest ={1:{10:{100:{110:[],
                      111:[]}},
            11:[],
            20:{200:{220:[],
                 222:[]}},
            22:[]}
        }
ALLKEYStest =[1,10,100,110,111,11,20,200,220,222,22]
ID_ORDERtest = [1,10,20,200,222,22]
ID_ORDERfalse_test =[1,10,111,20,200,222,22]

def key_at_depth(dic, dpt):
     if dpt > 0:
         return [key for subdic in dic.itervalues() if isinstance(subdic,dict) 
                         for key in key_at_depth(subdic, dpt-1) ]
     else:
         if isinstance(dic,dict):
             return dic.keys()
         else:
             return []


def keys_all_depths(dic):
    if isinstance(dic,dict):
        return dic.keys()+[key for subdic in dic.itervalues() 
                                   if isinstance(subdic,dict) 
                                       for key in keys_all_depths(subdic)]
    else:
        return []
    
def value_all_depth(dic):
    if isinstance(dic,dict):    
        return [v for nested in dic.itervalues() for v in nested.itervalues()]
    else:
        return 


def dict_key_subset(dic, keys2keep):
    if isinstance(dic,dict):
        return dic.keys()+[key for subdic in dic.itervalues() 
                                   if isinstance(subdic,dict) 
                                       for key in dict_key_subset(subdic,keys2keep) if key in keys2keep]
    else:
        return dic
    

def dict_subset(dic, keys2keep):
    return {k:dict_subset(v, keys2keep) 
            if isinstance(v,dict) else v 
                for k,v in dic.items() 
                    if k in keys2keep} 


keys_in = keys_all_depths(structure2)
new_structure = dict_subset(structure2, THREAD_KEYS2)
keys_out = keys_all_depths(new_structure)
keys_out1 = dict_key_subset(structure2, THREAD_KEYS2)
print set(keys_out1)==set(THREAD_KEYS2)
print "KEYS_OUT vs THEAD",set(keys_out)==set(THREAD_KEYS2),len(keys_out),len(THREAD_KEYS2)
print set(TooDEL2)==set(keys_in)-set(keys_out)
