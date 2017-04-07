# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:18:19 2017

@author: Colin Drayton
"""

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import twit_auth
from pymongo import MongoClient

#Twitter API credentials fron twit_auth
#    auth = twit_auth.authentication1()
auth = twit_auth.authentication2()
#    auth = twit_auth.authentication3()

# this code needs to change for Python 3 to use the function
consumer_key = auth.consumer_key
consumer_secret = auth.consumer_secret
access_token = auth.access_token
access_token_secret = auth.access_token_secret


#MongoDB credentials and collections
DBname = 'test-database'
#DBname = 'Alta_Real'
DBhost = 'localhost'
DBport = 27017

# initiate Mongo Client
client = MongoClient()
client = MongoClient(DBhost, DBport)
db = client[DBname]



def get_all_replies(screen_name_list):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
	
    #initialize a list to hold all the tweepy Tweets
    alltweets = []	
	
    #make initial request for most recent tweets (200 is the maximum allowed count)
#    new_tweets = api.search(" to:".join(screen_name_list),count=100)
    new_tweets = api.search(" to:".join(screen_name_list),count=100)
    #save most recent tweets
    alltweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.search(" to:".join(screen_name_list),count=100,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print "...%s tweets downloaded so far" % (len(alltweets))
    # ins
        for tweet in alltweets:
            post = tweet._json
            post["_id"] = post["id"]
            trump_tweet_collection = db.replies_to_trump
            try:
                post_id = trump_tweet_collection.insert_one(post).inserted_id
            except:
                pass


if __name__ == '__main__':
    name_list = ['realDonaldTrump']
    #pass in the username of the account you want to download
    get_all_replies(name_list)