#!/bin/bash
# script to exit immediately if any command exits with a non-zero status (indicating an error).
set -e

# Export kaggle.json to os env for Kaggle authentication
KAGGLE_JSON_PATH="./project/kaggle.json"
KAGGLE_CONFIG_DIR=$(dirname "$KAGGLE_JSON_PATH")
export KAGGLE_CONFIG_DIR

#Install required packages
pip install --upgrade pip
pip install -r ./project/requirements.txt

# Run testcase updates
pytest ./project/tests/test_pipeline.py