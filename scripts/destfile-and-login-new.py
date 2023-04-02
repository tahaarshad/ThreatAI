import csv
# import os

import sys

if len(sys.argv) != 2:
    print("Usage: python modified_script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

# # Set the input file path
# input_file = 'cowrie copy.csv'

# Read the entire input file into memory
input_data = []
with open(input_file, 'r') as csv_in:
    reader = csv.DictReader(csv_in)
    for row in reader:
        input_data.append(row)

# Modify the input data in memory
fieldnames = ['session', 'eventid', 'src_ip', 'timestamp', 'input']
modified_data = []
for row in input_data:
    if row['destfile']:
        row['input'] = row['destfile']
    if row['username'] or row['password']:
        row['input'] = row['username'] + '/' + row['password']
    del row['destfile']
    del row['username']
    del row['password']
    modified_data.append(row)

# Write the modified data back to the input file
with open(input_file, 'w', newline='') as csv_in:
    writer = csv.DictWriter(csv_in, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(modified_data)
