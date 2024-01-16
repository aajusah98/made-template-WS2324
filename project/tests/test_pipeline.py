# test_pipeline.py

import os
import sqlite3
import pandas as pd
import pytest

from pipeline import fetch_and_clean_financial_news, fetch_and_clean_twitter_sentiment


def test_fetch_and_clean_financial_news():
    fetch_and_clean_financial_news()

    # Check if the SQLite database is created
    assert os.path.isfile('../data/financial_news.sqlite')

    # Check if the database has the 'financial_news' table
    conn = sqlite3.connect('../data/financial_news.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('financial_news',) in tables

    # Check if the 'financial_news' table has some rows
    df = pd.read_sql_query("SELECT * FROM financial_news;", conn)
    assert not df.empty
    conn.close()

def test_fetch_and_clean_twitter_sentiment():
    fetch_and_clean_twitter_sentiment()

    # Check if the SQLite database is created
    assert os.path.isfile('../data/twitter_sentiment.sqlite')

    # Check if the database has the 'twitter_sentiment' table
    conn = sqlite3.connect('../data/twitter_sentiment.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('twitter_sentiment',) in tables

    # Check if the 'twitter_sentiment' table has some rows
    df = pd.read_sql_query("SELECT * FROM twitter_sentiment;", conn)
    assert not df.empty
    conn.close()
