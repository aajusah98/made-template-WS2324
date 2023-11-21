import pandas as pd
import sqlite3
import os
from nltk.corpus import stopwords
import nltk
import re
import string

# ---------------------------Start::Text cleaning functions-------------------------------
# Remove HTML Tags
def remove_html_tags(text):
    pattern = re.compile('<.*?>')
    return pattern.sub(r'', text)

# Remove URLs
def remove_url(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return pattern.sub(r'', text)

# Handling Emojis

# Defining dictionary containing all emojis with their meanings.
emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed',
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink',
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

def handel_emoji(text):
    for emoji in emojis.keys():
        text = text.replace(emoji, "EMOJI" + emojis[emoji])

    return text

# Remove Punctiations
exclude = string.punctuation
def remove_punc(text):
    return text.translate(str.maketrans('', '', exclude))


# --------------------------------------------End::Text Cleaning Function------------------------

# Download NLTK stopwords
nltk.download('stopwords')

# Function to fetch and clean Financial News Dataset
def fetch_and_clean_financial_news():
    # The dataset contains two columns, "Sentiment" and "News Headline(Sentence)". The sentiment can be negative, neutral or positive.
    file_path = 'project\\data_set\\sentiment-analysis-for-financial-news\\all-data.csv'
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path, delimiter=',',encoding='latin-1')
        df.columns=['Sentiment','Sentence'] #renaming column name
        df["Sentence"]=df["Sentence"].str.lower() #Convert the texts to lowercase.
        df['Sentence'] = df['Sentence'].apply(lambda x: remove_punc(x)) #Remove punctuation marks from the texts.
        df["Sentence"]=df["Sentence"].str.replace("\d+","") #Removing numbers from our texts.
        df["Sentence"]=df["Sentence"].str.replace("\n","").replace("\r","") #Remove spaces in our texts.
        df['Sentence'] = df['Sentence'].apply(lambda x: remove_url(x)) #remove urls
        df['Sentence'] = df['Sentence'].apply(lambda x: remove_html_tags(x)) #remove html tags
        df['Sentence'] = df['Sentence'].apply(lambda x: handel_emoji(x)) #handle emoji
        df_neutral=df[df['Sentiment']=="neutral"]
        df_positive=df[df['Sentiment']=="positive"]
        df_negative=df[df['Sentiment']=="negative"]
        
        df["Sentiment"]=df["Sentiment"].map({"positive":1,"negative":0,"neutral":2})
        
        # Clean and preprocess the textual data (remove stopwords)
        stop_words = set(stopwords.words('english'))
        df['Sentence'] = df['Sentence'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
        df.dropna() # Removing Missing Values from Data Frames
        
        # Store the cleaned data in an SQLite database
        conn = sqlite3.connect('./data/financial_news.db')
        df.to_sql('financial_news', conn, index=False, if_exists='replace')
        conn.close()
        print("Database Created And stored at /data/financial_news.db")
    else:
        print(f"File not found: {file_path}")

# Function to fetch and clean Twitter Sentiment Analysis Dataset
def fetch_and_clean_twitter_sentiment():
    
    # It contains the following 6 fields:
    # target: the polarity of the tweet (0 = negative, 2 = neutral, 4 = positive)
    # ids: The id of the tweet ( 2087)    
    # date: the date of the tweet (Sat May 16 23:58:44 UTC 2009)
    # flag: The query (lyx). If there is no query, then this value is NO_QUERY.
    # user: the user that tweeted (robotickilldozr)
    # text: the text of the tweet (Lyx is cool)
    
    file_path = 'project\\data_set\\sentiment_twiter\\twiter_data.csv'

    if os.path.isfile(file_path):
        df = pd.read_csv(file_path, delimiter=',',encoding='latin-1')
        df.columns=['target','ids','date','flag','user','text'] #renaming column name
        df = df[['text', 'target']] #dropping unnecessary columns
        df['target'] = df['target'].replace(4,1) #4 = positive replaed to 1=postive
        
        df["text"]=df["text"].str.lower() #Convert the texts to lowercase.
        df['text'] = df['text'].apply(lambda x: remove_punc(x)) #Remove punctuation marks from the texts.
        df["text"]=df["text"].str.replace("\d+","") #Removing numbers from our texts.
        df['text'] = df['text'].apply(lambda x: remove_url(x)) #remove urls
        df['text'] = df['text'].apply(lambda x: remove_html_tags(x)) #remove html tags
        df['text'] = df['text'].apply(lambda x: handel_emoji(x)) #handle emoji
        df["text"]=df["text"].str.replace("\n","").replace("\r","") #Remove spaces in our texts.
        
        # Clean and preprocess the textual data (remove stopwords)
        stop_words = set(stopwords.words('english'))
        df['text'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
        df.dropna() # Removing Missing Values from Data Frames
        
        #  Store the cleaned data in an SQLite database
        conn = sqlite3.connect('./data/twitter_sentiment.db')
        df.to_sql('twitter_sentiment', conn, index=False, if_exists='replace')
        conn.close()
        print("Database Created And stored at /data/twitter_sentiment.db")
    else:
        print(f"File not found: {file_path}")


def main():
    fetch_and_clean_financial_news()
    fetch_and_clean_twitter_sentiment()

if __name__ == "__main__":
    main()