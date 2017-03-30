# from:
# http://piratefache.ch/twitter-streaming-api-with-tweepy/
class authentication:
    def __init__(self):
        self.consumer_key = "hGqgNKnozGGUZB3IyW6Noheky"
        self.consumer_secret = "MjZAkFlsOzDdikPO5HPoNNjsa6FF7pvx99RIgGWxpSNbGRcjti"
        
        # Go to http://apps.twitter.com and create an app.
        # The consumer key and secret will be generated for you after
        # After the step above, you will be redirected to your app's page.
        # Create an access token under the the "Your access token" section
        
        self.access_token = "228503532-B6Y7fDmPVP1ppMLG57MJs8jpYfXVMycshIYj4oCc"
        self.access_token_secret = "OTZ7DtmjMqNuChSK5VDNqoqVDOXtVMQnjUTDAYwXVqAAt"
        def getconsumer_key(self):
            return self.consumer_key
        def getconsumer_secret(self):
            return self.consumer_secret
        def getaccess_token(self):
            return self.access_token
        def getaccess_token_secret(self):
            return self.access_token_secret