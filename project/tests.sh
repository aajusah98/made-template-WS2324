#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Export kaggle.json to os env for Kaggle authentication
KAGGLE_JSON_PATH="./project/kaggle.json"
KAGGLE_CONFIG_DIR=$(dirname "$KAGGLE_JSON_PATH")
export KAGGLE_CONFIG_DIR

# Install required packages from requirements.txt
pip install --upgrade pip
pip install -r ./project/requirements.txt

# Run test case update
pytest ./project/tests/test_pipeline.py

##run project-testing.yml trigger workflow
##kaggle json test

