# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:21:21 2017

@author: scram
"""
import twit_auths as twit_auth
import pprint
import tweepy
import json
from bson.son import SON
from pymongo import MongoClient
from collections import Counter

pp = pprint.PrettyPrinter(indent=0)


def get_root_drop_branches(child_collection,parent_collection,db):
    """ Inserts replies to children, deletes if no parent or if not a reply
    """
    trump_ids = list(db[parent_collection].distinct("id"))
    #no_status_error = "[{u'message': u'No status found with that ID.', u'code': 144}]"
    No_reply_deleted = 0
    No_root_deleted = 0
    root_inserted = 0
    for status_id in db[child_collection].distinct("in_reply_to_status_id"):
        if not status_id:
            del_dict = {"in_reply_to_status_id":status_id}
            dNum = db[child_collection].delete_many(del_dict).deleted_count
            No_reply_deleted += dNum
            print "Not reply deleted",dNum,"\n" 
        elif status_id not in trump_ids:
            try:
                tweet = api.get_status(str(status_id))
                post = tweet._json
                post["_id"] = post["id"]
                trump_tweet_collection = db[parent_collection]
                try:
                    post_id = trump_tweet_collection.insert_one(post).inserted_id
                    root_inserted += 1
                    print "_ID",post_id,"inserted"
                except:
                    pass
            except Exception as error:
                print "\tERROR\n",error,"\n","status_id",status_id,"\n\tERROR"
                del_dict = {"in_reply_to_status_id":status_id}
                dNum = db[child_collection].delete_many(del_dict).deleted_count
                No_root_deleted = dNum
                print "Root not found deleted",dNum,"\n"
                
    if root_inserted + No_reply_deleted + No_root_deleted > 0:
        print "CHANGES TO",db
        print "INSERTS TO", parent_collection
        print "Total parent tweets inserted", root_inserted 
        print "DELETED FROM",child_collection
        print "Total tweets deleted",No_reply_deleted + No_root_deleted
        print "\tNumber deleted because not a reply",No_reply_deleted
        print "\tNumber deleted because no root found",No_root_deleted

    
if __name__ == "__main__":
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    DB = client.Alta_Real
#    DB = client['test-database']
        
    # Get access and key from another class
    #auth = twit_auth.authentication1()
    #auth = twit_auth.authentication2()
    #auth = twit_auth.authentication3()
    auth = twit_auth.authentication4()
    #auth = twit_auth.authentication5()
    
    consumer_key = auth.consumer_key
    consumer_secret = auth.consumer_secret
    
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    
    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        
#    parent_coll_name = "trump_tweets"
#    child_coll_name = "replies_to_trump"
    
    parent_coll_name = "test_parents"
    child_coll_name = "trump_tweets"
    get_root_drop_branches(child_coll_name,parent_coll_name,DB)