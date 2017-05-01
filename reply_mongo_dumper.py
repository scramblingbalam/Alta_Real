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
from collections import Counter


def get_all_replies(screen_name_id_dict,db):
	#Twitter only allows access to a users most recent 3240 tweets with this method
    if isinstance(screen_name_id_dict,dict):
        screen_name_list = screen_name_id_dict.keys()
        tweet_id_list = screen_name_id_dict.values()[0]
    elif isinstance(screen_name_id_dict,list):
        screen_name_list = screen_name_id_dict
        tweet_id_list = None
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
    errors = []
    #save the id of the oldest tweet less one
    collection = db.replies_to_trump
    for tweet in new_tweets:
        post = tweet._json
        post["_id"] = post["id"]
        if post['in_reply_to_status_id']:
            if tweet_id_list:
                if post['in_reply_to_status_id'] in tweet_id_list:
                    try:
                        post_id = collection.insert_one(post).inserted_id
                        posted +=1
                    except Exception as err1:
                        errors.append(err1.code)
                        pass
            else:
                if post['in_reply_to_screen_name'] in screen_name_list:
                    try:
                        post_id = collection.insert_one(post).inserted_id
                        posted +=1
                    except Exception as err2:
                        errors.append(err2.code)
                        pass
    if new_tweets:
        oldest = new_tweets[-1].id - 1
        print "...%s tweets downloaded so far" % (i)
        print "\t%s/%s"%(posted,i),"posted/downloaded"
        print "Post Errors"
        for k,v in Counter(errors).items():
            print "\t",k,v
    else:
        print "No more tweets for users:",", ".join(screen_name_list)
        
        
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
            if post['in_reply_to_status_id']:
                if tweet_id_list:
                    if post['in_reply_to_status_id'] in tweet_id_list:
                        try:
                            post_id = collection.insert_one(post).inserted_id
                            posted +=1
                        except Exception as err3:
                            errors.append(err3.code)
                            pass
                else:
                    if post['in_reply_to_screen_name'] in screen_name_list:
                        try:
                            post_id = collection.insert_one(post).inserted_id
                            posted +=1
                        except Exception as err4:
                            errors.append(err4.code)
                            pass
                        
        if new_tweets:
            oldest = new_tweets[-1].id - 1
            print "...%s tweets downloaded so far" % (i)
            print "\t%s/%s"%(posted,i),"posted/downloaded"
            if errors:
                print "Post Errors"
                for k,v in Counter(errors).items():
                    print "\t",k,v
        else:
            print "No more tweets for users:",", ".join(screen_name_list)


if __name__ == '__main__':
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
    DBname = 'test-tree-new'
    #DBname = 'Alta_Real'
    DBname = 'test-tree'
    DBhost = 'localhost'
    DBport = 27017
    
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB = client[DBname]
#    pipeline = [
#      {"$group": {"_id": { "screen_name": "$user.screen_name"}, 
#        "uniqueIds": { "$addToSet": "$_id" },
#      }}, 
#    ]
    pipeline = [
      {"$group": {"_id": "$user.screen_name", 
        "uniqueIds": { "$addToSet": "$_id" },
      }}, 
    ]
    root_name = "drchuck"
#    root_name = "realDonaldTrump"
    screen_name_ID_dic = []
    screen_name_ID_dic = list(DB.replies_to_trump.aggregate(pipeline))
    screen_name_ID_dic = []
    screen_name_ID_dic = list(DB.trump_tweets.aggregate(pipeline))
    if not screen_name_ID_dic:
        name_id_dic = [root_name]
    else:
        name_id_dic = {i["_id"]:i["uniqueIds"] for i in screen_name_ID_dic}
    get_all_replies(name_id_dic,DB)