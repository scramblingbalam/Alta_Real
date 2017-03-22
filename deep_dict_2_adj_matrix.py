# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:12:09 2017

@author: scram
"""
import itertools as it
import numpy as np
import pprint
import nested_dict
pp = pprint.PrettyPrinter(indent=0)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return it.chain.from_iterable(listOfLists)

    
def walk(dic):
    """
    TODO:
        Test against all types 
        handle python recursion limit
    """
    if isinstance(dic,dict):
        return [(key,subkey) for key,subdic in dic.items() 
                                   if isinstance(subdic,dict) 
                                       for subkey in nested_dict.all_keys(subdic)]
    else:
        return dic


              
def dic_2_adj_mat(Dic):
    unique_out =[]
    out_set = set()
    for i in out:
        if i not in out_set:
            unique_out.append(i)
            out_set.add(i)   
    id_dic = {ID:num for num,ID in enumerate(unique_out)}
    walk_out = list(set([(parent,child) 
            for parent,child in 
                zip(out[::2],out[1::2])]))
    adj_mat =np.zeros((len(walk_out)+1,len(walk_out)+1))
    for i,j in walk_out:
        adj_mat[id_dic[i],id_dic[j]]=1
    return adj_mat, id_dic

def dic_2_node_lists(edge_list):
    out = edge_list
    unique_out =[]
    out_set = set()
    for i in out:
        if i not in out_set:
            unique_out.append(i)
            out_set.add(i)   
    id_dic = {ID:num for num,ID in enumerate(unique_out)}
    return np.array(walk_out), id_dic

