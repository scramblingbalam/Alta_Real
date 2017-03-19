# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:12:09 2017

@author: scram
"""
import itertools as it
import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent=0)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return it.chain.from_iterable(listOfLists)

    
def walk(dic, parent=None, mem_set = None, adj=None):
    if not isinstance(dic,dict):
        return adj
    else:
#        print adj,"DIC"
        if parent is None and mem_set is None:
            mem_set = set()
            for k,v in dic.items():
                if v:
                    parent = k
#                    print k, "K"
#                    print v, "V"
                    return walk(v,parent,mem_set)
                else:
                    pass
        elif adj is None:
#            print "ADJ_None"
            adj = []
            for k,v in dic.items():
                edge = (parent,k)
                if edge not in mem_set:
                    adj.append(edge)
                mem_set.add(edge)
#                print adj,"ADJ_"
            for k,v in dic.items():
#                print adj,"ADJ"
                if isinstance(v,dict):
                    adj = walk(v,k,mem_set,adj)
            return adj
        else:
            for k,v in dic.items():
                edge = (parent,k)
                if edge not in mem_set:
                    adj.append(edge)
                mem_set.add(edge)
            walk_out =[list(flatten(walk(v,k,mem_set,adj))) for k,v in dic.items()]
            return walk_out
            
              
def dic_2_adj_mat(Dic):
    out = walk(Dic)[-1]
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

def dic_2_node_lists(Dic):
    out = walk(Dic)[-1]
    unique_out =[]
    out_set = set()
    for i in out:
        if i not in out_set:
            unique_out.append(i)
            out_set.add(i)   
    id_dic = {ID:num for num,ID in enumerate(unique_out)}
    walk_out = list(set([( id_dic[parent], id_dic[child] )
            for parent,child in 
                zip(out[::2],out[1::2])]))
    return np.array(walk_out), id_dic