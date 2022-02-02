import json
from operator import is_
from posixpath import split
import re
# from tabnanny import check
# import tkinter as tk
# from tkinter.filedialog import askopenfilename
import os
from tabnanny import check
import time
import csv
import sys
import getopt

# Set initial variables
orgText = ''
newText = ''
checked_arg = ''
location_info = ''


def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", [
            "help", "directory=", "file="])
    except getopt.GetoptError:
        print('Usage: test.py --file <filename> or --directory <directory path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('')
            print(
                '#######################################################################################')
            print(
                '#                 Synchronoss Search Warrant Return .JSON Cleaner                     #')
            print(
                '#######################################################################################')
            print('')
            print('# This program is intended to clean up the returned data returned from chat application \"Synchronoss\" and export it into a proper JSON and CSV format.')
            print('# This program can be ran from the main directory without arguments, or can receive arguments that note a specific file or directory.')
            print('')
            print('When ran without arguments, the script will search it\'s parent directory for any ".json" file and try to parse it')
            print('# Usage: test.py')
            print('')
            print(
                'When a single file is passed, the program will only attempt to parse that one file.')
            print(
                'If the filename has spaces in it, please place quotations around the name.')
            print('# Usage: test.py --file \"<filename>\"')
            print('')
            print('When a directory is passed, it will search that specific dirctory for any ".json" file and attempt to parse those files.')
            print(
                'If the directory path has spaces in it, please place quotations around the entire path.')
            print('# Usage: test.py --directory \"<directory path>\"')
            print('')
        elif opt in ("--file"):
            print("File provided as argument: ", arg)
            return arg
        elif opt in ("--directory"):
            print("Directory provided as argument: ", arg)
            return arg
        else:
            assert False, "Unhandled Option"


def check_args(arg):
    errors = 0
    # print(arg)
    cwd = os.getcwd()
    # print(type(cwd))
    full_file_path = str(cwd) + '\\' + str(arg)
    # print(os.path.isfile(full_file_path))
    if os.path.isfile(full_file_path) != False:
        is_file = 'File'
        return is_file, full_file_path, errors
    elif os.path.isdir(arg) != False:
        is_dir = 'Directory'
        return is_dir, arg, errors
    else:
        errors = 1
        return arg, '', errors


def get_JSON_File(user_arg, full_file_name):
    split_file = os.path.splitext(user_arg)
    # print(split_file)

    file_name = split_file[0]  # Set filename to variable
    file_ext = split_file[1]  # Set file extension to variable
    # print(file_name)
    # print(file_ext)

    if file_ext == '.json':
        file = open(user_arg, 'r')  # Open file
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


def export_Converted_JSON(conv_text, file_loc):
    # print(file_loc)
    path = os.path.dirname(os.path.abspath(file_loc))
    # print(path)
    folder = 'Converted_Data'
    join_path = os.path.join(path, folder)
    # print(join_path)
    if os.path.isdir(join_path):
        pass
    else:
        os.mkdir(join_path)
    save_fname = 'converted_data'
    save_loc = os.path.join(join_path, save_fname+".json")
    # print(save_loc)
    if os.path.isfile(save_loc):
        print('Can not create file, as folder Converted_Data already containes a converted_data.json file')
        return False
    else:
        with open(save_loc, 'w') as outfile:
            outfile.write(conv_text)
        outfile.close()
        return True


# def write_converted_JSON():
#     return True

###########################
# Begin Main Body Of Code #
###########################

passed_arg = get_args()
# print('Passed arg: {}'.format(passed_arg))
if str(passed_arg) != 'None':
    checked_arg, location_info, errors = check_args(passed_arg)
    if errors == 1:
        print('You provided {}, which did not show to be a valid file or directory.'.format(
            checked_arg))
        print('Please try again...')
        time.sleep(3)
else:
    print('You provided no arguemnts. Scanning current directory of this script for JSON files...')
    time.sleep(3)

if checked_arg == 'File':
    print('Time to load, read and process the File....')
    orgText, fname, fext = get_JSON_File(passed_arg, location_info)
    # print(orgText)
    print('File successfully loaded. Time to remove unwanted \"u\"characters and change all \' to \"')
    convertText = format_to_JSON(orgText)
    # print(convertText)
    print('Successfully changed characters and returned proper JSON format')
    print('Preparting to export formatted data to \"Converted_data.json\"....')
    status = export_Converted_JSON(convertText, location_info)
    if status != False:
        print('File created successfully!')
    else:
        print('There was an error while creating file. Please try again...')
        time.sleep(3)
        sys.exti()
elif checked_arg == 'Directory':
    print('Time to scan entire directory provided by user')
else:
    print('Scanning cwd of python file')

# print(checked_arg)
# print(location_info)
# print(errors)

# # Examples to get current working directory of file
# print("Path at terminal when executing this file")
# print(os.getcwd() + "\n")

# print("This file path, relative to os.getcwd()")
# print(__file__ + "\n")

# print("This file full path (following symlinks)")
# full_path = os.path.realpath(__file__)
# print(full_path + "\n")

# print("This file directory and name")
# path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")

# print("This file directory only")
# print(os.path.dirname(full_path))

# jsonText = json.loads(newText)
# print(jsonText.keys())

# print(jsonText["received"])
# print(jsonText["sender"])
# print(jsonText["body"])

# print(fname)
# print(fext)
