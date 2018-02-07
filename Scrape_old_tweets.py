import tweepy
import pandas as pd

# Specify the account credentials in the following variables:
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


# Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
dataset=[]
# Find all English tweets related to #iPhone6 since January 10 2018
for tweet in tweepy.Cursor(api.search, q={"curryspcworld -filter:retweets AND -filter:replies"}, count=100,
                           lang="en", since="2018-01-10").items():
    print("\n-----\n"+str(tweet.created_at), tweet.text+ "\n-----\n")
    dataset.append({'created_at': tweet.created_at, 'tweet': tweet.text, 'user': tweet.user.name})

oldtweets = pd.DataFrame(dataset)
oldtweets.to_csv('Oldtweets_currys.csv', sep = '|')
