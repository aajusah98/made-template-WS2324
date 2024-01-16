# Sentiment Analysis for Financial News And Tweets 

## Overview
This project aims to leverage sentiment analysis techniques to analyze financial news articles and social media posts for their impact on stock price movements. By employing Natural Language Processing (NLP) and machine learning algorithms, we aim to determine if sentiment scores from textual data can be used as a predictive signal for trading decisions. This research has the potential to provide valuable insights for investors and traders.

## Technologies Used
- **Python**: Data analysis and visualization are performed using Python programming language.
- **Pandas**: For data manipulation and analysis.
- **sqlite3**: For creating databse
- **Matplotlib and Seaborn**: Used for creating visualizations to better understand the trends.
- **Kaggle API**: Utilized for accessing the dataset.


## Kaggle Authentication
To access the dataset from Kaggle, follow these steps:

1. Go to [Kaggle Account Settings](https://www.kaggle.com/settings).
2. Download your Kaggle API key as a `kaggle.json` file.
3. Place the `kaggle.json` file inside the `/project/` directory.

**Filepath:** `/project/kaggle.json`

```
{
  "username":"a*****h",
  "key":"3a2b***********************25"
}
```

## Set Execute Permissions for the Pipeline Script
Before running the analysis pipeline, ensure that the pipeline script has execute permissions. Run the following command:

```bash
chmod +x ./project/pipeline.sh
```
## Run the Analysis Pipeline
Navigate to the project directory and execute the pipeline script:

```bash
cd project && ./pipeline.sh
```

## Set Execute Permissions for the Test Pipeline Script
If you want to run the test pipeline, grant execute permissions to the test script:

```bash
chmod +x ./project/tests.sh
```

## Run the Test Pipeline
Navigate to the project directory and execute the test script:

```bash
cd project && ./tests.sh
```

## Analysis Report
Explore the detailed analysis report [here](https://github.com/aajusah98/made-template-WS2324/blob/main/project/report.ipynb).
