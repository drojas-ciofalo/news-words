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
	    "X-RapidAPI-Key": "3ce6b87bf8mshce4a5a6a77a9d12p1b2843jsn51183bab967d",
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
    contents = " ".join(df["content"])

    # Create the word cloud image
    word_cloud = WordCloud(background_color='white',
                       stopwords=stop_words,
                       width=800,
                       height=400)

    # Generate the word cloud using the review data
    word_cloud.generate(contents)

    # Display the word cloud
    plt.rcParams["figure.figsize"] = (12, 8)
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("News from "+country.upper())
    plt.show()

countries = {"us": "english", "mx": "spanish", "de": "german"}

for k, v in countries.items():
    json_data = get_news(k)
    df = create_df(json_data)
    stop_words = set(stopwords.words(v))
    wordcloud_plot(df, stop_words, k)
