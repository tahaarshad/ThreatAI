import gzip
import re
import json
import csv
import shutil

import sys

if len(sys.argv) != 2:
    print("Usage: python modified_script.py <input_file>")
    sys.exit(1)

file_name = sys.argv[1]

# define a function to extract and rename a gz file
def extract_and_rename(file_name):
    # open the gz file in read mode
    with gzip.open(file_name, "rb") as gz_file:
        # read the content as bytes
        content = gz_file.read()

    # define a regular expression to match the .gz extension and any preceding digits
    pattern = r"\d*\.gz"

    # use re.sub to replace the pattern with an empty string
    new_file_name = re.sub(pattern, "", file_name)

    # open the new file in write mode
    with open(new_file_name, "wb") as new_file:
        # write the content to the new file
        new_file.write(content)

    # print a success message
    print(f"Extracted {file_name} and renamed it to {new_file_name}")

    # return the new file name
    return new_file_name

# define a function to overwrite a json file with formatted data
def overwrite_json(file_name):
    with open(file_name, 'r') as f:
        data = f.read().splitlines()

    # Remove any empty lines
    data = list(filter(lambda x: x.strip(), data))

    # Wrap the JSON data with square brackets and add commas
    new_data = '[{}]'.format(','.join(data))

    # Parse the JSON data to ensure it's valid
    json.loads(new_data)

    # Write the new data to the same file
    with open(file_name, 'w') as f:
        f.write(new_data)

    # print a success message
    print(f"Overwritten {file_name} with formatted data")

# define a function to convert a json file to a csv file and keep only the specified columns
def convert_json_to_csv(file_name):
    # specify the columns to keep in the output CSV file
    columns_to_keep = ['session', 'eventid', 'src_ip', 'destfile', 'username', 'password', 'timestamp', 'input']

    # make a backup copy of the original JSON file
    # shutil.copy(file_name, file_name + '.bak')

    # read in the JSON data from the input file
    with open(file_name, 'r') as f:
        data = json.load(f)

    # change the output file name to have a .csv extension
    output_file_name = file_name.replace('.json', '.csv')

    # write the filtered data to the output CSV file
    with open(output_file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # write the header row with the selected column names
        writer.writerow(columns_to_keep)
        
        # iterate over each item in the JSON data and write a row to the CSV file
        for item in data:
            row = [item.get(col, '') for col in columns_to_keep]
            writer.writerow(row)

    # print a success message
    print(f"Converted {file_name} from JSON to CSV and kept only {columns_to_keep}")

# define the original file name
# file_name = "cowrie.json.11.gz"

# call the first function and get the new file name
new_file_name = extract_and_rename(file_name)

# call the second function with the new file name
overwrite_json(new_file_name)

# call the third function with the new file name
convert_json_to_csv(new_file_name)