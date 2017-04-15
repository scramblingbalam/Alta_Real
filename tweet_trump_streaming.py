import tweepy
import socket
import requests
import time
import twit_auths as twit_auth#import authentication  # Consumer and access token/key
import datetime
import pymongo
import pprint
from pymongo import MongoClient
# original code from 
# http://piratefache.ch/twitter-streaming-api-with-tweepy/
my_id = 228503532
Kat_id = 1335150097
Trump_id = 25073877
fin_test = 99097480
dan_klyn = 10089542
user_id = Trump_id

class TwitterStreamListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_status(self, status):
        get_trump_tweet(status)
        get_reply_tweet(status)
#        get_user_informations(status)

    # Twitter error list : https://dev.twitter.com/overview/api/response-codes

    def on_error(self, status_code):
        if status_code == 403:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False


def get_trump_tweet(tweet):
#    print "\t",tweet.user.name
#    print tweet.text
    
    if tweet.user.id == user_id and tweet.in_reply_to_user_id == None:
        post = tweet._json
        post["_id"] = post["id"]
        trump_tweet_collection = db.trump_tweets
        try:
            post_id = trump_tweet_collection.insert_one(post).inserted_id
            print "TRUMP_TWEET\n\tINSERT _ID",post_id
            print "\t",post["text"]

        except:
            pass
#        pprint.pprint(posts.find_one())



def get_reply_tweet(tweet):
    # Display sender and mentions user
    if tweet.in_reply_to_user_id == user_id :
        post = tweet._json
        post["_id"] = post["id"]
        replies_to_trump_collection = db.replies_to_trump
        try:
            post_id = replies_to_trump_collection.insert_one(post).inserted_id
#            print "REPLY 2 REAL_DONALD_TRUMP\n\tINSERT _ID",post_id
        except:
            pass
#        pprint.pprint(posts.find_one())


if __name__ == '__main__':
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.Alta_Real
#    db = client['test-database']
    
    # Get access and key from another class
    auth = twit_auth.authentication1()
#    auth = twit_auth.authentication2()
#    auth = twit_auth.authentication3()
#    auth = twit_auth.authentication4()
#    auth = twit_auth.authentication5()

    consumer_key = auth.consumer_key
    consumer_secret = auth.consumer_secret

    access_token = auth.access_token
    access_token_secret = auth.access_token_secret

    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

    streamListener = TwitterStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
    trump_str = "realDonaldTrump"
    kat_str = "Katalogofchaos"
    fin_test ="IronViolin"
    dan_klyn = "danklyn"
    filter_string = trump_str
#    myStream.filter(track=[filter_string], async=True)
    myStream.filter(follow=[str(user_id)], async=True)