# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:40:47 2017

@author: scram
"""
import twit_auths as twit_auth
import pprint
import tweepy
import json
from bson.son import SON
from pymongo import MongoClient
from pymongo import errors as mongo_errors
from collections import Counter



def mongo_tweet_up(id_tweet,db,auth):
    reply_db = db.replies_to_trump
    root_db = db.trump_tweets
    consumer_key = auth.consumer_key
    consumer_secret = auth.consumer_secret
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True,
                 retry_count = 10,
                 retry_errors=10054,
                 retry_delay=5)
    tweet = api.get_status(id_tweet)
    tweet_json = tweet._json
#    print tweet_json['text']
    tweet_json.update({"_id":tweet._json["id"]})

    if not tweet_json["in_reply_to_status_id"]:
        try:
            post_id=root_db.insert_one(tweet_json).inserted_id
            return post_id
        except:
            return tweet_json["_id"]

    else:
        try:
            post_id=reply_db.insert_one(tweet_json).inserted_id
            return mongo_tweet_up(tweet_json["in_reply_to_status_id"],db,auth)
        except:
            return mongo_tweet_up(tweet_json["in_reply_to_status_id"],db,auth)



def post_tweets(tweets,id_list, collection):
    post_ids = []
    reply_name_id_d = {}
    errors = []
    not_post_ids =[]
    for tweet in tweets:
        if tweet.in_reply_to_status_id in id_list:
            tweet_json = tweet._json
            tweet_json.update({"_id":tweet._json["id"]})
            s_id = tweet.id
            follow_count = tweet.user.followers_count
            name = tweet.user.screen_name
            if tweet.user.screen_name not in reply_name_id_d:
                reply_name_id_d[name] = (follow_count,[s_id])
            else:
                if reply_name_id_d[name][0]<follow_count:
                    reply_name_id_d[name][0] = [follow_count]
                reply_name_id_d[name][1].append(s_id)
#            print tweet.user.screen_name,"--",tweet_json["text"]
            try:
                post_id=collection.insert_one(tweet_json).inserted_id
                post_ids.append(post_id)
            except Exception as err:
                errors.append(err.code)
                post_ids.append(s_id)
                if err.code != 11000:
                    print err

    return reply_name_id_d,post_ids,errors

def print_results(num,posts,errors):
    if posts:
        if errors:
            posted = len(posts) - sum(v for k,v in Counter(errors).items() if k !=11000)
        else:
            posted = len(posts)
        print "\t%s/%s"%(posted,num),"in Mongo/downloaded, oldest post ==",posts[0]
    if errors:
        print "\tPost Errors"
        for k,v in Counter(errors).items():
            print "\t\t",k,v 


def mongo_tweet_down(name_id_dic,db,auth,oldest):
    ### SETUP
    reply_db = db.replies_to_trump_down
    consumer_key = auth.consumer_key
    consumer_secret = auth.consumer_secret
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True,
                 retry_count = 10,
                 retry_errors=10054,
                 retry_delay=5) 
    reply_name_id_dic ={}
    posted_ids = []
    errors = []
    i = 0
    ### Main logic
    sorted_dic = sorted(name_id_dic.items(),key=lambda (k,v):(-v[0],k))
    for screen_name,tweet_id_list in sorted_dic:
        tweet_id_list = tweet_id_list[1]
        new_tweets = api.search("to:"+screen_name,count=100,since_id=oldest)
        i += len(new_tweets)
        tup_out =post_tweets(new_tweets,tweet_id_list, reply_db)
        reply_dict,posted,errs = tup_out
        reply_name_id_dic.update(reply_dict)
        posted_ids += posted
        errors += errs
        if new_tweets:
            user_oldest = new_tweets[-1].id - 1
        while len(new_tweets) > 0:
            new_tweets = api.search("to:"+screen_name,count=100,max_id=user_oldest,since_id=oldest,)
            i += len(new_tweets)
            tup_out =post_tweets(new_tweets,tweet_id_list, reply_db)
            reply_dict,posted,errs = tup_out
            reply_name_id_dic.update(reply_dict)
            posted_ids += posted
            errors += errs
            if new_tweets:
                user_oldest = new_tweets[-1].id - 1
        print "Finished tweets @", screen_name
        print_results(i,posted_ids,errors)
    if reply_name_id_dic:
        reply_oldest = min(posted_ids)
        return posted_ids + mongo_tweet_down(reply_name_id_dic,db,auth,reply_oldest)
    else:
        return posted_ids
    

if __name__ == '__main__':
    #pass in the username of the account you want to download
    #Twitter API credentials fron twit_auth
#    Auth = twit_auth.authentication1()
#    Auth = twit_auth.authentication2()
#    Auth = twit_auth.authentication3()
    Auth = twit_auth.authentication4()
#    Auth = twit_auth.authentication5()

    # this code needs to change for Python 3 to use the function

    
    
    #MongoDB credentials and collections
#    DBname = 'test-tree'
#    DBname = 'test_recurse'
    DBname = 'test_tree'
    DBhost = 'localhost'
    DBport = 27017
    
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB = client[DBname]

    
    print "_______________________"
    test_ids_all = [861390012235083777,
                    861404636099608576,
                    861544451587682304,
                    861544819444862976,
                    861544990509608960,
                    861547334093688835,
                    861555537179279360,
                    861558323509948416,
                    861553761008963586,
                    861558523594932229,
                    861996266322104321,
                    861377007594221568,
                    861380349359779841]
    pipeline = [
      {"$group": 
          {"_id": "$user.screen_name",
            "follow_num":{"$max":"$user.followers_count"},
            "uniqueIds": { "$addToSet": "$_id" },
      }}, 
    ]
        
#    root_name = "drchuck"
    root_name = "danklyn"
#    root_name = "realDonaldTrump"
    screen_name_ID_dic = []
    ### Enable below code to get replies from to root_user/Trump
    screen_name_ID_dic = list(DB.trump_tweets.aggregate(pipeline))
    ### Enable below code to get second order replies
#    screen_name_ID_dic = list(DB.replies_to_trump.aggregate(pipeline))

    if not screen_name_ID_dic:
        name_id_dict = [root_name]
    else:
        name_id_dict = {i["_id"]:(i["follow_num"],i["uniqueIds"]) for i in screen_name_ID_dic}
        
    pipeline_oldest =[{"$group":
                {"_id":"$in_reply_to_screen_name",
                "oldest":{"$min":"$id"},
                "newest":{"$max":"$id"},
                "count": {"$sum":1}
                }    
            }]
    oldest_id =list(DB.trump_tweets.aggregate(pipeline_oldest))[0]["oldest"]
    all_out = mongo_tweet_down(name_id_dict,DB,Auth,oldest_id)
    print all_out
    
    
    
    
    
    
    
    
    
    