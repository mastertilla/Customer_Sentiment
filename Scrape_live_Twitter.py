import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd


import json

# Specify the account credentials in the following variables:
consumer_key = '4VB2qMsbzAoN5n7CnFBlyawNF'
consumer_secret = 'a8mhO2t2ZyWnBxJpkNXPxA4FELi2l8zn5vu8WcfxsiMexfBLhY'
access_token = '274720570-BQptEbg3sNThYgaywDmfCDVmPVwKIUQGGT9pY9Ny'
access_token_secret = 'WfosewkX06ubVqQG1h1NjNBt1FRIlTV2DMdT1Y7AbnR0f'


# Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

searchwords = ['curryspcworld', 'TeamKnowhowUK']

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):

        datajson = json.loads(data)
        print(data)

        date = datajson['created_at']
        tweet = datajson['text']
        user = datajson['user']

        user_dict = {}
        for item, value in user.items():
            user_dict.update({item: value})
        username = user_dict['name']

        dataset = pd.DataFrame({'date': date, 'tweet_text': tweet, 'username': username}, index=[0])
        dataset.to_csv('Newtweets_currys.csv', sep=';', mode='a', header=False)

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, StdOutListener())

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=searchwords)

