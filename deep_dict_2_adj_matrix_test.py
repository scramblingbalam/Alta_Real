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

d={u'305': {u'704': {u'864': [],
                     u'016': [],
                     u'265': {u'648':[],
                              u'056':[]}},
            u'513': {u'136': []},
            u'864': {u'336': [],
                     u'296': [],
                     u'937': [],
                     u'049': {u'971': []}},
            u'752': [],
            u'848': [],
            u'792': [],
            u'088': [],
            u'496': [],
            u'920': [],
            u'481': []}}
    
def walk(dic, parent=None, mem_set = None, adj=None):
    if not isinstance(dic,dict):
        print adj,"NOT_DIC"
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
    return adj_mat 

#adj_matrix = dic_2_adj_mat(d)    
#
#print adj_matrix

adj_list=[
        (u'305',u'704'),
        (u'305',u'513'),
        (u'305',u'864'),
        (u'305',u'752'),
        (u'305',u'848'),
        (u'305',u'792'),
        (u'305',u'088'),
        (u'305',u'496'),
        (u'305',u'920'),
        (u'305',u'481'),
            (u'704',u'864'),
            (u'704',u'016'),
            (u'704',u'265'),
                (u'265',u'648'),
                (u'265',u'056'),
            (u'513',u'136'),
            (u'864',u'336'),
            (u'864',u'296'),
            (u'864',u'937'),
            (u'864',u'049'), 
            (u'049',u'971')
        ]                       

d2 ={u'525023025792835585': {u'525023379481313281': [],
                             u'525024498999783424': [],
                             u'525024680613511169': [],
                             u'525025685820030976': [],
                             u'525025735338381313': [],
                             u'525028433106309121': [],
                             u'525031384029872128': [],
                             u'525032806288601088': [],
                             u'525046262467293184': [],
                             u'525049296794574850': []},
    u'525040225441951744': []}    

al=[(u'525023025792835585',u'525023379481313281'),
    (u'525023025792835585',u'525024498999783424'),
    (u'525023025792835585',u'525024680613511169'),
    (u'525023025792835585',u'525025685820030976'),
    (u'525023025792835585',u'525025735338381313'),
    (u'525023025792835585',u'525028433106309121'),
    (u'525023025792835585',u'525031384029872128'),
    (u'525023025792835585',u'525032806288601088'),
    (u'525023025792835585',u'525046262467293184'),
    (u'525023025792835585',u'525049296794574850')]
   
test_2 = walk(d2)
print set(test_2) == set(al)


{u'500347114975944705': {u'500347712764518400': [],
                       u'500347833774374912': {u'500350502690115584': [],
                                              u'500382101930143745': {u'500382921476145152': []}},
                       u'500348365746737152': {u'500366747506335744': {u'500367139652784128': {u'500367482679746560': {u'500368570724155392': {u'500479738964901889': [],
                                                                                                                                          u'500654216239915008': []}}}},
                                              u'500367241888944130': {u'500368286027354113': {u'500369339628126209': {u'500369701240066048': [],
                                                                                                                   u'500371514127310850': [],
                                                                                                                   u'500371833376350208': []}}},
                                              u'500371547496796162': {u'500372089967476736': {u'500373700974112768': []},
                                                                     u'500373096860487680': {u'500374119725031424': []}}},
                       u'500348806480035841': {u'500350665315450881': {u'500354964838166528': {u'500355777878835200': {u'500356119932719104': []}}},
                                              u'500352847351775234': {u'500355271332757504': {u'500356093801795585': {u'500356545730084864': [],
                                                                                                                   u'500356692560072704': {u'500357394845560835': {u'500357701827039232': {u'500358464325947393': {u'500359435911716864': {u'500360127522693120': []}}}},
                                                                                                                                          u'500357862699192321': [],
                                                                                                                                          u'500358008979722243': {u'500358715992969218': {u'500359336359518208': [],
                                                                                                                                                                                        u'500359448531980288': []}}},
                                                                                                                   u'500356909816631296': {u'500357587997831169': {u'500358410572156928': []}}},
                                                                                            u'500356297519165440': {u'500357390299308032': []},
                                                                                            u'500384144405192704': []}},
                                              u'500356480432754689': {u'500357905968033792': {u'500359294181580800': []}}},
                       u'500348911404728320': [],
                       u'500348984347860992': []},
u'500348815061557248': {u'500351276123979776': []},
u'500360857826889728': [],
u'500383410766872576': {u'500384204585435136': {u'500387834562244610': {u'500388602350940160': []},
                                              u'500388535250079744': []},
                       u'500384274366070784': []},
u'500385664458690560': {u'500386073865125888': {u'500387351453921283': {u'500387829005168641': [],
                                                                     u'500408075816542208': {u'500408562779037696': {u'500409091978969088': []}}}}},
u'500389197618761728': {u'500389896792834049': []},
u'500391351997829120': {u'500392313076871168': []},
u'500395670562697218': [],
u'500395965962932224': [],
u'500396220951842817': {u'500397848425680897': []}}


d3={u'4705': {u'8400': [],
              u'4912': {u'5584': [],
                        u'3745': {u'5152': []}},
              u'7152': {u'5744': {u'4128': {u'6560': {u'5392': {u'1889': [],
                                                                u'5008': []}}}},
                        u'4130': {u'4113': {u'6209': {u'6048': [],
                                                      u'0850': [],
                                                      u'0208': []}}},
                        u'6162': {u'6736': {u'2768': []},
                                  u'7680': {u'1424': []}}},
              u'5841': {u'0881': {u'6528': {u'5200': {u'9104': []}}},
                                              u'5234': {u'7504': {u'5585': {u'4864': [],
                                                                            u'2704': {u'0835': {u'9232': {u'7393': {u'6864': {u'3120': []}}}},
                                                                                      u'2321': [],
                                                                                      u'2243': {u'9218': {u'8208': [],
                                                                                                                                                                                        u'0288': []}}},
                                                                                      u'1296': {u'1169': {u'6928': []}}},
                                                                                            u'5440': {u'8032': []},
                                                                                            u'2704': []}},
                                              u'4689': {u'3792': {u'0800': []}}},
                       u'8320': [],
                       u'0992': []},
u'7248': {u'9776': []},
u'9728': [],
u'2576': {u'5136': {u'4610': {u'0160': []},
                    u'9744': []},
                    u'0784': []},
u'0560': {u'5888': {u'1283': {u'8641': [],
                              u'2208': {u'7696': {u'9088': []}}}}},
u'1728': {u'4049': []},
u'9120': {u'1168': []},
u'7218': [],
u'2224': [],
u'2817': {u'0897': []}}



al3={u'500347114975944705': {u'500347712764518400': [],
                             u'500347833774374912': {u'500350502690115584': [],
                                                     u'500382101930143745': {u'500382921476145152': []}},
                             u'500348365746737152': {u'500366747506335744': {u'500367139652784128': {u'500367482679746560': {u'500368570724155392': {u'500479738964901889': [],
                                                                                                                                                     u'500654216239915008': []}}}},
                                                     u'500367241888944130': {u'500368286027354113': {u'500369339628126209': {u'500369701240066048': [],
                                                                                                                             u'500371514127310850': [],
                                                                                                                             u'500371833376350208': []}}},
                                                     u'500371547496796162': {u'500372089967476736': {u'500373700974112768': []},
                                                                             u'500373096860487680': {u'500374119725031424': []}}},
                             u'500348806480035841': {u'500350665315450881': {u'500354964838166528': {u'500355777878835200': {u'500356119932719104': []}}},
                                                     u'500352847351775234': {u'500355271332757504': {u'500356093801795585': {u'500356545730084864': [],
                                                                                                                             u'500356692560072704': {u'500357394845560835': {u'500357701827039232': {u'500358464325947393': {u'500359435911716864': {u'500360127522693120': []}}}},
                                                                                                                                                     u'500357862699192321': [],
                                                                                                                                                     u'500358008979722243': {u'500358715992969218': {u'500359336359518208': [],
                                                                                                                                                                                                     u'500359448531980288': []}}},
                                                                                                                                                     u'500356909816631296': {u'500357587997831169': {u'500358410572156928': []}}},
                                                                                                    u'500356297519165440': {u'500357390299308032': []},
                                                                                                    u'500384144405192704': []}},
                                                     u'500356480432754689': {u'500357905968033792': {u'500359294181580800': []}}},
                             u'500348911404728320': [],
                             u'500348984347860992': []}#,
#u'500348815061557248': {u'500351276123979776': []},
#u'500360857826889728': [],
#u'500383410766872576': {u'500384204585435136': {u'500387834562244610': {u'500388602350940160': []},
#                                              u'500388535250079744': []},
#                       u'500384274366070784': []},
#u'500385664458690560': {u'500386073865125888': {u'500387351453921283': {u'500387829005168641': [],
#                                                                     u'500408075816542208': {u'500408562779037696': {u'500409091978969088': []}}}}},
#u'500389197618761728': {u'500389896792834049': []},
#u'500391351997829120': {u'500392313076871168': []},
#u'500395670562697218': [],
#u'500395965962932224': [],
#u'500396220951842817': {u'500397848425680897': []}}