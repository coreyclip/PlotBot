
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
#tweet_plot(sentiments, sentiments['user'][0])    
```


```python

def mention_check(starting_id):
    ''' activates when a twitter user tweets @PlotMood and then returns a graph of polarities

        old_mentions: previous iterations of tweets that you want to exclude from the plots

    '''

    # Target Term
    target_term = "@MoodPlot"

    # Get the last 10 tweets
    public_tweets = api.search(target_term, count=10, result_type="recent", since_id=starting_id)

    output_dict = list()

    # Loop through all public_tweets
    for tweet in public_tweets["statuses"]:

        # Get ID and Author of most recent tweet

        tweet_id = tweet["id"]
        tweet_author = tweet["user"]["screen_name"]
        tweet_text = tweet["text"]
        user_mentions = set()
        for user in tweet['entities']['user_mentions']:
            if user in old_mentions:
                pass
            else:
                output_dict.append({'id':tweet_id, 'user':user['screen_name']})



    # Print success message
    print("checked successfully, sir!")
    return output_dict

start = None
mention_check(start)
```

    checked successfully, sir!





    [{'id': 974446844888604672, 'user': 'MoodPlot'},
     {'id': 974446844888604672, 'user': 'NASA'},
     {'id': 974446764756369409, 'user': 'MoodPlot'},
     {'id': 974446764756369409, 'user': 'ETKevinsMind'},
     {'id': 973025188634804224, 'user': 'MoodPlot'},
     {'id': 973025188634804224, 'user': 'co_cothoughts'},
     {'id': 973022735860252672, 'user': 'MoodPlot'},
     {'id': 973022735860252672, 'user': 'co_cothoughts'}]




```python
# Set timer to run 5 minutes every hour
import time
t_end = time.time() + 3600 * 24

start = None
while(time.time() < t_end):
    records = mention_check(start)



    print("Activating Twitter bot")

    for record in records:
        print("running anaylsis for: " + record['user'])
        if record['user'] == 'MoodPlot':
            pass
        else:
            user_sentiments = tweet_sentiments(record['user'])
            tweet_plot(user_sentiments, record['user'])

            #read tweet_plot output
            #file = open(f"{user}.png", 'rb')
            #data = file.read()

            #upload media to twitter
            res = api.media_upload(f"{record['user']}.png")
            print(res)
            media_id = res['media_id_string']
            print(media_id)
            api.update_status(status=f"Here's plot analysis for {record['user']}",in_reply_to_status_id=record['id'], media_ids=[media_id])

            #wait thirty seconds before sending out tweet    
            time.sleep(30)
    start = recor[-1]['id']


```

    checked successfully, sir!
    Activating Twitter bot
    running anaylsis for: MoodPlot
    running anaylsis for: NASA
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('.@NASADawn spacecraft observations of Ceres have detected recent variations '
     'in its surface, revealing that the only… https://t.co/T6IuGIj4Ih')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @NASAJPL_Edu: We've got the answers to your 2018 #NASAPiDayChallenge "
     'problems! See if your pi skills mean you can hang like a @NASA spac…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Seen STEVE? Glowing in purple &amp; green colors, a new celestial '
     'phenomenon, known as STEVE, is caused by charged part… '
     'https://t.co/vqztFlv6s9')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A newly discovered dancing purple light called STEVE is illuminating how '
     'Earth interacts with charged particles in… https://t.co/Da2rVoq89M')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Meet STEVE - a mysterious purple ribbon of light related to auroras. This '
     'thin glowing light may be a puzzle piece… https://t.co/xDRVSB9GFI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A warm welcome to our new Senate-confirmed chief financial officer, Jeff '
     'DeWit (@AZTreasurer)\n'
     '\n'
     '"I know he will be a… https://t.co/na0NhIrw0r')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @ISS_Research: Researchers now know that 93% of @StationCDRKelly's genes "
     'returned to normal after his #YearInSpace. However, the remaini…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("There's always room for pi, even on Mars! By using pi and a crater’s "
     'perimeter + area to determine how circular it… https://t.co/Abur47B5BJ')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a digital creator or active on social media? Apply to attend a '
     '#NASASocial on May 3-5 for the launch of our… https://t.co/5P60LIOKYw')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Today, we remembered Professor Stephen Hawking, who was a brilliant '
     'cosmologist that changed our view of the univer… https://t.co/lqE7QHA89k')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @Dr_ThomasZ: Stephen Hawking's ability to communicate to the general "
     'public about the importance to study the universe and move science…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Following the passing of renowned astrophysicist Stephen Hawking, we put '
     'together a look at footage of his lectures… https://t.co/HEwAMEKOrV')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL: Pi, you the real MVP. @NASA uses #pi to explore outer space, '
     'and you can too! \n'
     '\n'
     'Take the #NASAPiDayChallenge: https://t.co/ZcW…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Did you know that we use pi to explore space, search for quakes on Mars and '
     'even calculate the rotation of asteroid… https://t.co/dAp8UBhV2V')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How do you like your pi? Colorful and fun? Today we’re celebrating the '
     'beloved number known as pi with games design… https://t.co/PkBi7RZ9K1')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How pi savvy are you? We’re inviting you to find out by participating in our '
     '2018 #PiDay Challenge involving pi and… https://t.co/7BIabzbjnX')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL_Edu: How many pi digits do you need if you want to explore space '
     'with @NASA? The answer may surprise you: https://t.co/k8h93uMa…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('What makes pi so special? Our scientists and engineers use this special '
     'number to learn about moons, planets, stars… https://t.co/TZQXZXM3QI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @chandraxray: #Pi has been calculated to over a trillion digits. There '
     'are that many stars in the Andromeda Galaxy alone! Happy #PiDay!…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAHubble: Happy #PiDay! March 14th represented in numbers is 3.14, '
     'which are the first three numbers in the pi constant. Pi is a math…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('.@NASADawn spacecraft observations of Ceres have detected recent variations '
     'in its surface, revealing that the only… https://t.co/T6IuGIj4Ih')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @NASAJPL_Edu: We've got the answers to your 2018 #NASAPiDayChallenge "
     'problems! See if your pi skills mean you can hang like a @NASA spac…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Seen STEVE? Glowing in purple &amp; green colors, a new celestial '
     'phenomenon, known as STEVE, is caused by charged part… '
     'https://t.co/vqztFlv6s9')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A newly discovered dancing purple light called STEVE is illuminating how '
     'Earth interacts with charged particles in… https://t.co/Da2rVoq89M')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Meet STEVE - a mysterious purple ribbon of light related to auroras. This '
     'thin glowing light may be a puzzle piece… https://t.co/xDRVSB9GFI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A warm welcome to our new Senate-confirmed chief financial officer, Jeff '
     'DeWit (@AZTreasurer)\n'
     '\n'
     '"I know he will be a… https://t.co/na0NhIrw0r')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @ISS_Research: Researchers now know that 93% of @StationCDRKelly's genes "
     'returned to normal after his #YearInSpace. However, the remaini…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("There's always room for pi, even on Mars! By using pi and a crater’s "
     'perimeter + area to determine how circular it… https://t.co/Abur47B5BJ')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a digital creator or active on social media? Apply to attend a '
     '#NASASocial on May 3-5 for the launch of our… https://t.co/5P60LIOKYw')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Today, we remembered Professor Stephen Hawking, who was a brilliant '
     'cosmologist that changed our view of the univer… https://t.co/lqE7QHA89k')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @Dr_ThomasZ: Stephen Hawking's ability to communicate to the general "
     'public about the importance to study the universe and move science…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Following the passing of renowned astrophysicist Stephen Hawking, we put '
     'together a look at footage of his lectures… https://t.co/HEwAMEKOrV')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL: Pi, you the real MVP. @NASA uses #pi to explore outer space, '
     'and you can too! \n'
     '\n'
     'Take the #NASAPiDayChallenge: https://t.co/ZcW…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Did you know that we use pi to explore space, search for quakes on Mars and '
     'even calculate the rotation of asteroid… https://t.co/dAp8UBhV2V')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How do you like your pi? Colorful and fun? Today we’re celebrating the '
     'beloved number known as pi with games design… https://t.co/PkBi7RZ9K1')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How pi savvy are you? We’re inviting you to find out by participating in our '
     '2018 #PiDay Challenge involving pi and… https://t.co/7BIabzbjnX')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL_Edu: How many pi digits do you need if you want to explore space '
     'with @NASA? The answer may surprise you: https://t.co/k8h93uMa…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('What makes pi so special? Our scientists and engineers use this special '
     'number to learn about moons, planets, stars… https://t.co/TZQXZXM3QI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @chandraxray: #Pi has been calculated to over a trillion digits. There '
     'are that many stars in the Andromeda Galaxy alone! Happy #PiDay!…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAHubble: Happy #PiDay! March 14th represented in numbers is 3.14, '
     'which are the first three numbers in the pi constant. Pi is a math…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('.@NASADawn spacecraft observations of Ceres have detected recent variations '
     'in its surface, revealing that the only… https://t.co/T6IuGIj4Ih')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @NASAJPL_Edu: We've got the answers to your 2018 #NASAPiDayChallenge "
     'problems! See if your pi skills mean you can hang like a @NASA spac…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Seen STEVE? Glowing in purple &amp; green colors, a new celestial '
     'phenomenon, known as STEVE, is caused by charged part… '
     'https://t.co/vqztFlv6s9')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A newly discovered dancing purple light called STEVE is illuminating how '
     'Earth interacts with charged particles in… https://t.co/Da2rVoq89M')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Meet STEVE - a mysterious purple ribbon of light related to auroras. This '
     'thin glowing light may be a puzzle piece… https://t.co/xDRVSB9GFI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A warm welcome to our new Senate-confirmed chief financial officer, Jeff '
     'DeWit (@AZTreasurer)\n'
     '\n'
     '"I know he will be a… https://t.co/na0NhIrw0r')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @ISS_Research: Researchers now know that 93% of @StationCDRKelly's genes "
     'returned to normal after his #YearInSpace. However, the remaini…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("There's always room for pi, even on Mars! By using pi and a crater’s "
     'perimeter + area to determine how circular it… https://t.co/Abur47B5BJ')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a digital creator or active on social media? Apply to attend a '
     '#NASASocial on May 3-5 for the launch of our… https://t.co/5P60LIOKYw')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Today, we remembered Professor Stephen Hawking, who was a brilliant '
     'cosmologist that changed our view of the univer… https://t.co/lqE7QHA89k')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @Dr_ThomasZ: Stephen Hawking's ability to communicate to the general "
     'public about the importance to study the universe and move science…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Following the passing of renowned astrophysicist Stephen Hawking, we put '
     'together a look at footage of his lectures… https://t.co/HEwAMEKOrV')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL: Pi, you the real MVP. @NASA uses #pi to explore outer space, '
     'and you can too! \n'
     '\n'
     'Take the #NASAPiDayChallenge: https://t.co/ZcW…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Did you know that we use pi to explore space, search for quakes on Mars and '
     'even calculate the rotation of asteroid… https://t.co/dAp8UBhV2V')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How do you like your pi? Colorful and fun? Today we’re celebrating the '
     'beloved number known as pi with games design… https://t.co/PkBi7RZ9K1')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How pi savvy are you? We’re inviting you to find out by participating in our '
     '2018 #PiDay Challenge involving pi and… https://t.co/7BIabzbjnX')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL_Edu: How many pi digits do you need if you want to explore space '
     'with @NASA? The answer may surprise you: https://t.co/k8h93uMa…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('What makes pi so special? Our scientists and engineers use this special '
     'number to learn about moons, planets, stars… https://t.co/TZQXZXM3QI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @chandraxray: #Pi has been calculated to over a trillion digits. There '
     'are that many stars in the Andromeda Galaxy alone! Happy #PiDay!…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAHubble: Happy #PiDay! March 14th represented in numbers is 3.14, '
     'which are the first three numbers in the pi constant. Pi is a math…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('.@NASADawn spacecraft observations of Ceres have detected recent variations '
     'in its surface, revealing that the only… https://t.co/T6IuGIj4Ih')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @NASAJPL_Edu: We've got the answers to your 2018 #NASAPiDayChallenge "
     'problems! See if your pi skills mean you can hang like a @NASA spac…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Seen STEVE? Glowing in purple &amp; green colors, a new celestial '
     'phenomenon, known as STEVE, is caused by charged part… '
     'https://t.co/vqztFlv6s9')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A newly discovered dancing purple light called STEVE is illuminating how '
     'Earth interacts with charged particles in… https://t.co/Da2rVoq89M')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Meet STEVE - a mysterious purple ribbon of light related to auroras. This '
     'thin glowing light may be a puzzle piece… https://t.co/xDRVSB9GFI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A warm welcome to our new Senate-confirmed chief financial officer, Jeff '
     'DeWit (@AZTreasurer)\n'
     '\n'
     '"I know he will be a… https://t.co/na0NhIrw0r')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @ISS_Research: Researchers now know that 93% of @StationCDRKelly's genes "
     'returned to normal after his #YearInSpace. However, the remaini…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("There's always room for pi, even on Mars! By using pi and a crater’s "
     'perimeter + area to determine how circular it… https://t.co/Abur47B5BJ')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a digital creator or active on social media? Apply to attend a '
     '#NASASocial on May 3-5 for the launch of our… https://t.co/5P60LIOKYw')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Today, we remembered Professor Stephen Hawking, who was a brilliant '
     'cosmologist that changed our view of the univer… https://t.co/lqE7QHA89k')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @Dr_ThomasZ: Stephen Hawking's ability to communicate to the general "
     'public about the importance to study the universe and move science…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Following the passing of renowned astrophysicist Stephen Hawking, we put '
     'together a look at footage of his lectures… https://t.co/HEwAMEKOrV')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL: Pi, you the real MVP. @NASA uses #pi to explore outer space, '
     'and you can too! \n'
     '\n'
     'Take the #NASAPiDayChallenge: https://t.co/ZcW…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Did you know that we use pi to explore space, search for quakes on Mars and '
     'even calculate the rotation of asteroid… https://t.co/dAp8UBhV2V')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How do you like your pi? Colorful and fun? Today we’re celebrating the '
     'beloved number known as pi with games design… https://t.co/PkBi7RZ9K1')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How pi savvy are you? We’re inviting you to find out by participating in our '
     '2018 #PiDay Challenge involving pi and… https://t.co/7BIabzbjnX')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL_Edu: How many pi digits do you need if you want to explore space '
     'with @NASA? The answer may surprise you: https://t.co/k8h93uMa…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('What makes pi so special? Our scientists and engineers use this special '
     'number to learn about moons, planets, stars… https://t.co/TZQXZXM3QI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @chandraxray: #Pi has been calculated to over a trillion digits. There '
     'are that many stars in the Andromeda Galaxy alone! Happy #PiDay!…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAHubble: Happy #PiDay! March 14th represented in numbers is 3.14, '
     'which are the first three numbers in the pi constant. Pi is a math…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('.@NASADawn spacecraft observations of Ceres have detected recent variations '
     'in its surface, revealing that the only… https://t.co/T6IuGIj4Ih')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @NASAJPL_Edu: We've got the answers to your 2018 #NASAPiDayChallenge "
     'problems! See if your pi skills mean you can hang like a @NASA spac…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Seen STEVE? Glowing in purple &amp; green colors, a new celestial '
     'phenomenon, known as STEVE, is caused by charged part… '
     'https://t.co/vqztFlv6s9')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A newly discovered dancing purple light called STEVE is illuminating how '
     'Earth interacts with charged particles in… https://t.co/Da2rVoq89M')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Meet STEVE - a mysterious purple ribbon of light related to auroras. This '
     'thin glowing light may be a puzzle piece… https://t.co/xDRVSB9GFI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('A warm welcome to our new Senate-confirmed chief financial officer, Jeff '
     'DeWit (@AZTreasurer)\n'
     '\n'
     '"I know he will be a… https://t.co/na0NhIrw0r')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @ISS_Research: Researchers now know that 93% of @StationCDRKelly's genes "
     'returned to normal after his #YearInSpace. However, the remaini…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("There's always room for pi, even on Mars! By using pi and a crater’s "
     'perimeter + area to determine how circular it… https://t.co/Abur47B5BJ')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a digital creator or active on social media? Apply to attend a '
     '#NASASocial on May 3-5 for the launch of our… https://t.co/5P60LIOKYw')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Today, we remembered Professor Stephen Hawking, who was a brilliant '
     'cosmologist that changed our view of the univer… https://t.co/lqE7QHA89k')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ("RT @Dr_ThomasZ: Stephen Hawking's ability to communicate to the general "
     'public about the importance to study the universe and move science…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Following the passing of renowned astrophysicist Stephen Hawking, we put '
     'together a look at footage of his lectures… https://t.co/HEwAMEKOrV')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL: Pi, you the real MVP. @NASA uses #pi to explore outer space, '
     'and you can too! \n'
     '\n'
     'Take the #NASAPiDayChallenge: https://t.co/ZcW…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Did you know that we use pi to explore space, search for quakes on Mars and '
     'even calculate the rotation of asteroid… https://t.co/dAp8UBhV2V')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How do you like your pi? Colorful and fun? Today we’re celebrating the '
     'beloved number known as pi with games design… https://t.co/PkBi7RZ9K1')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('How pi savvy are you? We’re inviting you to find out by participating in our '
     '2018 #PiDay Challenge involving pi and… https://t.co/7BIabzbjnX')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAJPL_Edu: How many pi digits do you need if you want to explore space '
     'with @NASA? The answer may surprise you: https://t.co/k8h93uMa…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('What makes pi so special? Our scientists and engineers use this special '
     'number to learn about moons, planets, stars… https://t.co/TZQXZXM3QI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @chandraxray: #Pi has been calculated to over a trillion digits. There '
     'are that many stars in the Andromeda Galaxy alone! Happy #PiDay!…')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('RT @NASAHubble: Happy #PiDay! March 14th represented in numbers is 3.14, '
     'which are the first three numbers in the pi constant. Pi is a math…')
    {'media_id': 974448875225341952, 'media_id_string': '974448875225341952', 'size': 41991, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    974448875225341952
    running anaylsis for: MoodPlot
    running anaylsis for: ETKevinsMind
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@MarkHarrisNYC Just watch RHONY and you’ll be good, or do the reunions for '
     'the first couple seasons')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@hoglundan The Alley !'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a #GoldenGirls fan ? Do you live in Boston or want to travel there ? '
     'My friend Eric is hosting a Golden Gir… https://t.co/nbNgy3mEDo')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@AMCTheatres Still haven’t gone to an AMC theatre since you stopped using '
     '@MoviePass at the Boston Common Loews. Mo… https://t.co/ch2AoBNtwO')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@screencrushnews @20thcenturyfox Keep it grounded please'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@kirstiealley Same with you and your career after Cheers ended. I mean '
     'between It Takes Two and For Richer or Poore… https://t.co/ZMkqFGIzaW')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@Marvel @netflix shows need to follow the path of The Crown, 10 episodes, no '
     'more!')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@JBAwardsCircuit I’m betting she did the Bitch Sesh podcast to try and cover '
     'her ass too')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@jasonosia Yea, what a terrible call on the winner, they picked the boring '
     'meal, boring season for @BravoTopChef')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'This final 2 on Top Chef are baffling to me'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Not cute Erika, not cute! #RHOBH https://t.co/fGpnilYP1y'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Team @TeddiMellencamp all the way! #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'I genuinely don’t understand how Erika is bonding with Dorit #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@filmguy619 Agreed, the performances are what stick the landing. I think the '
     'show tackles emotions in a very intere… https://t.co/5RwEUhTD4Z')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@yashar @xeni Hey @DrJillStein  do you have any money you could lend her. I '
     'kind of remember you taking money from… https://t.co/KcQ1fcEEST')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@sweetgreen Another bad customer experience this week, I think I’m good on '
     'you all for a while #Customerexperience')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@danblackroyd Bening in Kids are alright \n'
     'Blanchett in Blue Jasmine  \n'
     'Chastain in ZDT\n'
     'Cotillard in Two Days One Nig… https://t.co/KV6z8Baxha')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('I won’t be watching #Rise since they changed the sexuality of the teacher '
     '(real life person) from gay to straight')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Why don’t they have videos for the   @SAGawards Best Film Ensemble winners? '
     'I’m want to see those wins for The Bird… https://t.co/ve6VxpA7rI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Fuck you @netflix and @unitedtalent ! https://t.co/V74mhEAthX'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@MarkHarrisNYC Just watch RHONY and you’ll be good, or do the reunions for '
     'the first couple seasons')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@hoglundan The Alley !'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a #GoldenGirls fan ? Do you live in Boston or want to travel there ? '
     'My friend Eric is hosting a Golden Gir… https://t.co/nbNgy3mEDo')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@AMCTheatres Still haven’t gone to an AMC theatre since you stopped using '
     '@MoviePass at the Boston Common Loews. Mo… https://t.co/ch2AoBNtwO')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@screencrushnews @20thcenturyfox Keep it grounded please'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@kirstiealley Same with you and your career after Cheers ended. I mean '
     'between It Takes Two and For Richer or Poore… https://t.co/ZMkqFGIzaW')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@Marvel @netflix shows need to follow the path of The Crown, 10 episodes, no '
     'more!')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@JBAwardsCircuit I’m betting she did the Bitch Sesh podcast to try and cover '
     'her ass too')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@jasonosia Yea, what a terrible call on the winner, they picked the boring '
     'meal, boring season for @BravoTopChef')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'This final 2 on Top Chef are baffling to me'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Not cute Erika, not cute! #RHOBH https://t.co/fGpnilYP1y'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Team @TeddiMellencamp all the way! #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'I genuinely don’t understand how Erika is bonding with Dorit #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@filmguy619 Agreed, the performances are what stick the landing. I think the '
     'show tackles emotions in a very intere… https://t.co/5RwEUhTD4Z')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@yashar @xeni Hey @DrJillStein  do you have any money you could lend her. I '
     'kind of remember you taking money from… https://t.co/KcQ1fcEEST')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@sweetgreen Another bad customer experience this week, I think I’m good on '
     'you all for a while #Customerexperience')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@danblackroyd Bening in Kids are alright \n'
     'Blanchett in Blue Jasmine  \n'
     'Chastain in ZDT\n'
     'Cotillard in Two Days One Nig… https://t.co/KV6z8Baxha')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('I won’t be watching #Rise since they changed the sexuality of the teacher '
     '(real life person) from gay to straight')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Why don’t they have videos for the   @SAGawards Best Film Ensemble winners? '
     'I’m want to see those wins for The Bird… https://t.co/ve6VxpA7rI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Fuck you @netflix and @unitedtalent ! https://t.co/V74mhEAthX'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@MarkHarrisNYC Just watch RHONY and you’ll be good, or do the reunions for '
     'the first couple seasons')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@hoglundan The Alley !'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a #GoldenGirls fan ? Do you live in Boston or want to travel there ? '
     'My friend Eric is hosting a Golden Gir… https://t.co/nbNgy3mEDo')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@AMCTheatres Still haven’t gone to an AMC theatre since you stopped using '
     '@MoviePass at the Boston Common Loews. Mo… https://t.co/ch2AoBNtwO')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@screencrushnews @20thcenturyfox Keep it grounded please'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@kirstiealley Same with you and your career after Cheers ended. I mean '
     'between It Takes Two and For Richer or Poore… https://t.co/ZMkqFGIzaW')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@Marvel @netflix shows need to follow the path of The Crown, 10 episodes, no '
     'more!')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@JBAwardsCircuit I’m betting she did the Bitch Sesh podcast to try and cover '
     'her ass too')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@jasonosia Yea, what a terrible call on the winner, they picked the boring '
     'meal, boring season for @BravoTopChef')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'This final 2 on Top Chef are baffling to me'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Not cute Erika, not cute! #RHOBH https://t.co/fGpnilYP1y'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Team @TeddiMellencamp all the way! #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'I genuinely don’t understand how Erika is bonding with Dorit #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@filmguy619 Agreed, the performances are what stick the landing. I think the '
     'show tackles emotions in a very intere… https://t.co/5RwEUhTD4Z')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@yashar @xeni Hey @DrJillStein  do you have any money you could lend her. I '
     'kind of remember you taking money from… https://t.co/KcQ1fcEEST')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@sweetgreen Another bad customer experience this week, I think I’m good on '
     'you all for a while #Customerexperience')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@danblackroyd Bening in Kids are alright \n'
     'Blanchett in Blue Jasmine  \n'
     'Chastain in ZDT\n'
     'Cotillard in Two Days One Nig… https://t.co/KV6z8Baxha')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('I won’t be watching #Rise since they changed the sexuality of the teacher '
     '(real life person) from gay to straight')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Why don’t they have videos for the   @SAGawards Best Film Ensemble winners? '
     'I’m want to see those wins for The Bird… https://t.co/ve6VxpA7rI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Fuck you @netflix and @unitedtalent ! https://t.co/V74mhEAthX'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@MarkHarrisNYC Just watch RHONY and you’ll be good, or do the reunions for '
     'the first couple seasons')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@hoglundan The Alley !'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a #GoldenGirls fan ? Do you live in Boston or want to travel there ? '
     'My friend Eric is hosting a Golden Gir… https://t.co/nbNgy3mEDo')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@AMCTheatres Still haven’t gone to an AMC theatre since you stopped using '
     '@MoviePass at the Boston Common Loews. Mo… https://t.co/ch2AoBNtwO')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@screencrushnews @20thcenturyfox Keep it grounded please'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@kirstiealley Same with you and your career after Cheers ended. I mean '
     'between It Takes Two and For Richer or Poore… https://t.co/ZMkqFGIzaW')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@Marvel @netflix shows need to follow the path of The Crown, 10 episodes, no '
     'more!')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@JBAwardsCircuit I’m betting she did the Bitch Sesh podcast to try and cover '
     'her ass too')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@jasonosia Yea, what a terrible call on the winner, they picked the boring '
     'meal, boring season for @BravoTopChef')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'This final 2 on Top Chef are baffling to me'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Not cute Erika, not cute! #RHOBH https://t.co/fGpnilYP1y'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Team @TeddiMellencamp all the way! #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'I genuinely don’t understand how Erika is bonding with Dorit #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@filmguy619 Agreed, the performances are what stick the landing. I think the '
     'show tackles emotions in a very intere… https://t.co/5RwEUhTD4Z')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@yashar @xeni Hey @DrJillStein  do you have any money you could lend her. I '
     'kind of remember you taking money from… https://t.co/KcQ1fcEEST')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@sweetgreen Another bad customer experience this week, I think I’m good on '
     'you all for a while #Customerexperience')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@danblackroyd Bening in Kids are alright \n'
     'Blanchett in Blue Jasmine  \n'
     'Chastain in ZDT\n'
     'Cotillard in Two Days One Nig… https://t.co/KV6z8Baxha')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('I won’t be watching #Rise since they changed the sexuality of the teacher '
     '(real life person) from gay to straight')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Why don’t they have videos for the   @SAGawards Best Film Ensemble winners? '
     'I’m want to see those wins for The Bird… https://t.co/ve6VxpA7rI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Fuck you @netflix and @unitedtalent ! https://t.co/V74mhEAthX'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@MarkHarrisNYC Just watch RHONY and you’ll be good, or do the reunions for '
     'the first couple seasons')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@hoglundan The Alley !'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Are you a #GoldenGirls fan ? Do you live in Boston or want to travel there ? '
     'My friend Eric is hosting a Golden Gir… https://t.co/nbNgy3mEDo')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@AMCTheatres Still haven’t gone to an AMC theatre since you stopped using '
     '@MoviePass at the Boston Common Loews. Mo… https://t.co/ch2AoBNtwO')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    '@screencrushnews @20thcenturyfox Keep it grounded please'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@kirstiealley Same with you and your career after Cheers ended. I mean '
     'between It Takes Two and For Richer or Poore… https://t.co/ZMkqFGIzaW')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@Marvel @netflix shows need to follow the path of The Crown, 10 episodes, no '
     'more!')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@JBAwardsCircuit I’m betting she did the Bitch Sesh podcast to try and cover '
     'her ass too')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@jasonosia Yea, what a terrible call on the winner, they picked the boring '
     'meal, boring season for @BravoTopChef')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'This final 2 on Top Chef are baffling to me'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Not cute Erika, not cute! #RHOBH https://t.co/fGpnilYP1y'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Team @TeddiMellencamp all the way! #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'I genuinely don’t understand how Erika is bonding with Dorit #RHOBH'
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@filmguy619 Agreed, the performances are what stick the landing. I think the '
     'show tackles emotions in a very intere… https://t.co/5RwEUhTD4Z')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@yashar @xeni Hey @DrJillStein  do you have any money you could lend her. I '
     'kind of remember you taking money from… https://t.co/KcQ1fcEEST')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@sweetgreen Another bad customer experience this week, I think I’m good on '
     'you all for a while #Customerexperience')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('@danblackroyd Bening in Kids are alright \n'
     'Blanchett in Blue Jasmine  \n'
     'Chastain in ZDT\n'
     'Cotillard in Two Days One Nig… https://t.co/KV6z8Baxha')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('I won’t be watching #Rise since they changed the sexuality of the teacher '
     '(real life person) from gay to straight')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    ('Why don’t they have videos for the   @SAGawards Best Film Ensemble winners? '
     'I’m want to see those wins for The Bird… https://t.co/ve6VxpA7rI')
    Analyzing tweet:

    ------------------------------------------------------------------------------------------
    'Fuck you @netflix and @unitedtalent ! https://t.co/V74mhEAthX'
    {'media_id': 974449014555865088, 'media_id_string': '974449014555865088', 'size': 54233, 'expires_after_secs': 86400, 'image': {'image_type': 'image/png', 'w': 720, 'h': 576}}
    974449014555865088
