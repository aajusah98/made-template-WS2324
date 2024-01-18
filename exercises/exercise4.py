import pandas as pd
import zipfile
import urllib.request
from sqlalchemy import create_engine

#               ***Data Fetching***
url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
path = "mowesta-dataset-20221107.zip"
urllib.request.urlretrieve(url, path)

#               ***Extracting***
with zipfile.ZipFile(path, 'r') as zip_ref:
    zip_ref.extractall('mowesta-dataset-20221107')


#               ***Data Reading***
df = pd.read_csv("./mowesta-dataset-20221107/data.csv", delimiter=";", decimal=",", index_col=False, 
                 usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"])

#               ***Columns Renaming***
df = df.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C": "Batterietemperatur"})

#               ***Data Transformation (C To F)***
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

# Convert temperatures to Fahrenheit
df["Temperatur"] = celsius_to_fahrenheit(df["Temperatur"])
df["Batterietemperatur"] = celsius_to_fahrenheit(df["Batterietemperatur"])

#               ***Validation***
column_types = {
    'Geraet': int,
    'Hersteller': str,
    'Model': str,
    'Monat': int,
    'Temperatur': float,
    'Batterietemperatur': float,
    'Geraet aktiv': str
}
df = df.astype(column_types)

# Write to SQLite database
df.to_sql('temperatures', 'sqlite:///temperatures.sqlite', if_exists='replace', index=False)