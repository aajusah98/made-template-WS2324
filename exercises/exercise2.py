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

# print(df.dtypes)
# sys.exit()
# Define column data types
column_types = {
    "EVA_NR": "BIGINT",
    "DS100": "TEXT",
    "IFOPT": "TEXT",
    "NAME": "TEXT",
    "Verkehr": "TEXT",
    "Laenge": "FLOAT",
    "Breite": "FLOAT",
    "Betreiber_Name": "TEXT",
    "Betreiber_Nr": "BIGINT"
}

# Connect to SQLite database
# conn = sqlite3.connect('exercises/trainstops.sqlite')
conn=create_engine("sqlite:///exercises/trainstops.sqlite", echo=True)


# Write the DataFrame to SQLite database
df.to_sql('trainstops', conn, if_exists='replace',index=False , dtype=column_types)

# Close the database connection
# conn.close()

print("DONE")