import pandas as pd
from sqlalchemy import create_engine
import re


# Fetch the CSV data from the provided URL
data_set_url='https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'

# Read CSV data into a pandas DataFrame
df = pd.read_csv(data_set_url, delimiter=';')

# Drop the "Status" column
df = df.drop(columns=['Status'])

# Define validation functions
def is_valid_verkehr(value):
    return value in ["FV", "RV", "nur DPN"]

def is_valid_coordinate(value):
    try:
        # Replace comma with dot and convert to float
        numeric_value = float(value.replace(',', '.'))
        return -90 <= numeric_value <= 90
    except (ValueError, TypeError):
        return False

def is_valid_ifopt(value):
    # Regular expression pattern for IFOPT validation
    pattern = re.compile(r"^\w{2}:\d+:\d+(?::\d+)?$")
    return bool(pattern.match(str(value)))

# Apply data validation and filtering
df = df[df['Verkehr'].apply(is_valid_verkehr)]
df = df[df['Laenge'].apply(is_valid_coordinate)]
df = df[df['Breite'].apply(is_valid_coordinate)]
df = df[df['IFOPT'].apply(is_valid_ifopt)]
df = df.dropna()  # Drop rows with empty cells

# print(df['Laenge'])
# sys.exit()
# Define column data types
column_types = {
    "EVA_NR": int,
    "DS100": str,
    "IFOPT": str,
    "NAME": str,
    "Verkehr": str,
    "Laenge": str,
    "Breite": str,
    "Betreiber_Name": str,
    "Betreiber_Nr": int
}

# Connect to SQLite database
# conn = sqlite3.connect('exercises/trainstops.sqlite')
conn=create_engine("sqlite:///trainstops.sqlite", echo=True)

df = df.astype(column_types)
# Write the DataFrame to SQLite database
df.to_sql('trainstops', conn, if_exists='replace',index=False)

# Close the database connection


print("DONE")