from flask import Flask, render_template, request
from textblob import TextBlob

import tweepy
import os

# Authenticate to Twitter
KEY = os.environ.get("TWITTER_KEY")
auth = tweepy.OAuth2BearerHandler(KEY)
api = tweepy.API(auth)

app = Flask(__name__)


def get_tweets(api, username, num_of_tweets):
    tweets = api.user_timeline(screen_name=username, count=num_of_tweets)
    return tweets


def get_polarity_tag(polarity_score):
    if polarity_score < 0:
        return "Negative"
    elif polarity_score == 0:
        return "Neutral"
    elif polarity_score > 0:
        return "Positive"


def get_tag_num(polarity_tag_list):
    pos = 0
    neg = 0
    neu = 0
    for tag in polarity_tag_list:
        if tag == "Positive":
           pos += 1
        elif tag == "Negative":
            neg += 1
        elif tag == "Neutral":
            neu += 1
    return pos, neg, neu


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        num_of_tweets = int(request.form["num_of_tweets"])
        tweet_text_list = get_tweets(api, username, num_of_tweets)
        polarity_score_list = []
        polarity_tag_list = []
        polarity_subjectivity_list = []

        for tweet in tweet_text_list:
            edu = TextBlob(tweet.text)
            polarity_score = edu.sentiment.polarity
            polarity_subjectivity = edu.sentiment.subjectivity
            polarity_tag = get_polarity_tag(polarity_score)
            polarity_score_list.append(polarity_score)
            polarity_tag_list.append(polarity_tag)
            polarity_subjectivity_list.append(polarity_subjectivity)

        pos, neg, neu = get_tag_num(polarity_tag_list)
        return render_template("index.html", tweets=tweet_text_list, score=polarity_score_list, tag=polarity_tag_list,
                               subjectivity=polarity_subjectivity_list, username=username, pos=pos, neg=neg, neu=neu)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
