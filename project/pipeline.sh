#!/bin/bash


# Install required packages from requirements.txt
pip install --upgrade pip
pip install -r ./project/requirements.txt

# Run your Python file
python3 ./project/pipeline.py