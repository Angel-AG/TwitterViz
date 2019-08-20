# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython

#%%
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from twython import Twython

# Obtain an OAUTH 2 Access Token
twitter = Twython(config.API_KEY, config.API_SECRET_KEY, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

#%%
# Prepare to use Access Token
twitter = Twython(config.API_KEY, access_token=ACCESS_TOKEN)

#%%
# Get users Tweets, Rts, Replies and Favs from timeline
Tweets = twitter.get_user_timeline(screen_name=config.USER, count=200)
Favs = twitter.get_favorites(screen_name=config.USER)

# for fav in Favs:
#     print(f"User: {fav['quoted_status']['user']['screen_name']} -> {fav['text']}")

#%%
# Select the columns we want to use in our DataFrame
cols = ["screen_name", "created_at", "text", "in_reply_to_status_id_str", "type"]

#%%
# Find the type of each Tweet object and add another key called "type"
for tweet in Tweets:
    tweet["created_at"] = pd.to_datetime(tweet["created_at"], infer_datetime_format=True).normalize().date()
    tweet["screen_name"] = tweet["user"]["screen_name"]
    if (tweet["in_reply_to_status_id_str"] != None):
        tweet["type"] = "Reply"
    elif "retweeted_status" in tweet:
        tweet["type"] = "RT"
    else:
        tweet["type"] = "Tweet"

#%%
# Create our DataFrame using the ids as the index and our selected columns
TweetsPD = pd.DataFrame(data=Tweets, index=[tweets["id"] for tweets in Tweets], columns=cols)

#%%
# Separate each type
Replies = TweetsPD[TweetsPD["type"] == "Reply"]
OGTweets = TweetsPD[TweetsPD["type"] == "Tweet"]
ReTweets = TweetsPD[TweetsPD["type"] == "RT"]

#%%
plt.figure(figsize=(16,16))
plt.title("Replies frequency")
sns.countplot(y="created_at", data=Replies)

#%%
plt.figure(figsize=(16,16))
plt.title("Tweets frequency")
sns.countplot(y="created_at", data=OGTweets)

#%%
plt.figure(figsize=(16,16))
plt.title("ReTweets frequency")
sns.countplot(y="created_at", data=ReTweets)