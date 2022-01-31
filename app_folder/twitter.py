import requests
import ast
import spacy

from .models import db, User, Tweet

nlp = spacy.load("en_core_web_sm")

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def get_user_and_tweets(username):
    """
    A function which makes a call to obtain data pertaining to a Twitter user and their most recent 200
    events on their timeline.  *Note* If all of the past 200 events on their timeline were replies or
    retweets then it is possible that no Tweets will be returned *Note*

    :param username: str -- a user's Twitter handle
    :returns tweets_added: int -- a number representing the number of tweets added this session
    """

    # The link at which we will be making calls
    HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'

    # Use the `literal_eval` method to turn the JSON response into a Python dictionary
    user = ast.literal_eval(requests.get(HEROKU_URL + username).text)

    try:

        # If the user already exists, create a variable of their record from the database
        if User.query.get(user['twitter_handle']['id']):
            db_user = User.query.get(user['twitter_handle']['id'])
        else:
            # Otherwise, create a new instance and add it to the database
            db_user = User(id=user['twitter_handle']['id'],
                           name=user['twitter_handle']['username'])
            db.session.add(db_user)

        # If we don't add any tweets this session, we will make a note of it
        tweets_added = 0

        for tweet in user['tweets']:

            # If the tweet id exists in the database we will go against the non-unique constraint so,
            # this line of code will break the loop meaning we already obtained the other tweets
            if Tweet.query.get(tweet['id']):
                break
            else:
                # Otherwise, add a new Tweet record
                db_tweet = Tweet(id=tweet['id'], text=tweet['full_text'], vect=nlp(tweet["full_text"]).vector)

                # Append it to the User instance
                db_user.tweets.append(db_tweet)

                # Add it to the database session
                db.session.add(db_tweet)

                # Incrementing to let us know how many tweets we added
                tweets_added += 1

    # If ANYTHING in our try statement fails, we will raise the error here
    except Exception as e:
        raise e

    db.session.commit()

    return tweets_added
