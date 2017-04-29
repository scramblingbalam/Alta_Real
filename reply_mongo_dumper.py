# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:18:19 2017

@author: Colin Drayton
"""

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import twit_auths as twit_auth
from pymongo import MongoClient



def get_all_replies(screen_name_list,db):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
    #initialize a list to hold all the tweepy Tweets
	
    #make initial request for most recent tweets (200 is the maximum allowed count)
#    new_tweets = api.search(" to:".join(screen_name_list),count=100)
    new_tweets = api.search(" to:".join(screen_name_list),count=100)
    #save most recent tweets
    i = len(new_tweets)
    posted = 0
    #save the id of the oldest tweet less one
    
    for tweet in new_tweets:
        post = tweet._json
        post["_id"] = post["id"]
        trump_tweet_collection = db.replies_to_trump
        if post['in_reply_to_status_id']:
            try:
                post_id = trump_tweet_collection.insert_one(post).inserted_id
                posted +=1
            except:
                pass
    if new_tweets:
        oldest = new_tweets[-1].id - 1
        print "...%s tweets downloaded so far" % (i)
        print "\t%s/%s"%(posted,i),"posted/downloaded"
    else:
        print "No more tweets"   
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
#        print "getting tweets before %s" % (oldest)
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.search(" to:".join(screen_name_list),count=100,max_id=oldest)
        i += len(new_tweets)
        #update the id of the oldest tweet less one

    # ins
        for tweet in new_tweets:
            post = tweet._json
            post["_id"] = post["id"]
            trump_tweet_collection = db.replies_to_trump
            if post['in_reply_to_status_id']:
                try:
                    post_id = trump_tweet_collection.insert_one(post).inserted_id
                    posted +=1
                except:
                    pass
        if new_tweets:
            oldest = new_tweets[-1].id - 1
            print "...%s tweets downloaded so far" % (i)
            print "\t%s/%s"%(posted,i),"posted/downloaded"
        else:
            print "No more tweets for users:",", ".join(name_list)

if __name__ == '__main__':
    name_list = ['drchuck']
    #pass in the username of the account you want to download
    #Twitter API credentials fron twit_auth
#    auth = twit_auth.authentication1()
#    auth = twit_auth.authentication2()
#    auth = twit_auth.authentication3()
    auth = twit_auth.authentication4()
#    auth = twit_auth.authentication5()

    # this code needs to change for Python 3 to use the function
    consumer_key = auth.consumer_key
    consumer_secret = auth.consumer_secret
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    
    
    #MongoDB credentials and collections
    DBname = 'test-tree'
    #DBname = 'Alta_Real'
    DBhost = 'localhost'
    DBport = 27017
    
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB = client[DBname]
    get_all_replies(name_list,DB)