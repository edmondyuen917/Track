# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 12:30:13 2021

@author: edmond
"""


# Python program to demonstrate
# Conversion of JSON data to
# dictionary


# importing the module
import json
import csv
import os
import sys

# Opening JSON file


def ReadConfig(filename):
    try:
        if not os.path.isfile(filename):
            print("File not exist: ", filename)
            return dict()
        with open(filename) as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("File Not Found Error")


def WriteConfig(d, filename):
    app_json = json.dumps(d)
    with open(filename, "w") as f:
        f.write(app_json)


def dict2csv(filename):
    csv_columns = ['No', 'Name', 'Country']
    dict_data = [
        {'No': 1, 'Name': 'Alex', 'Country': 'India'},
        {'No': 2, 'Name': 'Ben', 'Country': 'USA'},
        {'No': 3, 'Name': 'Shri Ram', 'Country': 'India'},
        {'No': 4, 'Name': 'Smith', 'Country': 'USA'},
        {'No': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
    ]

    try:
        csvfile = filename
        with open(csvfile, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def csv2json(csvFilePath, jsonFilePath):

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # Assuming a column named 'No' to
            # be the primary key
            key = rows['Name']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
