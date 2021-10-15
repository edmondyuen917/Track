# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:20:16 2021

@author: edmond
"""

from csv import reader
import os.path
import sys

x_offset = y_offset = 0
x_size = y_size = 240 - 1
latitude_column = 6
longitude_column = 7
max_x = max_y = -1
min_x = min_y = 100000
res_x = x_size - x_offset * 2
res_y = y_size - y_offset * 2
last_x = last_y = -1


filename = input("Please input filename (csv):")
file_in = filename + ".csv"

if (os.path.exists(file_in) == False):
    print("File not exist :", file_in)
    sys.exit()


# read csv file as a list of lists
with open(file_in, 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    # print(list_of_rows)
    del list_of_rows[0]             # remove the first row
    print("Raw row = ", len(list_of_rows))

for row in list_of_rows:
    x = float(row[latitude_column])
    y = float(row[longitude_column])

    if (x > max_x) and (x != 200):
        max_x = x

    if (x < min_x) and (x != 200):
        min_x = x

    if (y > max_y) and (y != 200):
        max_y = y

    if (y < min_y) and (y != 200):
        min_y = y




delta_x = max_x - min_x
delta_y = max_y - min_y
print("Max X: {}, Min X: {}".format(max_x, min_x))
print("Max Y: {}, Min Y: {}".format(max_y, min_y))


file_out = filename + "_out.csv"
new_row = 0

with open(file_out, 'w') as write_obj:
    for row in list_of_rows:
        x = float(row[latitude_column])
        y = float(row[longitude_column])
        if ((x != 200) and (y != 200)):
            x = int(((x - min_x) / delta_x)*res_x)
            y = int(((y - min_y) / delta_y)*res_y)
            if ((x != last_x) or (y != last_y)):                # not the same point
                new_row = new_row + 1
                last_x = x
                last_y = y
                write_obj.write(str(y + y_offset) + "," +
                                str(x + x_offset) + '\n')
print("New row 1 = ", new_row)

file_out = filename + "_out2.csv"
new_row = 0
with open(file_out, 'w') as write_obj:
    for row in list_of_rows:
        x = float(row[latitude_column])
        y = float(row[longitude_column])
        if ((x != 200) and (y != 200)):
            x = int(((x - min_x) / delta_x)*res_x)
            y = int(((y - min_y) / delta_y)*res_y)
            # x & y should aprt more than 1
            if ((abs(x - last_x) > 3) and (abs(y - last_y) > 3)):
                new_row = new_row + 1
                last_x = x
                last_y = y
                write_obj.write(str(y + y_offset) + "," +
                                str(x + x_offset) + '\n')
print("New row 2 = ", new_row)