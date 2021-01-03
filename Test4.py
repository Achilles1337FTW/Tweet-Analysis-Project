import tweepy

consumer_key = 'Ay5nxj2rsTuCGrz9sFqQL5LfF'
consumer_secret = 'vAFT99kY3o4IOsHQ3VrRQuLSDw6I6GGXJEh478E13ATtGyuVrr'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

#for tweet_info in tweepy.Cursor(api.search, q='Election', lang = 'en', tweet_mode='extended').items(100):
#    if 'retweeted_status' in dir(tweet_info):
#        tweet=tweet_info.retweeted_status.full_text
#    else:
#        tweet=tweet_info.full_text

query = input("Enter your query: ")

#COUNT IS 10 RIGHT NOW
tweets_list = api.search(q = query, lang = 'en', count=10, tweet_mode='extended')

#for tweet in tweets_list:
#    print("----------")
#    try:
#        print(tweet.retweeted_status.full_text)
#    except:
#        print(tweet.full_text)

#for tweet in tweets_list:
#    print(tweet.id)

tweet_ids = []
for tweet in tweets_list:
    tweet_ids.append(tweet.id)

#for id in tweet_ids:
#    print(id)

tweet_file = open("tweet_file.txt", "w")

for id in tweet_ids:
    temp = str(id)
    tweet_file.write(temp + '\n')

tweet_file.close()

#status = api.get_status(id, tweet_mode="extended")
#try:
#    print(status.retweeted_status.full_text)
#except AttributeError:                             # Not a Retweet
#    print(status.full_text)
