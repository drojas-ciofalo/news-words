import config
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud
from nltk.corpus import stopwords

nltk.download('stopwords')

def get_news(country):
    url = "https://newsdata2.p.rapidapi.com/news"

    headers = {
	    "X-RapidAPI-Key": config.news_api_key,
	    "X-RapidAPI-Host": "newsdata2.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=dict(country=country))
    return response.json()

def create_df(data):
    df = pd.DataFrame(data["results"])
    df["content"] = df["content"].replace("’", "", regex=True)
    return df

def wordcloud_plot(df, stop_words, country):
    # Concatenate the text from the column 'content'
    df = df.dropna(subset=["content"])
    contents = " ".join(df["content"])

    # Create the word cloud image
    word_cloud = WordCloud(background_color='white',
                       stopwords=stop_words,
                       width=800,
                       height=400)

    # Generate the word cloud using the review data
    word_cloud.generate(contents)

    # Display the word cloud
    title = "News from " + country.upper()
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.savefig(f'{country}.png', dpi=150)
    #plt.show()

def post_telegram(country):
    TOKEN = config.TG_TOKEN
    chat_id = config.chat_id
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
    files = {"photo": open(f"{country}.png", "rb")}
    requests.post(url, files=files)

countries = {"us": "english", "mx": "spanish", "de": "german"}

for k, v in countries.items():
    json_data = get_news(k)
    df = create_df(json_data)
    stop_words = set(stopwords.words(v))
    stop_words.add('said')
    wordcloud_plot(df, stop_words, k)
    post_telegram(k)
