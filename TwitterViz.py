# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
from IPython import get_ipython


#%%
import config
import pandas as pd
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
# Perform a search by user to test Twython
Tweets = twitter.get_user_timeline(screen_name=config.USER, exclude_replies=True, include_rts=False, count=200)

for tweet in Tweets:
    print(f"User: {tweet['user']['screen_name']} -> {tweet['text']}")
