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
import sys
import time

gate_out = "GATE_out_replies_to_trump_Test_Recurse.json"
gate_out = "corpus_twitIE_POS"
POS_dir ="Data\\twitIE_pos\\"

ids_around_IDless_tweets=[136,139,1085,1087]


test_tweet ={"text":"Mike Brown was staying with his grandmother for the summer, who lived in the community. #Ferguson",
"entities":{"Token":[{"indices":[0,4],"category":"NNP"},{"indices":[5,10],"category":"NNP"},{"indices":[11,14],"category":"VBD"},{"indices":[15,22],"category":"VBG"},{"indices":[23,27],"category":"IN"},{"indices":[28,31],"category":"PRP$"},{"indices":[32,43],"category":"NN"},{"indices":[44,47],"category":"IN"},{"indices":[48,51],"category":"DT"},{"indices":[52,58],"category":"NN"},{"indices":[58,59],"category":","},{"indices":[60,63],"category":"WP"},{"indices":[64,69],"category":"VBD"},{"indices":[70,72],"category":"IN"},{"indices":[73,76],"category":"DT"},{"indices":[77,86],"category":"NN"},{"indices":[86,87],"category":"."},{"indices":[88,89],"category":"HT"},{"indices":[89,97],"category":"NNP"}]},
"contributors":None,"truncated":False,
"user":{"id":24165761,"follow_request_sent":False,"profile_use_background_image":True,"default_profile_image":False,"is_translation_enabled":False,"screen_name":"MichaelSkolnik","lang":"en","profile_banner_url":"https://pbs.twimg.com/profile_banners/24165761/1406690750","listed_count":1645,"is_translator":False,"profile_link_color":"0099B9","profile_background_image_url":"http://abs.twimg.com/images/themes/theme4/bg.gif","protected":False,"time_zone":"Eastern Time (US & Canada)","profile_background_image_url_https":"https://abs.twimg.com/images/themes/theme4/bg.gif","verified":True,"profile_text_color":"3C3940","profile_image_url":"http://pbs.twimg.com/profile_images/570370729964920832/NSsz3-uv_normal.jpeg","url":"http://t.co/uYd9vD5LNN","following":False,"name":"Michael Skolnik","contributors_enabled":False,"location":"","geo_enabled":True,"profile_background_tile":False,"followers_count":133561,"profile_image_url_https":"https://pbs.twimg.com/profile_images/570370729964920832/NSsz3-uv_normal.jpeg","utc_offset":-14400,"favourites_count":19845,"profile_sidebar_fill_color":"95E8EC","id_str":"24165761","profile_sidebar_border_color":"5ED4DC","profile_background_color":"0099B9","statuses_count":28255,"friends_count":127,"default_profile":False,"description":"Political Director to Russell Simmons + Editor-In-Chief of GlobalGrind. Contact: info@mskolnik.com","notifications":False,"created_at":"Fri Mar 13 12:55:21 +0000 2009","entities":{"url":{"urls":[{"url":"http://t.co/uYd9vD5LNN","indices":[0,22],"expanded_url":"http://en.wikipedia.org/wiki/Michael_Skolnik","display_url":"en.wikipedia.org/wiki/Michael_S…"}]},"description":{"urls":[]}}},"place":None,"in_reply_to_status_id":None,"id":498280126254428160,"favorite_count":46,"source":"<a href=\"https://about.twitter.com/products/tweetdeck\" rel=\"nofollow\">TweetDeck</a>","created_at":"Sun Aug 10 01:30:14 +0000 2014","geo":None,"in_reply_to_status_id_str":None,"in_reply_to_user_id_str":None,"retweeted":False,"favorited":False,"lang":"en","retweet_count":146,"coordinates":None,"in_reply_to_screen_name":None,"id_str":"498280126254428160","in_reply_to_user_id":None}


#non_english_event =[]


def tag_tweet_zub_full(tweet,tagger=StanfordPOSTagger('gate-EN-twitter-fast.model')):
    # get indicies for words 
    if tweet.get('full_text',None):
        tokens = nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '',tweet['full_text']))
    else:
#        print(tweet['full_text'])
        tokens = nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '',tweet['text']))
    text = " ".join(tokens)
    tags = tagger.tag(tokens)
    index_tags = []
    for word,tag in tags:
        try:
            index_tags = [{'indices':[text.index(word),text.index(word)+len(word)],
                           'category':tag} for word,tag in tags]
        except:
            try:
                index_tags = [{'category':tag} for word,tag in tags]
            except:
                error_id = tweet["_id"]
                print(error_id)
                return error_id
                
    tweet['entities'].update({'Token':index_tags})
    tagged_tweet = json.dumps(tweet)+"\n"
    with open(POS_dir+tok+DBname+"_twitIE_POS_FULL_TEXT",'a')as tagFile:
        tagFile.writelines(tagged_tweet)
    return ""

def tag_tweet_twit_full(tweet,tagger=StanfordPOSTagger('gate-EN-twitter-fast.model')):
    # get indicies for words
    if tweet.get('full_text',None):
        tokens = twit_token.ize(tweet['full_text'])
    else:
        print(tweet["full_text"])
        print(tweet["text"])
        tokens = twit_token.ize(tweet['text'])
    text = " ".join(tokens)
    tags = tagger.tag(tokens)
    index_tags = []
    for word,tag in tags:
        try:
            index_tags = [{'indices':[text.index(word),text.index(word)+len(word)],
                           'category':tag} for word,tag in tags]
        except:
            try:
                index_tags = [{'category':tag} for word,tag in tags]
            except:
                error_id = tweet["_id"]
                print(error_id)
                return error_id
                
    tweet['entities'].update({'Token':index_tags})
    tagged_tweet = json.dumps(tweet)+"\n"
    with open(POS_dir+tok+DBname+"_twitIE_POS_FULL_TEXT",'a')as tagFile:
        tagFile.writelines(tagged_tweet)
    return ""


def tag_tweet_zub(tweet,tagger=StanfordPOSTagger('gate-EN-twitter-fast.model')):
    # get indicies for words 
    tokens = nltk.word_tokenize(re.sub(r'([^\s\w]|_)+', '',tweet['text']))
    text = " ".join(tokens)
    tags = tagger.tag(tokens)
    index_tags = []
    for word,tag in tags:
        try:
            index_tags = [{'indices':[text.index(word),text.index(word)+len(word)],
                           'category':tag} for word,tag in tags]
        except:
            try:
                index_tags = [{'category':tag} for word,tag in tags]
            except:
                error_id = tweet["_id"]
                print(error_id)
                return error_id
                
    tweet['entities'].update({'Token':index_tags})
    tagged_tweet = json.dumps(tweet)+"\n"
    with open(POS_dir+tok+DBname+"_twitIE_POS",'a')as tagFile:
        tagFile.writelines(tagged_tweet)
    return ""

def tag_tweet_twit(tweet,tagger=StanfordPOSTagger('gate-EN-twitter-fast.model')):
    # get indicies for words
    tokens = twit_token.ize(tweet['text'])
    text = " ".join(tokens)
    tags = tagger.tag(tokens)
    index_tags = []
    for word,tag in tags:
        try:
            index_tags = [{'indices':[text.index(word),text.index(word)+len(word)],
                           'category':tag} for word,tag in tags]
        except:
            try:
                index_tags = [{'category':tag} for word,tag in tags]
            except:
                error_id = tweet["_id"]
                print(error_id)
                return error_id
                
    tweet['entities'].update({'Token':index_tags})
    tagged_tweet = json.dumps(tweet)+"\n"
    with open(POS_dir+tok+DBname+"_twitIE_POS",'a')as tagFile:
        tagFile.writelines(tagged_tweet)
    return ""

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

    

    #MongoDB credentials and collections
#    DBname = 'test-tree'
#    DBname = 'test_recurse'
    DBname = 'Alta_Real_New'
    DBhost = 'localhost'
    DBport = 27017
    full_trunc = True
    # initiate Mongo Client
    client = MongoClient()
    client = MongoClient(DBhost, DBport)
    DB = client[DBname]
    # get ids from trump root trees
    trump_ids = list(DB.trump_tweets.distinct("_id"))
    trump_parent_ids = list(DB.edge_list.distinct("edge_list.parent",{"_id":{"$in":trump_ids}}))
    trump_child_ids = list(DB.edge_list.distinct("edge_list.child",{"_id":{"$in":trump_ids}}))
    trump_thread_ids = trump_parent_ids + trump_child_ids
    for tok in ["twit_","zub_"]:
        old_ids = []
        # open the old file and create a list with the ids 
#        if full_trunc == True:
#            with open(POS_dir+tok+DBname+"_twitIE_POS_FULL_TEXT",'r')as tagFile:
#                old_ids = [v for twt in tagFile.readlines() for k,v in json.loads(twt).items() if k=="id"]
#        else:
#            with open(POS_dir+tok+DBname+"_twitIE_POS",'r')as tagFile:
#                old_ids = [v for twt in tagFile.readlines() for k,v in json.loads(twt).items() if k=="id"]
#        
        
        stall_ids = [860631580502482944]
        stall_text = ['@realDonaldTrump 🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕🖕']

        # filter out ids for tweets that have already been saved 
        if full_trunc == False:
            start = time.time()
            mongo_tweets = list(DB.trump_tweets.find())+list(DB.replies_to_trump.find())
            mongo_tweets = list(filter(lambda x: x['id'] not in old_ids+stall_ids,mongo_tweets))
            print("NOT WRITTEN YET",len(mongo_tweets))
            mongo_tweets = list(filter(lambda x: x['id'] in trump_thread_ids,mongo_tweets))
            print("TRUMP is ROOT",len(mongo_tweets))
            end = time.time()
            print("TWEET METHOD TOOK",end-start)
    #        print(mongo_tweets[0])
    #        print(mongo_tweets[0]['_id'])
            error_list = [860480579581640710,860480579787268096,860480580730880002,
                          860480580965814274,860480581896896512,860480582274494468,
                          860480582286925827,860480582731616257,860480582891053057,
                          860480583008432128,860480583587303425,860480584010915841,
                          860480584493273088,860480584669200384,860480584811982848,
                          860480585428484097,860480585554427904,860480585629929472,
                          860480586774962182,860480586863054848]
            
            for child__id in error_list:
                print(child__id)
                print("errored_tweet in trump_child_ids",child__id in trump_child_ids)
                
    #        print("IDs_works?",set(mongo_tweets)-set(test_trump+test_replies))
            
            if tok == "twit_":
                error_tweets = list(map(tag_tweet_twit,mongo_tweets))
            elif tok == "zub_":
                error_tweets = list(map(tag_tweet_zub,mongo_tweets))
            
            with open(POS_dir+"ERROR_IDS"+tok+DBname+"_twitIE_POS",'w')as tagFile:
                tagFile.writelines(error_tweets)
        else:
            start = time.time()
            mongo_tweets = list(DB.trump_tweets.find())+list(DB.replies_to_trump.find())
            mongo_tweets = list(filter(lambda x: x['id'] not in old_ids+stall_ids,mongo_tweets))
            print("NOT WRITTEN YET",len(mongo_tweets))
            mongo_tweets = list(filter(lambda x: x['id'] in trump_thread_ids,mongo_tweets))
            print("TRUMP is ROOT",len(mongo_tweets))
            end = time.time()
            print("TWEET METHOD TOOK",end-start)
    #        print(mongo_tweets[0])
    #        print(mongo_tweets[0]['_id'])
            mongo_tweets = list(filter(lambda x: x['truncated'] == True ,mongo_tweets))
            print("Number to Run POS on FULL TEXT",len(mongo_tweets))
            error_list = [860480579581640710,860480579787268096,860480580730880002,
                          860480580965814274,860480581896896512,860480582274494468,
                          860480582286925827,860480582731616257,860480582891053057,
                          860480583008432128,860480583587303425,860480584010915841,
                          860480584493273088,860480584669200384,860480584811982848,
                          860480585428484097,860480585554427904,860480585629929472,
                          860480586774962182,860480586863054848]
            
            for child__id in error_list:
                print(child__id)
                print("errored_tweet in trump_child_ids",child__id in trump_child_ids)
                
    #        print("IDs_works?",set(mongo_tweets)-set(test_trump+test_replies))
            
            if tok == "twit_":
                error_tweets = list(map(tag_tweet_twit_full,mongo_tweets))
            elif tok == "zub_":
                error_tweets = list(map(tag_tweet_zub_full,mongo_tweets))
            
            with open(POS_dir+"ERROR_IDS"+tok+DBname+"_twitIE_POS_FULL_TEXT",'w')as tagFile:
                tagFile.writelines(error_tweets)


