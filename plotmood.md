
PlotBot
In this activity, more challenging than the last, you will build a Twitter bot that sends out visualized sentiment analysis of a Twitter account's recent tweets.

Visit https://twitter.com/PlotBot5 for an example of what your script should do.

The bot receives tweets via mentions and in turn performs sentiment analysis on the most recent twitter account specified in the mention

For example, when a user tweets, "@PlotBot Analyze: @CNN," it will trigger a sentiment analysis on the CNN twitter feed.

A plot from the sentiment analysis is then tweeted to the PlotBot5 twitter feed. See below for examples of scatter plots you will generate:

@juanitasoranno.png@nancypwong.pngnytimes.png

Hints, requirements, and considerations:


* Your bot should scan your account every five minutes for mentions.
* Your bot should pull 500 most recent tweets to analyze for each incoming request.
* Your script should prevent abuse by analyzing only Twitter accounts that have not previously been analyzed.
* Your plot should include meaningful legend and labels.
It should also mention the Twitter account name of the requesting user.
When submitting your assignment, be sure to have at least three analyses tweeted out from your account (enlist the help of classmates, friends, or family, if necessary!).
Notable libraries used to complete this application include: Matplotlib, Pandas, Tweepy, TextBlob, and Seaborn.
You may find it helpful to organize your code in function(s), then call them.
If you're not yet familiar with creating functions in Python, here is a tutorial you may wish to consult: https://www.tutorialspoint.com/python/python_functions.htm.


```python
#Plot Bot

# Dependencies
import tweepy
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import json

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Setup Tweepy API Authentication
from config import (consumer_key, consumer_secret, access_token, access_token_secret)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
```


```python
def vader_tweet(tweet):
    '''returns vader polarity scores with the addition of a overall polarity score'''

    results = analyzer.polarity_scores(tweet)
    return results
```


```python
def tweet_sentiments(user):

    # Counter
    counter = 1

    # Variables for holding sentiments
    sentiments = []

    # Loop through 25 pages of tweets (total 100 tweets)
    for x in range(5):

        # Get all tweets from home feed
        public_tweets = api.user_timeline(user)

        # Loop through all tweets 
        for tweet in public_tweets:
            print("Analyzing tweet: \n")
            print("---" * 30)
            pprint(tweet['text'])
            
            # Run Vader Analysis on each tweet
            results = vader_tweet(tweet['text'])
            tweets_ago = counter
            sentiments.append(results)
            # Add to counter 
            counter = counter + 1
    polarities = list()
    positivity_list = list()
    negativity_list = list()
    for record in sentiments:
        polarities.append(record['compound'])
        positivity_list.append(record['pos'])
        negativity_list.append(record['neg'])
    
    final_json = json.dumps({ "user":user, 
                              "polarity":polarities,
                              "neg":negativity_list,
                              "pos":positivity_list
                            })
    df = pd.read_json(final_json)
    return df
    
    
    
    
```


```python
def tweet_plot(sentiments, user):
    
    #plot out polarities positive and negative
    plt.rcParams["figure.figsize"] = (10,8)
    
    pos = sentiments.pos.values
    neg = sentiments.neg.values
    polarity = sentiments.polarity.values
    
    ymax = max(np.append(pos, neg)) + .5
   
    
    f, (ax1,ax2, ax3) = plt.subplots(3, 1, sharey=True, sharex=True)
    ax1.set_ylim(ymax=ymax, ymin=-1)
    x_axis = np.arange(0,len(sentiments))
    #sns.kdeplot(sentiments.pos.values, shade=True, color="forestgreen", ax=ax1)
    #sns.kdeplot(sentiments.neg.values,shade=True, color='coral',  ax=ax2)
    ax1.plot(x_axis, pos, '-', color='coral', linewidth=4, marker="o")
    ax2.plot(x_axis, neg, '-', color='forestgreen', linewidth=4, marker="o")
    ax3.plot(x_axis, polarity, '-', color='skyblue', linewidth=4, marker="o")
    #  Incorporate the other graph properties
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    ax1.set_title("Sentiment Analysis of Tweets ({}) for {}".format(now, user))
    
    #draw horizontal line that seperates positive and negative values
    ax1.axhline(y=0, xmin=0, xmax=max(x_axis),color="red")
    ax2.axhline(y=0, xmin=0, xmax=max(x_axis),color="red")
    ax3.axhline(y=0, xmin=0, xmax=max(x_axis),color="red")
    #labels
    ax3.set_ylabel("Tweet Polarity")
    ax2.set_ylabel("Tweet Negativity")
    ax1.set_ylabel("Tweet Positivity")
    ax3.set_xlabel("Tweets Ago")
    plt.savefig(f"{user}.png")
tweet_plot(sentiments, sentiments['user'][0])    
```


```python

def mention_check(old_mentions):
    ''' activates when a twitter user tweets @plotmood and then returns a graph of polarities
        
        old_mentions: previous iterations of tweets that you want to exclude from the plots
    
    '''
    
    # Target Term
    target_term = "@MoodPlot"

    # Get the last 10 tweets
    public_tweets = api.search(target_term, count=10, result_type="recent", since_id=None)
    
    # Loop through all public_tweets
    for tweet in public_tweets["statuses"]:
        
        # Get ID and Author of most recent tweet
        ids = []
        ids.append(tweet["id"])
        tweet_author = tweet["user"]["screen_name"]
        tweet_text = tweet["text"]
        user_mentions = set()
        for user in tweet['entities']['user_mentions']:
            if user in old_mentions:
                pass
            else:
                user_mentions.add(user['screen_name'])
        

    # Print success message
    print("checked successfully, sir!")
    return user_mentions, ids

old_mentions = []
mention_check(old_mentions)
```

    checked successfully, sir!
    




    {'MoodPlot', 'co_cothoughts'}




```python
# Set timer to run 5 minutes every hour
import time 
t_end = time.time() + 3600 * 24

old_mentions = []
while(time.time() < t_end):
    mentions,ids = mention_check(old_mentions)
    
    
    if str('MoodPlot') in list(mentions):
        print("Activating Twitter bot")
        mentions.remove('MoodPlot')
        for user, ID in mentions,ids:
            print("running anaylsis for: " + mention)
            user_sentiments = tweet_sentiments(user)
            tweet_plot(user_sentiments, user)

            #read tweet_plot output
            #file = open(f"{user}.png", 'rb')
            #data = file.read()

            #upload media to twitter
            res = api.media_upload(f"{user}.png")
            print(res)
            media_id = res['media_id_string']
            print(media_id)
            api.update_status(status=f"Here's plot analysis for {user}",in_reply_to_status_id=ID, media_ids=[media_id])
            old_mentions.append(user)
            print(old_mentions)
            
            #wait thirty seconds before sending out tweet    
            time.sleep(30)

    else:
        print('nothing to tweet')

    
```

    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: co_cothoughts
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/rKQhpdRFJD'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/rKQhpdRFJD'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/rKQhpdRFJD'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/rKQhpdRFJD'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/rKQhpdRFJD'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    {'media_id': 973729196319977472, 'media_id_string': '973729196319977472', 'size': 48728, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    973729196319977472
    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: co_cothoughts
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    {'media_id': 973729331980648448, 'media_id_string': '973729331980648448', 'size': 48728, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    973729331980648448
    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: co_cothoughts
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/QTfEh6Cwi8'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/orzLd7MZ3D'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    {'media_id': 973729472414232581, 'media_id_string': '973729472414232581', 'size': 48761, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    973729472414232581
    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: co_cothoughts
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    {'media_id': 973729611182850048, 'media_id_string': '973729611182850048', 'size': 49522, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    973729611182850048
    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: co_cothoughts
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/WWLufguLpn'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/WWLufguLpn'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/WWLufguLpn'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/WWLufguLpn'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/WWLufguLpn'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/7YCsyHMT7g'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    {'media_id': 973729747858440193, 'media_id_string': '973729747858440193', 'size': 48920, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    973729747858440193
    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: co_cothoughts
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/T8KkItM28M'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/T8KkItM28M'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/T8KkItM28M'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/T8KkItM28M'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/T8KkItM28M'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'plot analysis for co_cothoughts https://t.co/9zCY9h1wrE'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@MoodPlot analyze @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '@Moodplot plot analysis for @co_cothoughts'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Weather in Irivne at 07:32 PM: light rain, 63.25 F'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    'Happiness is a warm puppy. - Charles M. Schulz'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Count your age by friends, not years. Count your life by smiles, not tears. '
     '- John Lennon')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('For every minute you are angry you lose sixty seconds of happiness. - Ralph '
     'Waldo Emerson')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('The happiness of your life depends upon the quality of your thoughts. - '
     'Marcus Aurelius')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('Folks are usually about as happy as they make their minds up to be. - '
     'Abraham Lincoln')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('7/41 Everyone has the right not to be loved, but not necessarily.\n'
     '— if you think yourself or others unloveable, you… https://t.co/OqxulKpGAA')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    '6/41 Everyone has the right to love.\n— it is never wrong to love'
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('5/41 Everyone has the right to be unique.\n'
     '— individuality is sacred, quashing what is unique is cruel')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('4/41 Everyone has the right to make mistakes.\n'
     '— you should forgive others, and especially yourself')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('3/41 3. Everyone has the right to die, but this is not an obligation.\n'
     '— You shall respect the fact that people end, but sometimes never')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('2/41 Everyone has the right to hot water, heating in winter and a tiled '
     'roof.\n'
     '— small comforts are less luxuries and closer to rights')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('1/41 Everyone has the right to live by the River Vilnele, and the River '
     'Vilnele has the right to flow by everyone.… https://t.co/ESEjMzh8kH')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('41/41 Do not surrender.\n'
     '— Never lose hope, never do anything that turns you weak, never give up what '
     'is good and tr… https://t.co/3Vhg5mJ5Y2')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('40/41. Do not fight back.\n'
     '— do not resist evil with evil, you do not save a house on fire by setting '
     'your neighbor home ablaze too')
    Analyzing tweet: 
    
    ------------------------------------------------------------------------------------------
    ('39/41. Do not defeat.\n'
     '— You never finish anything, you’ve never crushed any problem, you’ve just '
     'continued either a… https://t.co/NBqk75OchI')
    {'media_id': 973729884097794048, 'media_id_string': '973729884097794048', 'size': 49672, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    973729884097794048
    


    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-88-6efc12c6c513> in <module>()
         32         print('nothing to tweet')
         33     #wait thirty seconds before sending out tweet
    ---> 34     time.sleep(30)
         35 
    

    KeyboardInterrupt: 



```python
3600 * 24
```




    86400


