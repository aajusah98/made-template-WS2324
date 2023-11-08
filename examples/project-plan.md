# Project Plan

## Title

<!-- Give your project a short title. -->

Sentiment Analysis for Stock Trading

## Main Question

<!-- Think about one main question you want to answer based on the data. -->

1. Can sentiment analysis of financial news articles and social media posts be used to predict stock price movements?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->

This project aims to leverage sentiment analysis techniques to analyze financial news articles and social media posts for their impact on stock price movements. By employing Natural Language Processing (NLP) and machine learning algorithms, we aim to determine if sentiment scores from textual data can be used as a predictive signal for trading decisions. This research has the potential to provide valuable insights for investors and traders.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Financial News Dataset

- Metadata URL: [Link to metadata](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news)
- Data URL: [Link to dataset](https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news)
- Data Type: CSV

This dataset contains financial news articles labeled with their sentiment (positive, negative, neutral) with respect to the stock market. It will be used to train and test the sentiment analysis model.

### Datasource2: Twitter Sentiment Analysis Dataset

- Metadata URL: [Link to metadata](https://www.kaggle.com/kazanova/sentiment140)
- Data URL: [Link to dataset](https://www.kaggle.com/kazanova/sentiment140)
- Data Type: CSV

While not specifically focused on finance, this dataset contains 1.6 million tweets labeled with sentiments (positive or negative). We will filter tweets related to stock market discussions to supplement the sentiment analysis.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Data Acquisition and Exploration [#1](https://github.com/aajusah98/sentiment-analysis-stock-trading/issues/1)
