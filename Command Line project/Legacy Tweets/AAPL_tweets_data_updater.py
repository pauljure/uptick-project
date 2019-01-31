import tweepy
import csv
import pandas as pd
import json

import google_sheets_api as sheet

####input your credentials here
consumer_key = 'r1PWmElzBiEMA2CGVSToqeau3'
consumer_secret = 'vfidRAc3xn4hxnMMeUC0nNoDOhzmc5pvEmu93vTTWT88aam2aS'
access_token = '1053031421319794688-LrvfrNzNwRBxDOH2Qka16dBlg2mupu'
access_token_secret = '99Agon5uWaFzpH96wd6OXzjqihZ3ugKWYCavkCBoJoFSY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


def update_AAPL_tweets_data():
    for tweet in tweepy.Cursor(api.search,q="#AAPL",count=100, lang="en", since="2018-11-07").items():
        print("adding tweet to AAPL_tweets_data...")
        sheet.AAPL_tweets_data.append_row([str(tweet.created_at), tweet.text.replace("'b",""), tweet.retweet_count, tweet.favorite_count])

