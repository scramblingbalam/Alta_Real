# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 14:32:23 2017

@author: scram
"""
from bson.son import SON
from pymongo import MongoClient

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



def edge_list(collections_list,DB):
    """ Takes Tweets from MongoDB and creates directed edge_lists in new collections 
    
    ARGS(list: str) Mongo collection names in the order [children, parents, ...]
    ARGS(object: pymongo.database.Database) Mongo database with the collecctions
    
    """
    #loop though the collections
    child_coll = collections_list[0]
    parent_coll = collections_list[1]
    
    edge_collection = db.edge_list
    thread_root_ids = []
    thread_child_ids = set(edge_collection.distinct("edge_list.child"))
    thread_parent_ids = set(edge_collection.distinct("edge_list.parent"))
    thread_root_ids = set(edge_collection.distinct("_id"))
    print thread_root_ids == thread_parent_ids
    for num, collection in enumerate(collections_list):
        if num == 0:
            print collection
            for tweet in DB[collection].find():
                if tweet["in_reply_to_status_id"]:
                    if tweet["in_reply_to_status_id"] in thread_child_ids:  
                        edge_collection.update_one(
                                {"edge_list.child":tweet["in_reply_to_status_id"]},
                                {"$push": {"edge_list":
                                    {"parent":tweet["in_reply_to_status_id"],
                                     "child":tweet["id"]}
                                    }
                                })
                        thread_child_ids.add(tweet["id"])
                        thread_parent_ids.add(tweet["in_reply_to_status_id"])
                    elif tweet["in_reply_to_status_id"] not in thread_root_ids:
                        post = {"_id": tweet["in_reply_to_status_id"],
                            "edge_list": [
                                {"parent":tweet["in_reply_to_status_id"],
                                "child":tweet["id"]}
                                ]}
                        post_id = edge_collection.insert_one(post).inserted_id
                        print post_id,"<--",tweet["id"]
                        print test_dict[post_id],"<--",test_dict[tweet["id"]],"\n"
                        thread_root_ids.add(post_id)
                        thread_child_ids.add(tweet["id"])
                        thread_parent_ids.add(tweet["in_reply_to_status_id"])
#                        thread_root_ids = edge_collection.distinct("_id")
                    elif tweet["id"] not in thread_child_ids:  
                        print test_dict[tweet["id"]],"ELSE\n"
                        edge_collection.update_one(
                                {"_id":tweet["in_reply_to_status_id"]},
                                {"$push": {"edge_list":
                                    {"parent":tweet["in_reply_to_status_id"],
                                     "child":tweet["id"]}
                                    }
                                })
                        thread_child_ids.add(tweet["id"])
                        thread_parent_ids.add(tweet["in_reply_to_status_id"])
        else:
            # Decide if you want to do anything to with this to support different
            # strage approches....
            threads = 0
            print collection
            print "\t",collections_list[num-1]
            children = collections_list[num-1]
            child_ids = DB[children].distinct("id")
            for tweet in DB[collection].find():
                if tweet["in_reply_to_status_id"]:
                    if tweet["id"] in child_ids:
                        threads += 1
            print "threads", threads
            
if __name__ == "__main__":
    client = MongoClient()
    client = MongoClient('localhost', 27017)
#    db = client.Alta_Real
#    db = client["test-database"]
    db = client.test_tree
    collection_names = ["replies_to_trump","trump_tweets","test_parents"]
    collection_names = ["replies_to_trump","trump_tweets"]
#    for i in collection_names:
#        print db[i].distinct("id")
    edge_list(collection_names,db)
    edge_collection = db.edge_list
    print edge_collection.find_one()
