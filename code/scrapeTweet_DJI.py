import tweepy
import json
import pandas as pd
import csv
import re
import string
import preprocessor as p
import os
import time

'''
Fill your own secret key to scrape the data
'''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def scrapetweets(search_words, date_since, numTweets, numRuns):
    
    # Define a for-loop to generate tweets at regular intervals
    # We cannot make large API call in one go

    db_tweets = pd.DataFrame(columns = [ 'createdAt','location', 'following',
                                        'followers', 'totaltweets', 'retweetcount','text']
                                )
    program_start = time.time()
    for i in range(0, numRuns):
        # We will time how long it takes to scrape the tweets for each run:
        start_run = time.time()
        
        # Collect tweets using the Cursor object as shown in tweepy
        # .Cursor() returns an object that you can iterate or loop over to access the data collected.
        tweets = tweepy.Cursor(api.search, q=search_words+" -filter:retweets"+"profile_country:us", lang="en", since=date_since, tweet_mode='extended').items(numTweets)
# Store these tweets into a python list
        tweet_list = [tweet for tweet in tweets]
# Obtain the following info (methods to call them out):
        # user.created_at - twitter timestamp
        # user.location - where he/she tweeting from, we will restrict it to USA
        # user.friends_count - no. of other users that user is following (following)
        # user.followers_count - no. of other users who are following this user (followers)
        # user.statuses_count - total tweets by user
        # retweet_count - no. of retweets
        # retweeted_status.full_text - full text of the tweet, this will be used to analyze sentiment
# Begin scraping the tweets individually:
        noTweets = 0
        for tweet in tweet_list:
# Pull the values
            createdAt = tweet.created_at
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            retweetcount = tweet.retweet_count
            text = tweet.full_text
# Add the 7 variables to the empty list - ith_tweet:
            ith_tweet = [createdAt,location, following, followers, totaltweets,
                          retweetcount, text]
# Append to dataframe - db_tweets
            db_tweets.loc[len(db_tweets)] = ith_tweet
# increase counter - noTweets  
            noTweets += 1
        
        # Run ended:
        end_run = time.time()
        duration_run = round((end_run-start_run)/60, 2)
       # time.sleep(920) #1 minute sleep time
        print('no. of tweets scraped for run {} is {}'.format(i + 1, noTweets))
        print('time take for {} run to complete is {} mins'.format(i+1, duration_run))
        
        
# Once all runs have completed, save them to a single csv file:
    from datetime import datetime
    
    # Obtain timestamp in a readable format
    to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
# Define working path and filename
    path = os.getcwd()
    filename = path + '/data/' + to_csv_timestamp + '_TRV_tweets.csv' #replace with the relevant stock label
# Store dataframe in csv with creation date timestamp
    db_tweets.to_csv(filename, index = False)
    
    program_end = time.time()
    print('Scraping has completed!')
    print('Total time taken to scrape is {} minutes.'.format(round(program_end - program_start)/60, 2))
    

# Initialise these variables:
search_words = "$TRV" #replace with relevant stock label
date_since = "2020-03-22"
numTweets = 2000
numRuns = 1
# Call the function scraptweets to start scraping
scrapetweets(search_words, date_since, numTweets, numRuns)