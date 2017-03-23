# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:51:10 2017

@author: scram
"""



def all_keys(dic):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
    if isinstance(dic,dict):
        return dic.keys()+[key for subdic in dic.itervalues() 
                                   if isinstance(subdic,dict) 
                                       for key in all_keys(subdic)]
    else:
        return []

def to_edge_list(dic):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
#    print "\n",dic
    if isinstance(dic,dict):
        return [(k,i) for k,v in dic.items() for i in v]+[ 
               tup for subdic in dic.itervalues() for tup in to_edge_list(subdic)]
    else:
        return dic
    
def subset_by_key(dic, keys2keep):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
    return {k:subset_by_key(v, keys2keep) 
            if isinstance(v,dict) else v 
                for k,v in dic.items() 
                    if k in keys2keep} 
    

def subset_of_keys(dic, keys2keep):
    """
    TODO:
        negative_sets iie. all keys but
        Test against all types 
        handle python recursion limit
    """
    if isinstance(dic,dict):
        return dic.keys()+[key for subdic in dic.itervalues() 
                                   if isinstance(subdic,dict) 
                                       for key in subset_of_keys(subdic,keys2keep) if key in keys2keep]
    else:
        return dic
    



def key_at_depth(dic, dpt):
    """ From koffein
        http://stackoverflow.com/questions/20425886/python-how-do-i-get-a-list-of-all-keys-in-a-dictionary-of-dictionaries-at-a-gi
    """
    if dpt > 0:
        return [key for subdic in dic.itervalues() if isinstance(subdic,dict) 
                         for key in key_at_depth(subdic, dpt-1) ]
    else:
        if isinstance(dic,dict):
            return dic.keys()
        else:
            return []



 
    
def value_all_depth(dic):
    """ STILL WORKING ON
    lit comprehension from Martijn Pieters
        http://stackoverflow.com/questions/28015458/list-comprehension-to-flatten-a-dictionary-of-dictionaries"""
    if isinstance(dic,dict):    
        return [v for nested in dic.itervalues() for v in nested.itervalues()]
    else:
        return 


