import json
from posixpath import split
import re
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import time

# Set global variables needed to begin program
testData = 'test1.json'
orgText = ''
newText = ''


def get_JSON_File():  # Prompt the user to select the file needed, open the file and get filename
    root = tk.Tk()  # Initiate GUI file selector
    root.withdraw()  # Hide main GUI window
    path = askopenfilename(title="Select Synchronoss JSON File", filetypes=((
        "JSON File", "*.json"), ("All Files", "*.*")))  # Allow user to select JSON file

    full_file_name = os.path.basename(path)  # Get file path from selected file
    # Get just file name and extension
    split_file = os.path.splitext(full_file_name)
    # print(split_file)

    file_name = split_file[0]  # Set filename to variable
    file_ext = split_file[1]  # Set file extension to variable
    # print(file_name)
    # print(file_ext)

    if file_ext == '.json':
        file = open(path, 'r')  # Open file
        text = file.read()  # Read contents of file
        file.close()
        return text, file_name, file_ext
    else:
        print('########################################################################')
        print('You did not select a proper .JSON file extension')
        print(
            'You will need to restart program and select the file return from Synchronoss')
        print('The program will close in 5 seconds...')
        time.sleep(5)
        return False, False, False


def format_to_JSON(text):
    # Check to make sure the specific string (u'') exists in read file
    for m in re.finditer('u\'\'', text):
        # print('Character u\'\''' found at: {}'.format(str(m.span())))
        if len(m.span()) > 0:
            orgText = text.replace('u\'\'', '""')
            # print(orgText)

    # Check to make sure the specific string (u') exists in read file
    for n in re.finditer('u\'', orgText):
        # print('Character u\' found at: {}'.format(str(n.span())))
        if len(n.span()) > 0:
            orgText = orgText.replace('u\'', '"')
            # print(orgText)

    # Check to make sure the specific string (') exists in read file
    for o in re.finditer('\'', orgText):
        # print('Character \' found at: {}'.format(str(o.span())))
        if len(o.span()) > 0:
            orgText = orgText.replace('\'', '"')
            # print(orgText)
    return orgText


def write_converted_JSON():
    return True


# Get data from file selected by user, file name and file ext
orgText, fname, fext = get_JSON_File()
if orgText != False:
    newText = format_to_JSON(orgText)  # Format data and get proper JSON format
else:
    print('')

jsonText = json.loads(newText)
print(jsonText.keys())

print(jsonText["received"])
print(jsonText["sender"])
print(jsonText["body"])

# print(fname)
# print(fext)

# with open('converted_data.json', 'w') as outfile:
#     outfile.write(orgText)
