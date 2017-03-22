# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:51:10 2017

@author: scram
"""

def keys_all_depths(dic):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
    if isinstance(dic,dict):
        return dic.keys()+[key for subdic in dic.itervalues() 
                                   if isinstance(subdic,dict) 
                                       for key in keys_all_depths(subdic)]
    else:
        return []

def dict_key_subset(dic, keys2keep):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
    if isinstance(dic,dict):
        return dic.keys()+[key for subdic in dic.itervalues() 
                                   if isinstance(subdic,dict) 
                                       for key in dict_key_subset(subdic,keys2keep) if key in keys2keep]
    else:
        return dic
    

def dict_subset(dic, keys2keep):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
    return {k:dict_subset(v, keys2keep) 
            if isinstance(v,dict) else v 
                for k,v in dic.items() 
                    if k in keys2keep} 

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


