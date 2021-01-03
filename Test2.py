import tweepy
import twitter
import re
import string
from collections import Counter
import pandas as pd
import numpy

consumer_key = 'Ay5nxj2rsTuCGrz9sFqQL5LfF'
consumer_secret = 'vAFT99kY3o4IOsHQ3VrRQuLSDw6I6GGXJEh478E13ATtGyuVrr'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

#following functions used to convert tweets into more readable form
def alt_replace(old_str):           
    allowed_chars = string.digits + string.ascii_letters + "-' "
    new_str = "".join(c for c in old_str if c in allowed_chars)
    return new_str

def low_split(string):
    string2 = alt_replace(string)
    string_split = string2.split()
    ctr2 = 0
    for i in string_split:
        string_split[ctr2] = string_split[ctr2].lower()
        ctr2+=1
    return string_split

query = input("Enter your query: ")
num_tweet = 10
#date_since = "2020-11-01"   , since=date_since                         #optional parameter for query
tweets_list = api.search(q = query, lang = 'en', count=num_tweet, tweet_mode='extended')

tweet_ids = []
for tweet in tweets_list:
    tweet_ids.append(tweet.id)

tweet_str_list = []                 #chain of vars for turning tweet into string list
tweet_str_split = []                #into a dict w/ the no. of occurences
tweet_dict = []

ctr = 0
for id in tweet_ids:                #grabbing tweets from ids, adding to list
    status = api.get_status(tweet_ids[ctr], tweet_mode='extended')
    ctr+=1
    try:
        tweet_str_list.append(status.retweeted_status.full_text)
    except:
        tweet_str_list.append(status.full_text)

for tweet in tweet_str_list:
    temp = low_split(tweet)             #turns into string into list of strings
    for wrd in temp:                    #removes links and clutter from list
        if "https" in wrd:
            temp.remove(wrd)
    tweet_dict.append(Counter(temp))    #adds frequency of terms as value

tweet_dataframe = []

ctr=0
for tweet in tweet_dict:                #creating list of dataframes for tf-idf processing
    temp = pd.DataFrame()
    temp.insert(0, "Term", tweet_dict[ctr].keys(), True)
    temp.insert(1, "Frequency", tweet_dict[ctr].values(), True)
    temp.insert(2, "DocFreq", 0, True)
    temp.insert(3, "InvDocFreq", 0, True)
    temp.insert(4, "Q-Weight", 0, True)
    temp.insert(5, "Q-Normal", 0, True)
    temp.insert(6, "D-Weight", 0, True)
    temp.insert(7, "D-Normal", 0, True)
    temp.insert(8, "Product", 0, True)
    ctr+=1
    tweet_dataframe.append(temp)

tweet_dict_sum = {}                     #compilation of retrieved 'documents'
tweet_dict_sum2 = {}

ctr = 0
for doc in tweet_dict:                  #gives total # of occurrences of terms              #later realized did not require this
    tweet_dict_sum = Counter(tweet_dict_sum) + Counter(tweet_dict[ctr])
    ctr+=1

for word in tweet_dict_sum.keys():      #2ndary dictionary with values for term existing in a doc
    tweet_dict_sum2[word]=0

for word in tweet_dict_sum2.keys():
    for doc in tweet_dict:
        for term in doc.keys():
            if word == term:
                tweet_dict_sum2[word]+=1    

ctr1 =-1
for df in tweet_dataframe:                          #getting DocFrequency 
    ctr1 +=1
    ctr2 =-1
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 += 1
        for term in tweet_dict_sum2.keys():
            if term == wrd:
                tweet_dataframe[ctr1].iloc[ctr2,2]=tweet_dict_sum2.get(term)

query_split = low_split(query)
query_dict = Counter(query_split)               #query put into dict for calculating wts

ctr1 =-1
for df in tweet_dataframe:                          #getting IDf values                          
    ctr1 +=1
    ctr2 =-1
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 += 1
        temp = (num_tweet/tweet_dataframe[ctr1].iloc[ctr2,2])
        tweet_dataframe[ctr1].iloc[ctr2,3]= numpy.log10(temp)

ctr1 =-1
for df in tweet_dataframe:                          #getting Query-Wt values
    ctr1 +=1
    ctr2 =-1
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 += 1
        for term in query_dict.keys():
            if term == wrd:
                #print(tweet_dataframe[ctr1].iloc[ctr2,3], query_dict.get(term))
                temp = tweet_dataframe[ctr1].iloc[ctr2,3] * query_dict.get(term) 
                tweet_dataframe[ctr1].iloc[ctr2,4]= temp

ctr1 =-1
for df in tweet_dataframe:                          #getting Query-Normal values
    ctr1 +=1
    ctr2 =-1
    ctr3 =-1
    temp = 0
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 += 1
        temp += (numpy.power(tweet_dataframe[ctr1].iloc[ctr2,4], 2))
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr3 += 1
        if temp==0:
            temp=1
        tweet_dataframe[ctr1].iloc[ctr3,5]= (tweet_dataframe[ctr1].iloc[ctr3,4]/numpy.sqrt(temp))

ctr1 = -1
for df in tweet_dataframe:                          #getting Doc-Weight values
    ctr1 +=1
    ctr2 =-1
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 += 1
        temp = 1 + numpy.log10(tweet_dataframe[ctr1].iloc[ctr2,1])
        tweet_dataframe[ctr1].iloc[ctr2,6]=temp

ctr1 = -1
for df in tweet_dataframe:                          #getting Doc-Normal values
    ctr1 +=1
    ctr2 =-1
    ctr3 =-1
    temp = 0
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 += 1
        temp += (numpy.power(tweet_dataframe[ctr1].iloc[ctr2,6], 2))
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr3 += 1
        if temp==0:
            temp=1
        tweet_dataframe[ctr1].iloc[ctr3,7]= (tweet_dataframe[ctr1].iloc[ctr3,6]/numpy.sqrt(temp))

ctr1 = -1
for df in tweet_dataframe:                          #getting Product values
    ctr1 +=1
    ctr2 =-1
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 +=1
        temp = tweet_dataframe[ctr1].iloc[ctr2,7]*tweet_dataframe[ctr1].iloc[ctr2,5]
        tweet_dataframe[ctr1].iloc[ctr2,8]= temp

prod_list=[]
ctr1 = -1
for df in tweet_dataframe:                          #summing products into scorelist
    ctr1 +=1
    ctr2 =-1
    temp = 0
    for wrd in tweet_dataframe[ctr1]['Term']:
        ctr2 +=1
        temp += tweet_dataframe[ctr1].iloc[ctr2,8]
    prod_list.append(temp)
    
tweet_scores = pd.DataFrame()                                       #creates Dataframe with tweet ids and associated scores
tweet_scores.insert(0, "Tweet ID", tweet_ids, True)                 #then prints ranking from best to worst
tweet_scores.insert(1, "Scores", prod_list, True)
print(tweet_scores.sort_values(by=['Scores'], ascending=False))

#print("\n", tweet_dataframe[0])

#TESTING CODE
#===========================================================================
#with open("tweet_file.txt") as file_in:
#    for id in file_in:
#        temp = int(id)
#        tweet_ids.append(temp)
    
#for word in test_count:
#    print(word, " : ", test_count.get(word))
    
#test_count = [[1,2],[3,4]]
#print(test_count[0][1])

#for id in tweet_ids:
#    print(id)
#    print(type(id))

#test_str = tweet_str_list[0]

#test_split = low_split(test_str)

#test_count = Counter(test_split)
#turns split text into a dictionary of word:occurence pairs

#for tweet in tweet_str_list:
#    temp = low_split(tweet)
#    tweet_str_split.append(temp)

#df = pd.DataFrame()
#df.insert(0, "Term", tweet_dict[0].keys(), True)
#df.insert(1, "Frequency", tweet_dict[0].values(), True)

#for df in tweet_dataframe:
#    print (df, "\n")

#print(tweet_str_list[0], '\n', tweet_dict[0])

#for term in tweet_dict_sum:                #prints out all doc terms                       
#    print(term, tweet_dict_sum[term])

#dictionary.keys(); dictionary.values()

#df = pd.DataFrame()
#df.insert(0, "Term", tweet_dict_sum.keys(), True)
#df.insert(1, "Frequency", tweet_dict_sum.values(), True)

#print(tweet_dataframe[0]['Frequency'][1])
#x = tweet_dataframe[0]['Frequency'][1]
#print(numpy.sqrt(x+1))

#for term in tweet_dict_sum.keys():
#    print(term)

#for df in tweet_dataframe:
#    print(df.iloc[:,4:9], "\n")

#print(query_dict)

#print(prod_list)

#for i in tweet_str_list:
#    print(i, "\n")

#ctr=-1
#for wrd in tweet_dataframe[0]['Term']:
#    ctr+=1
#    for term in tweet_dict_sum.keys():
#        if term==wrd:
#            tweet_dataframe[0]['DocFreq'][ctr]=tweet_dict_sum.get(term)

#OBSOLETE CODE
#=====================================================================================
# rep_dict = {'(':' ',                  
#            'w/o':'without',
#            ')':' ',
#            '!':' ',
#            '@':' ',
#            '#':' ',
#            '$':' ',
#            '%':' ',
#            '^':' ',
#            '&':' and ',
#            '*':' ',
#            '_':' ',
#            '=':' ',
#            '+':' ',
#            '.':' ',
#            ',':' ',
#            '/':' ',
#            '\\':' ',
#            ':':' ',
#            ';':' ',
#           '~':' ',
#            '`':' ',
#            '"':' ',}

#def multi_replace(string, rep_dict):
#    reg_pattern = re.compile("|".join([re.escape(k) for k in sorted(rep_dict,key=len,reverse=True)]), flags=re.DOTALL)
#    return reg_pattern.sub(lambda x: rep_dict[x.group(0)], string)

#import os
#os.remove('tweet_file.txt')                deletes old txt file





