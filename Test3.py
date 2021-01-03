import twitter
import tweepy

my_key = 'Ay5nxj2rsTuCGrz9sFqQL5LfF'
my_secret = 'vAFT99kY3o4IOsHQ3VrRQuLSDw6I6GGXJEh478E13ATtGyuVrr'
my_token = '1153323485462241280-hi0xuMYoQGsqIvV4KyTUstMChvXmhB'
my_token_secret = 'tUPiTwHzdmkjeqCkRR7D923MSuwnMBw8r58CeQCsuIXre'
api = twitter.Api(my_key, my_secret, my_token, my_token_secret)

results = api.GetSearch(
    raw_query="q=West West West%20&result_type=recent&since=2019-07-19&count=100")

print(type(results))
print(type(results[0]))
#print(results[0].id)
print(results[0].text)
#print(results[0].user.id)
print('===========')

ctr = 0
for i in results:
    print(results[ctr].id)
    ctr+=1

#use twitter raw query to pull initial phrase then store ONLY the tweet
#and rank them using the tf-idf algorithim
