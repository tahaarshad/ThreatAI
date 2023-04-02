# Assuming the csv file is named data.csv and is in the same directory as this script
import csv
import tempfile


import sys

if len(sys.argv) != 2:
    print("Usage: python modified_script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]


# Open the csv file in read and write mode
with open(input_file, "r+") as infile:
    # Create a csv reader object
    reader = csv.reader(infile)
    # Read the first row as the original headers
    headers = next(reader)
    # Find the index of the input header
    input_index1 = headers.index("input")
    # Change the input header to Commands
    headers[input_index1] = "Commands"
    # Find the index of the input header
    input_index2 = headers.index("session")
    # Change the input header to Commands
    headers[input_index2] = "Session"
    # Create a new list to store the reordered headers
    new_headers = []
    # Append the headers in the desired order
    new_headers.append(headers[input_index2]) # Session
    new_headers.append(headers[1]) # eventid
    new_headers.append(headers[input_index1]) # Commands
    new_headers.append(headers[2]) # src_ip
    new_headers.append(headers[4]) # hour
    new_headers.append(headers[6]) # day
    new_headers.append(headers[7]) # month

    # Create a temporary file object
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
    # Create a csv writer object for the temporary file
    writer = csv.writer(temp_file)
    # Write the new headers as the first row
    writer.writerow(new_headers)
    # Loop through the remaining rows in the original file
    for row in reader:
        # Create a new list to store the reordered row
        new_row = []
        # Append the values in the desired order
        new_row.append(row[input_index2]) # Session
        new_row.append(row[1]) # eventid
        new_row.append(row[input_index1]) # Commands
        new_row.append(row[2]) # src_ip
        new_row.append(row[4]) # hour
        new_row.append(row[6]) # day
        new_row.append(row[7]) # month
        # Write the new row to the temporary file
        writer.writerow(new_row)

# Close both files
infile.close()
temp_file.close()

# Overwrite the original file with the temporary file contents
with open(input_file, "w") as outfile:
    with open(temp_file.name, "r") as infile:
        outfile.write(infile.read())