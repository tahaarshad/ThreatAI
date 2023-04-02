import csv
import shlex


import sys

if len(sys.argv) != 2:
    print("Usage: python modified_script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

def parse_commands(input_str):
    commands = []
    lexer = shlex.shlex(input_str)
    lexer.wordchars += "|>"
    while True:
        token = lexer.get_token()
        if not token:
            break
        if token == "|":
            continue
        else:
            command = []
            command.append(token)
            while True:
                next_token = lexer.get_token()
                lexer.push_token(next_token)
                if not next_token or next_token == "|":
                    break 
                else:
                    parameter = lexer.get_token()
                    command.append(parameter)
            commands.append(command)
    return commands

# Read the entire input file into memory
input_data = []
with open(input_file, "r") as infile:
    reader = csv.reader(infile)
    for row in reader:
        input_data.append(row)

# Modify the input data in memory
modified_data = []
header_row = input_data.pop(0)
modified_data.append(header_row)
for row in input_data:
    if row:
        if not row[-1]:
            row[-1] = "None"
        input_str = row[7]
        if input_str:
            commands = parse_commands(input_str)
            for command in commands:
                output_row = [
                    row[0],   # session
                    row[1],   # eventid
                    row[2],   # src_ip
                    row[3],   # destfile
                    row[4],   # username
                    row[5],   # password
                    row[6],   # timestamp
                    command[0]  # command
                ]
                modified_data.append(output_row)
        else:
            row[-1] = ''
            modified_data.append(row)

# Write the modified data back to the input file
with open(input_file, "w", newline='') as infile:
    writer = csv.writer(infile)
    writer.writerows(modified_data)
