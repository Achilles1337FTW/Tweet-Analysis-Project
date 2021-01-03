import tweepy
import json
import sys
import twitter
import pandas as pd       #perhaps remove as
#from sklearn.feature_extraction.text import TfidVectorizer
from nltk.corpus import stopwords

consumer_key = 'Ay5nxj2rsTuCGrz9sFqQL5LfF'
consumer_secret = 'vAFT99kY3o4IOsHQ3VrRQuLSDw6I6GGXJEh478E13ATtGyuVrr'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

user = api.get_user('CriticalRole')
#print(user.screen_name)
#print(user.followers_count)
#print(user.id)
#for friend in user.friends():
#    print(friend.screen_name)

status = api.get_status(1334966092133888000, tweet_mode='extended')
try:
    print(status.retweeted_status.full_text)
except:                             #If not a Retweet
    print(status.full_text)

print(stopwords.words('english'))

#status = api.get_status(id, tweet_mode="extended")
#try:
#    print(status.retweeted_status.full_text)
#except AttributeError:                             # Not a Retweet
#    print(status.full_text)

