import twitter
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from secrets import consumer_key, consumer_secret, access_token_key, access_token_secret

api = twitter.Api(consumer_key = consumer_key,
                    consumer_secret = consumer_secret,
                    access_token_key = access_token_key,
                    access_token_secret = access_token_secret)

# global variable to store all comments
all_comments = []

def find_tweet_ids(name, iterations):
    """
    :param name: twitter username, string
    :param iterations: integer
    :return: a set of unique tweet ids
    """

    global api

    tweet_ids = []
    max_id = ''
    for i in range(iterations):
        statuses = api.GetUserTimeline(screen_name=name, exclude_replies=True, count=200, max_id=max_id)
        for idx in range(len(statuses)):
            tweet_ids.append(str(statuses[idx].id))
        max_id = min(tweet_ids)
    return set(tweet_ids)

def find_comments(tweet_id, name):
    """
    Finds all the comments left on the specified tweets
    :param tweet_id: integer
    :param name: string
    :return: array of all comments
    """
    
    global all_comments

    r = requests.get("https://twitter.com/" + name + "/status/" + str(tweet_id))
    assert r.status_code == 200
    content = r.content
    html_soup = bs(content, "html.parser")
    comments = html_soup.find_all("p", {"class": "TweetTextSize js-tweet-text tweet-text"})
    for comment in comments:
        all_comments.append(comment.text)
    return all_comments

def stopwords():
    stopwords = set(STOPWORDS)
    stopwords_custom = ["aria", "img", "Emoji", "atreply", "twitter", "Hi", "train", "district", "service"]
    station_names = []
    for word in stopwords_custom:
        stopwords.add(word)
    return stopwords

def show_wordcloud(dataframe, stopwords, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=100,
        max_font_size=60, 
        scale=5,
        #random_state=1
    ).generate(str(dataframe))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

def main(iterations):
    global api
    try:
        api.VerifyCredentials()
    except Exception as err:
        print(err.message)

    name = input("Enter a twitter handle: \n")
    tweet_ids = find_tweet_ids(name, iterations)
    print("Found all tweet ids ")
    if tweet_ids:
        for id in tweet_ids:
            find_comments(id, name)
    df = pd.DataFrame(all_comments)
    print(df)
    show_wordcloud(df, stopwords)

if __name__ == '__main__':
    main(1)
