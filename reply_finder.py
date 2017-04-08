# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:18:19 2017

@author: Colin Drayton
"""

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import twit_auth
from pymongo import MongoClient

#Twitter API credentials fron twit_auth
auth1 = twit_auth.authentication1()
auth2 = twit_auth.authentication2()
auth3 = twit_auth.authentication3()
auth4 = twit_auth.authentication4()
auth5 = twit_auth.authentication5()

# this code needs to change for Python 3 to use the function



#MongoDB credentials and collections
DBname = 'test-database'
#DBname = 'Alta_Real'
DBhost = 'localhost'
DBport = 27017

# initiate Mongo Client
client = MongoClient()
client = MongoClient(DBhost, DBport)
DB = client[DBname]



def get_all_replies(screen_name_ids,collection,app_auth,db):
    consumer_key = app_auth.consumer_key
    consumer_secret = app_auth.consumer_secret
    access_token = app_auth.access_token
    access_token_secret = app_auth.access_token_secret
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
	
	
    #make initial request for most recent tweets (200 is the maximum allowed count)
#    new_tweets = api.search(" to:".join(screen_name_list),count=100)
    new_tweets = api.search(" to:".join(screen_name),count=100)
    #save most recent tweets
    i = len(new_tweets)
    #save the id of the oldest tweet less one
    oldest = new_tweets[-1].id - 1
    for tweet in new_tweets:
        post = tweet._json
        post["_id"] = post["id"]
        trump_tweet_collection = db[collection]
        try:
            post_id = trump_tweet_collection.insert_one(post).inserted_id
        except:
            pass
                       
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.search(" to:".join(screen_name),count=100,max_id=oldest)

        i += len(new_tweets)
        #update the id of the oldest tweet less one
        oldest = new_tweets[-1].id - 1
        print "...%s tweets downloaded so far" % (i)
    # ins
        for tweet in new_tweets:
            post = tweet._json
            post["_id"] = post["id"]
            trump_tweet_collection = db[collection]
            try:
                post_id = trump_tweet_collection.insert_one(post).inserted_id
            except:
                pass
#        yield new_tweets
    return i

if __name__ == '__main__':
    name_list = ['realDonaldTrump']
    #pass in the username of the account you want to download
    get_all_replies(name_list,"replies_to_trump",auth2,DB)