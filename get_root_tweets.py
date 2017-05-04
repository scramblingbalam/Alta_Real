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


def get_root_drop_branches(root_user,child_collection,parent_collection,db):
    """ Inserts replies to children, deletes if no parent or if not a reply
    """
    in_root_but_not_root = 0
    for trump_tweet in db[parent_collection].find({}):
        if trump_tweet["in_reply_to_status_id"]:
            del_dic ={"_id":trump_tweet["_id"]}
            delnum=db[parent_collection].delete_one(del_dic).deleted_count
            in_root_but_not_root += delnum
    trump_ids = set(db[parent_collection].distinct("id"))
    child_ids = set(db[child_collection].distinct("_id"))
    #no_status_error = "[{u'message': u'No status found with that ID.', u'code': 144}]"
    No_reply_del = 0
    No_root_del = 0
    Not_root_user_del = 0
    root_inserted = 0
    Not_to_root_user_del = 0
    deleted_ids = []
    for status_id in db[child_collection].distinct("in_reply_to_status_id"):
        if not status_id:
            del_dict = {"in_reply_to_status_id":status_id}
            dNum = db[child_collection].delete_many(del_dict).deleted_count
            No_reply_del += dNum
            print "Not reply deleted",dNum,"\n"
        else:
            if status_id not in trump_ids:
                try:
                    tweet = api.get_status(str(status_id))
                    if root_user == tweet.user.screen_name:
                        in_reply_id = tweet.in_reply_to_status_id
                        if in_reply_id in child_ids:
                            post = tweet._json
                            post["_id"] = post["id"]
                            trump_tweet_collection = db[child_collection]
                        elif not in_reply_id:
                            post = tweet._json
                            post["_id"] = post["id"]
                            trump_tweet_collection = db[parent_collection]
                        try:
                            post_id = trump_tweet_collection.insert_one(post).inserted_id
                            root_inserted += 1
                            print "_ID",post_id,"inserted"
                        except:
                            pass
                    else:
                        del_dict = {"in_reply_to_status_id":status_id}
                        dbruResult = db[child_collection].delete_many(del_dict)
                        dbruNum = dbruResult.deleted_count
                        Not_to_root_user_del += dbruNum
                        print "Reply not root user deleted",dbruNum,"\n"
                        
                except Exception as error:
                    print "\tERROR\n",error,"\n","status_id",status_id,"\n\tERROR"
                    del_dict = {"in_reply_to_status_id":status_id}
                    drResult = db[child_collection].delete_many(del_dict)
                    drNum = drResult.deleted_count
                    No_root_del += drNum
                    print "Root not found deleted",drNum,"\n"
            else:
                user_list =list(db[parent_collection].find({"_id":status_id},
                     {"user.screen_name":1,"_id":0}))
                tweet_user = user_list[0]["user"]["screen_name"]
                if tweet_user != root_user:
                    del_dict = {"user.screen_name":tweet_user}
                    druResult = db[parent_collection].delete_many(del_dict)
                    druNum = druResult.deleted_count
                    Not_root_user_del += druNum
                    print "User %s not root user deleted"%tweet_user,druNum,"\n"
                
    changes = [root_inserted, No_reply_del,
               No_root_del, Not_root_user_del,
               Not_to_root_user_del,in_root_but_not_root]           
    if sum(changes) > 0:
        print "CHANGES TO",db
        print "INSERTS TO", parent_collection
        print "Total parent tweets inserted", root_inserted 
        print "DELETED FROM",child_collection
        print "Total tweets deleted",No_reply_del + No_root_del+Not_to_root_user_del
        print "\tNumber deleted because not a reply",No_reply_del
        print "\tNumber deleted because no root found",No_root_del
        print "\tNumber deleted because reply not to root_user",Not_to_root_user_del
        print "DELETED FROM",parent_collection
        print "\tNumber deleted because no root found",Not_root_user_del
        print "tNumber deleted because reply not root",in_root_but_not_root
    else:
        print "None deleted"
    print "FINISHED"

def delete_branch_is_root(child_collection,parent_collection,db):
    for i in child:
        print i

    
if __name__ == "__main__":
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    DB = client.Alta_Real
#    DB = client['test_tree']
#    DB = client['test-tree']
        
    # Get access and key from another class
    #auth = twit_auth.authentication1()
    #auth = twit_auth.authentication2()
    #auth = twit_auth.authentication3()
    auth = twit_auth.authentication4()
#    auth = twit_auth.authentication5()
    
    consumer_key = auth.consumer_key
    consumer_secret = auth.consumer_secret
    
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    
    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#    root_name = "drchuck"
    root_name = "realDonaldTrump"
#    root_name = "danklyn"
    parent_coll_name = "trump_tweets"
    child_coll_name = "replies_to_trump"
    
#    parent_coll_name = "test_parents"
#    child_coll_name = "trump_tweets"

    get_root_drop_branches(root_name,child_coll_name,parent_coll_name,DB)
    
    
    
