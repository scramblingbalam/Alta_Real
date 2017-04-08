# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 23:11:00 2017

@author: scram
"""
import tweepy #https://github.com/tweepy/tweepy
import twit_auth
from reply_finder import get_all_replies
from pymongo import MongoClient

#Twitter API credentials fron twit_auth
#auth1 = twit_auth.authentication1()
#auth2 = twit_auth.authentication2()
auth3 = twit_auth.authentication3()
#auth4 = twit_auth.authentication4()
#auth5 = twit_auth.authentication5()

# this code needs to change for Python 3 to use the function



#MongoDB credentials and collections
DBname = 'test-database'
#DBname = 'Alta_Real'
DBhost = 'localhost'
DBport = 27017

# initiate Mongo Client

client = MongoClient()
client = MongoClient(DBhost, DBport)
db = client[DBname]

#i = 100
i = 1
while i > 0:
    pipeline = [
      {"$group": {"_id": { "screen_name": "$user.screen_name"}, 
        "uniqueIds": { "$addToSet": "$_id" },
      }}, 
    ]


    screen_name_ID_dic = list(db.replies_to_trump.aggregate(pipeline))
    print screen_name_ID_dic[0].keys()
    
    i = get_all_replies(screen_name_ID_dic,collection,auth3,db)
    
    
    