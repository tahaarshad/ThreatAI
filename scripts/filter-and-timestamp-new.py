import csv
import pandas as pd
from datetime import datetime

import sys

if len(sys.argv) != 2:
    print("Usage: python modified_script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

# Define the allowed event IDs
allowed_eventids = ['cowrie.command.input', 'cowrie.login.failed', 'cowrie.login.success', 'cowrie.session.file_download']

# Read the input file into a DataFrame
# input_file = 'cowrie copy 2.csv'
df = pd.read_csv(input_file)

# Filter the DataFrame based on allowed event IDs and non-empty rows
df = df[df['eventid'].isin(allowed_eventids) & df.apply(lambda x: any(x.str.strip()), axis=1)]

# Write the filtered DataFrame back to the input file
df.to_csv(input_file, index=False)

# Define a function to parse the timestamp and extract the desired information
def parse_timestamp(timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.hour, dt.date(), dt.day, dt.month

# Apply the function to the timestamp column and create new columns
df[["hour", "date", "day", "month"]] = df["timestamp"].apply(lambda x: pd.Series(parse_timestamp(x)))

# Delete the original timestamp column
df = df.drop("timestamp", axis=1)

# Save the modified dataset
df.to_csv(input_file, index=False)
