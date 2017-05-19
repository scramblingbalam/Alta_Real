# -*- coding: utf-8 -*-
"""
Created on Thu May 18 19:03:37 2017

@author: scram
"""
import twit_auths as twit_auth 
from nltk.tag import StanfordPOSTagger
from pymongo import MongoClient
import feature_functions as feature
import json
from copy import deepcopy
import twit_token
import nltk
import re


gate_out = "GATE_out_replies_to_trump_Test_Recurse.json"
gate_out = "corpus_twitIE_POS"
POS_dir ="Data\\twitIE_pos\\"

ids_around_IDless_tweets=[136,139,1085,1087]


test_tweet ={"text":"Mike Brown was staying with his grandmother for the summer, who lived in the community. #Ferguson",
"entities":{"Token":[{"indices":[0,4],"category":"NNP"},{"indices":[5,10],"category":"NNP"},{"indices":[11,14],"category":"VBD"},{"indices":[15,22],"category":"VBG"},{"indices":[23,27],"category":"IN"},{"indices":[28,31],"category":"PRP$"},{"indices":[32,43],"category":"NN"},{"indices":[44,47],"category":"IN"},{"indices":[48,51],"category":"DT"},{"indices":[52,58],"category":"NN"},{"indices":[58,59],"category":","},{"indices":[60,63],"category":"WP"},{"indices":[64,69],"category":"VBD"},{"indices":[70,72],"category":"IN"},{"indices":[73,76],"category":"DT"},{"indices":[77,86],"category":"NN"},{"indices":[86,87],"category":"."},{"indices":[88,89],"category":"HT"},{"indices":[89,97],"category":"NNP"}]},
"contributors":None,"truncated":False,
"user":{"id":24165761,"follow_request_sent":False,"profile_use_background_image":True,"default_profile_image":False,"is_translation_enabled":False,"screen_name":"MichaelSkolnik","lang":"en","profile_banner_url":"https://pbs.twimg.com/profile_banners/24165761/1406690750","listed_count":1645,"is_translator":False,"profile_link_color":"0099B9","profile_background_image_url":"http://abs.twimg.com/images/themes/theme4/bg.gif","protected":False,"time_zone":"Eastern Time (US & Canada)","profile_background_image_url_https":"https://abs.twimg.com/images/themes/theme4/bg.gif","verified":True,"profile_text_color":"3C3940","profile_image_url":"http://pbs.twimg.com/profile_images/570370729964920832/NSsz3-uv_normal.jpeg","url":"http://t.co/uYd9vD5LNN","following":False,"name":"Michael Skolnik","contributors_enabled":False,"location":"","geo_enabled":True,"profile_background_tile":False,"followers_count":133561,"profile_image_url_https":"https://pbs.twimg.com/profile_images/570370729964920832/NSsz3-uv_normal.jpeg","utc_offset":-14400,"favourites_count":19845,"profile_sidebar_fill_color":"95E8EC","id_str":"24165761","profile_sidebar_border_color":"5ED4DC","profile_background_color":"0099B9","statuses_count":28255,"friends_count":127,"default_profile":False,"description":"Political Director to Russell Simmons + Editor-In-Chief of GlobalGrind. Contact: info@mskolnik.com","notifications":False,"created_at":"Fri Mar 13 12:55:21 +0000 2009","entities":{"url":{"urls":[{"url":"http://t.co/uYd9vD5LNN","indices":[0,22],"expanded_url":"http://en.wikipedia.org/wiki/Michael_Skolnik","display_url":"en.wikipedia.org/wiki/Michael_S…"}]},"description":{"urls":[]}}},"place":None,"in_reply_to_status_id":None,"id":498280126254428160,"favorite_count":46,"source":"<a href=\"https://about.twitter.com/products/tweetdeck\" rel=\"nofollow\">TweetDeck</a>","created_at":"Sun Aug 10 01:30:14 +0000 2014","geo":None,"in_reply_to_status_id_str":None,"in_reply_to_user_id_str":None,"retweeted":False,"favorited":False,"lang":"en","retweet_count":146,"coordinates":None,"in_reply_to_screen_name":None,"id_str":"498280126254428160","in_reply_to_user_id":None}


#non_english_event =[]

pos_file_path =POS_dir+gate_out
#id_pos_dic, index_pos_dic = feature.pos_extract(pos_file_path)

if __name__ == '__main__':
    #pass in the username of the account you want to download
    #Twitter API credentials fron twit_auth
#    Auth = twit_auth.authentication1()
#    Auth = twit_auth.authentication2()
#    Auth = twit_auth.authentication3()
#    Auth = twit_auth.authentication4()
    Auth = twit_auth.authentication5()

    # this code needs to change for Python 3 to use the function

    
    def tag_tweet(tweet,tagger=StanfordPOSTagger('gate-EN-twitter.model')):
        tags = tagger.tag(tweet['text'].split())
        # get indicies for words 
#        text 
#        index_tags = [{'indices':[],'category':tag} for word,tag in tags]
        tweet['entities'].update({'Token':tags})
        return tweet
    #MongoDB credentials and collections
#    DBname = 'test-tree'
#    DBname = 'test_recurse'
    DBname = 'Alta_Real_New'
    DBhost = 'localhost'
    DBport = 27017
    
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB = client[DBname]
    test_mongo = DB.trump_tweets.find().limit(3)
#    tagged_tweets = map(tag_tweet,test_mongo)
    test_tweetC = deepcopy(test_tweet)
    tagged_tweets = map(tag_tweet,[test_tweetC])
    for twt in tagged_tweets:
        i = twt['entities']
        print(i)
        print(test_tweet['entities'])
        print(twt['text'])
        print(twt['text'][89:97])
        print("\n")
#    outT = twitIE.tag('What is the airspeed of an unladen swallow ?'.split())



