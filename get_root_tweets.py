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

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.Alta_Real
#db = client['test-database']
    
    # Get access and key from another class
#auth = twit_auth.authentication1()
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

trump_tweet_id = 848219027659010051
Trump_id = 25073877
error =[]
trump_ids = list(db.trump_tweets.distinct("id"))
non_existant_tweet =850184336318103554 

print db.replies_to_trump.distinct("in_reply_to_status_id")

no_status_error = "[{u'message': u'No status found with that ID.', u'code': 144}]"
for status_id in db.replies_to_trump.distinct("in_reply_to_status_id"):
    if not status_id:
        print db.replies_to_trump.remove({"in_reply_to_status_id":status_id})  
    elif status_id not in trump_ids:
        try:
            tweet = api.get_status(str(status_id))
            post = tweet._json
            post["_id"] = post["id"]
            trump_tweet_collection = db.trump_tweets
            try:
                post_id = trump_tweet_collection.insert_one(post).inserted_id
            except:
                pass
        except Exception as error:
            print "\tERROR\n",error,"\n",status_id,"\n\tERROR"
            removed_ids =[i["_id"] for i in db.replies_to_trump.find({"in_reply_to_status_id":status_id})]
            print db.replies_to_trump.remove({"in_reply_to_status_id":status_id}) 
            for rm_id in removed_ids:
                print "Documnet removed",rm_id
            
            

#print len(db.replies_to_trump.distinct("in_reply_to_status_id"))
# Code below can be used to print counts of replies
pipeline = [
     {"$unwind": "$in_reply_to_status_id"},
     {"$group": {"_id": "$in_reply_to_status_id", "count": {"$sum": 1}}},
     {"$sort": SON([("count", -1), ("_id", -1)])}
 ]

# pp.pprint(list(db.replies_to_trump.aggregate(pipeline)))
# print Counter([type(i) for i in db.replies_to_trump.distinct("in_reply_to_status_id")])

