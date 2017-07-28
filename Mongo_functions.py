# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 14:32:23 2017

@author: scram
"""
from bson.son import SON
from pymongo import MongoClient
import networkx as nx
import bson

test_dict ={
851588099360649216: "root_tweet",
851588741055623169: "top_reply_1",
851613881520803840: "reply_1_1",
851757634613018625: "reply_1_2",
851759076577079296: "reply_1_2_1",
851595539565105152: "top_reply_2",
851596235949658112: "reply_2_1",
851782925981028353: "reply_2_1_1",
851935916725764097: "reply_2_1_2",
851595212468084736: "top_reply_3"
 }

def get_tweet_time(TWEET):
    strfts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(TWEET['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
    ts = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.mktime(time.strptime(TWEET['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))) )
    return ts,strfts

def id2edgelist(mongo_id,collection):
    list_dicts = list(collection.find({"_id":mongo_id}))[0]
    edges = []
    for i in list_dicts['edge_list']:
        edges.append((i['parent'],i['child']))
    return edges

def edge_list(collections_list,DB):
    """ Takes Tweets from MongoDB and creates directed edge_lists in new collections 
    
    ARGS(list: str) Mongo collection names in the order [children, parents, ...]
    ARGS(object: pymongo.database.Database) Mongo database with the collecctions
    
    """
    #loop though the collections
    child_coll = collections_list[0]
    parent_coll = collections_list[1]
    
    edge_coll = db.edge_list
    root_ids = []
    child_ids = set(edge_coll.distinct("edge_list.child"))
    parent_ids = set(edge_coll.distinct("edge_list.parent"))
    root_ids = set(edge_coll.distinct("_id"))
    
    print(root_ids == parent_ids)
    for num, collection in enumerate(collections_list):
        if num == 0:
            print(collection)
            for tweet in DB[collection].find({}).sort("_id",1):
                edge = [tweet["in_reply_to_status_id"],tweet["id"]]
                if edge[1] not in child_ids:
                    if edge[0]:
                        if edge[0] in child_ids:
                            edge_coll.update_one(
                                    {"edge_list.child":edge[0]},
                                    {"$push": {"edge_list":
                                        {"parent":edge[0],
                                         "child":edge[1]}
                                        }
                                    })
                            child_ids.add(edge[1])
                            parent_ids.add(edge[0])
                            at_root = list(edge_coll.find({"edge_list.child":edge[0]}))[0]["_id"]
                            print( at_root,"^--",edge[0],"<--",edge[1])
                            if edge[1] in root_ids:
                                subThread =list(edge_coll.find({"_id":edge[1]}))
                                for edg in subThread[0]["edge_list"]:
                                    edge_coll.update_one(
                                        {"edge_list.child":edge[0]},
                                        {"$push": {"edge_list":
                                            edg
                                            }
                                        })
                                edge_coll.delete_one({"_id":edge[1]})                
                        elif edge[0] not in root_ids:
                            if db[parent_coll].find({'_id':edge[0]}):
                                post = {"_id": edge[0],
                                    "edge_list": [
                                        {"parent":edge[0],
                                        "child":edge[1]}
                                        ]}
                                post_id = edge_coll.insert_one(post).inserted_id
                                print( "^",post_id,"<--",edge[1])
                                root_ids.add(post_id)
                                child_ids.add(edge[1])
                                parent_ids.add(edge[0])
                            else:
                                db[child_coll].delete_one({'_id':tweet['id']})
                                
                        elif edge[1] not in child_ids:
                            edge_coll.update_one(
                                    {"_id":edge[0]},
                                    {"$push": {"edge_list":
                                        {"parent":edge[0],
                                         "child":edge[1]}
                                        }
                                    })
                            child_ids.add(edge[1])
                            parent_ids.add(edge[0])
                            print( edge[0],"^--",edge[1])
            print( "Finished first collection")
        else:
            # Decide if you want to do anything to with this to support different
            # strage approches....
            threads = 0
            print( collection)
            print( "\t",collections_list[num-1])
            children = (collections_list[num-1])
            child_ids = DB[children].distinct("id")
#            for tweet in DB[collection].find():
#                if edge[0]:
#                    if edge[1] in child_ids:
#                        threads += 1
            print( "threads", threads)



def remove_old_threads(DB,id_date):
    test =856172056932700164
#    for thread in list(DB.edge_list.find({"_id":test}))[:10]:
    del_replies = 0 
    del_roots = 0
    del_threads = 0
    for thread in list(DB.edge_list.find({}))[:100]:
        thread_old = []
        id_set = set()
        if thread['_id'] < id_date:
            for edge in thread['edge_list']:
                id_set.add(edge['parent'])
                id_set.add(edge['child'])
            del_roots +=1
            id_list = list(id_set - set([thread['_id']]))
            del_replies += len(id_list)
            DB.trump_tweets.delete_one({'_id':thread['_id']})
            del_dic ={'_id':{'$in':list(id_set)}}
            DB.replies_to_trump.delete_many(del_dic)
            DB.edge_list.delete_one({'_id':thread['_id']})
            del_threads +=1
        else:
            for edge in thread['edge_list']:
                id_set.add(edge['parent'])
                id_set.add(edge['child'])
                thread_old.append(edge['child'] < id_date)
                thread_old.append(edge['parent'] < id_date)
            if any(thread_old):
                del_roots +=1
                id_list = list(id_set - set([thread['_id']]))
                del_replies += len(id_list)
                DB.trump_tweets.delete_one({'_id':thread['_id']})
                del_dic ={'_id':{'$in':list(id_set)}}
                DB.replies_to_trump.delete_many(del_dic)
                DB.edge_list.delete_one({'_id':thread['_id']})
                del_threads +=1
        
    changes = [del_replies,del_roots,del_threads]
    if sum(changes)>0:
        print( 'Number deleted from "replies_to_tweets"',del_replies)
        print( 'Number deleted from "trump_tweets"',del_roots)
        print( 'Number deleted from "edge_list"',del_threads)
    else:
        print( "None deleted")
    print("FINISHED")
    
            
if __name__ == "__main__":
    client = MongoClient()
    client = MongoClient('localhost', 27017)
#    db = client.Alta_Real
    db = client.Alta_Real_New

#    db = client["test-tree"]
#    db = client.test_tree
    collection_names = ["replies_to_trump","trump_tweets"]

#    """
    edge_list(collection_names,db)
    edge_collection = db.edge_list
    big_thread = list(edge_collection.aggregate( [{ "$unwind" : "$edge_list" },
            { "$group" : { "_id" : "$_id", "len" : { "$sum" : 1 } } },
            { "$sort" : { "len" : 1 } },
            { "$limit" : 1 }
            ] ))
#    print list(big_thread)
    print( len(big_thread) )
    biggest_id =  big_thread[0]["_id"]
    print( biggest_id)
    DG=nx.DiGraph()
    DG.add_edges_from(id2edgelist(biggest_id,edge_collection))
    nx.draw_random(DG, with_labels=False)
    nx.draw_random(DG, with_labels=True)
#    """
    pipeline_oldest =[{"$group":
                {"_id":"$in_reply_to_screen_name",
                "oldest":{"$min":"$id"},
                "newest":{"$max":"$id"},
                "count": {"$sum":1}
                }    
            }]

#    oldest_time = list(db.replies_to_trump.find({"_id":old_id}))[0]["created_at"]
    oldest_id =list(db.replies_to_trump.aggregate(pipeline_oldest))[0]["oldest"]
    remove_old_threads(db,oldest_id)
#    remove_old_threads(db,oldest_time)
    
    