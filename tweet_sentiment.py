# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 17:24:21 2018

@author: corey
"""

def vader_tweet(tweet):
    '''returns vader polarity scores with the addition of a overall polarity score'''

    results = analyzer.polarity_scores(tweet)
    return results

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