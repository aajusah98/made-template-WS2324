import pandas as pd
import sqlite3
import os
from nltk.corpus import stopwords
import nltk
import re
import string
from kaggle.api.kaggle_api_extended import KaggleApi

# Function to download and extract a Kaggle dataset and rename CSV files
def download_and_extract_kaggle_dataset(dataset_name, extraction_path, new_csv_name):
    # Set up Kaggle API
    api = KaggleApi()
    api.authenticate() 

    # Create the destination folder if it doesn't exist
    os.makedirs(extraction_path, exist_ok=True)
    
    # Download the dataset
    api.dataset_download_files(dataset_name, extraction_path, unzip=True)

    # Rename CSV file(s)
    return rename_csv_files(extraction_path, new_csv_name)

# Function to rename CSV files in a directory
def rename_csv_files(extraction_path, new_csv_name):
    # List all files in the extraction folder
    files = os.listdir(extraction_path)
    
    # Iterate through files and rename CSV files
    for file_name in files:
        if file_name.endswith('.csv'):
            # Full path to the current file
            current_file_path = os.path.join(extraction_path, file_name)

            # Full path to the new file
            new_file_path = os.path.join(extraction_path, new_csv_name)

            # Rename the file
            os.rename(current_file_path, new_file_path)
            
    return new_file_path 

# Download NLTK stopwords
nltk.download('stopwords')

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

# Remove Punctuations
exclude = string.punctuation
def remove_punc(text):
    return text.translate(str.maketrans('', '', exclude))

# --------------------------------------------End::Text Cleaning Function------------------------


# Function to fetch and clean Financial News Dataset
def fetch_and_clean_financial_news():
    dataset_name = 'ankurzing/sentiment-analysis-for-financial-news'
    extraction_path = './data_set/sentiment-analysis-for-financial-news'
    new_csv_name = 'financial-news.csv'
    
    file_path = download_and_extract_kaggle_dataset(dataset_name, extraction_path, new_csv_name)
    
    if os.path.isfile(file_path):
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=',', encoding='latin-1')
        # Rename columns
        df.columns = ['Sentiment', 'Sentence']
        # Convert text to lowercase
        df["Sentence"] = df["Sentence"].str.lower()
        # Remove punctuation
        df['Sentence'] = df['Sentence'].apply(lambda x: remove_punc(x))
        # Remove numbers
        df["Sentence"] = df["Sentence"].str.replace('r"\d+"', "")
        # Remove newline characters
        df["Sentence"] = df["Sentence"].str.replace("\n", "").replace("\r", "")
        # Remove URLs, HTML tags, and handle emojis
        df['Sentence'] = df['Sentence'].apply(lambda x: remove_url(x))
        df['Sentence'] = df['Sentence'].apply(lambda x: remove_html_tags(x))
        df['Sentence'] = df['Sentence'].apply(lambda x: handel_emoji(x))
        # Map sentiment labels to integers
        df["Sentiment"] = df["Sentiment"].map({"positive": 1, "negative": 0, "neutral": 2})
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        df['Sentence'] = df['Sentence'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
        df.dropna()  # Remove missing values
        # Store the cleaned data in an SQLite database
        conn = sqlite3.connect('../data/financial_news.sqlite')
        df.to_sql('financial_news', conn, index=False, if_exists='replace', dtype={'Sentiment': 'INTEGER', 'Sentence': 'TEXT'})
        conn.close()
        print("Database Created And stored at /data/financial_news.sqlite")
    else:
        print(f"File not found: {file_path}")

# Function to fetch and clean Twitter Sentiment Analysis Dataset
def fetch_and_clean_twitter_sentiment():
    dataset_name = 'kazanova/sentiment140'
    extraction_path = './data_set/sentiment-twitter'
    new_csv_name = 'twitter-data.csv'
    
    file_path = download_and_extract_kaggle_dataset(dataset_name, extraction_path, new_csv_name)
    
    if os.path.isfile(file_path):
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path, delimiter=',', encoding='latin-1')
        # Rename columns and select relevant columns
        df.columns = ['target', 'ids', 'date', 'flag', 'user', 'text']
        df = df[['text', 'target']]
        # Replace target values (4 -> 1 for positive)
        df['target'] = df['target'].replace(4, 1)
        # Convert text to lowercase
        df["text"] = df["text"].str.lower()
        # Remove punctuation, numbers, URLs, HTML tags, and handle emojis
        df['text'] = df['text'].apply(lambda x: remove_punc(x))
        df["text"] = df["text"].str.replace('r"\d+"', "")
        df['text'] = df['text'].apply(lambda x: remove_url(x))
        df['text'] = df['text'].apply(lambda x: remove_html_tags(x))
        df['text'] = df['text'].apply(lambda x: handel_emoji(x))
        df["text"] = df["text"].str.replace("\n", "").replace("\r", "")
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        df['text'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
        df.dropna()  # Remove missing values
        # Store the cleaned data in an SQLite database
        conn = sqlite3.connect('../data/twitter_sentiment.sqlite')
        df.to_sql('twitter_sentiment', conn, index=False, if_exists='replace', dtype={'text': 'TEXT', 'target': 'INTEGER'})
        conn.close()
        print("Database Created And stored at /data/twitter_sentiment.sqlite")
    else:
        print(f"File not found: {file_path}")

# Main function
def main():
    # Create the /data directory if it doesn't exist
    if not os.path.exists('../data'):
        os.makedirs('../data')
    if not os.path.exists('./data_set'):
        os.makedirs('./data_set')
    # Fetch and clean Financial News and Twitter Sentiment datasets
    fetch_and_clean_financial_news()
    fetch_and_clean_twitter_sentiment()

if __name__ == "__main__":
    main()    

