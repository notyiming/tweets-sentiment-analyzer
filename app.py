from flask import Flask, render_template, request
from textblob import TextBlob

import datetime

import tweepy

auth = tweepy.OAuthHandler("w1X27TSdDw4tuGPJ9WvnqN5PN", "9LajqdEafIwOx0tsCfPbgHaewmzFC3jjohxX56tLap8VokfLGZ")
auth.set_access_token("813994085560107008-6T9Y4DrlXTO5fLjk9J6RfMKTUiGnd2Q", "itRGLrIyPoRufb3esbpUybE0CZnsKQY7KZ3euz5lL3UjV")
api = tweepy.API(auth)

app = Flask(__name__)


def get_tweets(api, username, max_tweet_age):
    page = 1
    print(max_tweet_age)
    tweet_text_list = []

    deadend = False
    while True:
        tweets = api.user_timeline(username, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days <= max_tweet_age:
                tweet_text_list.append(tweet.text)
            else:
                deadend = True
                return tweet_text_list
        if not deadend:
            page = page + 1


def getPolarityTag(polarity_score):
    if polarity_score < 0:
        return "Negative"
    elif polarity_score == 0:
        return "Neutral"
    elif polarity_score > 0:
        return "Positive"


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        # text = request.form["text"]
        # edu = TextBlob(text)
        # polarity_score = edu.sentiment.polarity
        # polarity_subjectivity = edu.sentiment.subjectivity
        # polarity_text = getPolarityResult(polarity_score)
        # print(polarity_score, polarity_text)
        # return render_template("index.html", results=polarity_text, score=polarity_score, sub=polarity_subjectivity)

        username = request.form["username"]
        max_tweet_age = 2
        tweet_text_list = get_tweets(api, username, max_tweet_age)
        print(tweet_text_list)
        polarity_score_list = []
        polarity_tag_list = []
        polarity_subjectivity_list = []
        for tweet in tweet_text_list:
            edu = TextBlob(tweet)
            polarity_score = edu.sentiment.polarity
            polarity_subjectivity = edu.sentiment.subjectivity
            polarity_tag = getPolarityTag(polarity_score)
            polarity_score_list.append(polarity_score)
            polarity_tag_list.append(polarity_tag)
            polarity_subjectivity_list.append(polarity_subjectivity)
        print(polarity_score_list, polarity_tag_list, polarity_subjectivity_list)

        return render_template("index.html", tweets=tweet_text_list, score=polarity_score_list, tag=polarity_tag_list,
                               subjectivity=polarity_subjectivity_list, username=username)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
