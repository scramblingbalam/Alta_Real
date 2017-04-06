# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:21:21 2017

@author: scram
"""
import twit_auth
import pprint
import tweepy
import json
from bson.son import SON
from pymongo import MongoClient

pp = pprint.PrettyPrinter(indent=0)

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.Alta_Real
#db = client['test-database']
    
    # Get access and key from another class
#    auth = twit_auth.authentication1()
auth = twit_auth.authentication2()
#    auth = twit_auth.authentication3()
#    auth.
consumer_key = auth.consumer_key
consumer_secret = auth.consumer_secret

access_token = auth.access_token
access_token_secret = auth.access_token_secret

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

trump_tweet_id = 848219027659010051
Trump_id = 25073877
for status_id in db.replies_to_trump.distinct("in_reply_to_status_id"):
    if status_id:
        tweet = api.get_status(str(status_id))
        post = tweet._json
        post["_id"] = post["id"]
        trump_tweet_collection = db.trump_tweets
        try:
            post_id = trump_tweet_collection.insert_one(post).inserted_id
        except:
            pass
#print len(db.replies_to_trump.distinct("in_reply_to_status_id"))