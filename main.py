# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:20:16 2021

@author: edmond
"""

from csv import reader
import os.path
import sys
import matplotlib.pyplot as plt
import JsonTest


def CheckValidPoint(d_x, d_y):
    result = False
    if (X_and_Y):
        if (d_x >= ThresholdX) and (d_y >= ThresholdY):
            result = True
    else:        
        if (d_x >= ThresholdX) or (d_y >= ThresholdY):
            result = True
    return result
        


#----------------------------------------------------------

""" read/write confifuration file """

d = JsonTest.ReadConfig("configure.json")
ThresholdX = d.setdefault("ThresholdX", "1")
ThresholdY = d.setdefault("ThresholdY", "1")
x_margin = d.setdefault("x_margin", "0")
y_margin = d.setdefault("y_margin", "0")
x_size = d.setdefault("x_size", "240")
y_size = d.setdefault("y_size", "240")
X_and_Y = d.setdefault("X_and_Y", True)


print("Threshold X: {}, Threshold Y: {}".format(ThresholdX, ThresholdY))
print("Margin X: {}, Margin Y: {}".format(x_margin, y_margin))
print("Size X: {}, Size Y: {}".format(x_size, y_size))
x_size = x_size - 1
y_size = y_size - 1


map_size_x = x_size - x_margin * 2
map_size_y = y_size - y_margin * 2
latitude_column = 6
longitude_column = 7
max_x = max_y = -1
min_x = min_y = 100000
last_x = last_y = -100

version = float(d.setdefault("version", "1.00"))


#----------------------------------------------------------
""" optimize the track """

filename = input("Please input filename (csv):")
# filename = "GPS_20210207_1109"
# filename = "GPS_20210326_1435"
# filename = "GPS_20210328_1207"


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
    y = float(row[latitude_column])
    x = float(row[longitude_column])

    if (x > max_x) and (x != 200):
        max_x = x

    if (x < min_x) and (x != 200):
        min_x = x

    if (y > max_y) and (y != 200):
        max_y = y

    if (y < min_y) and (y != 200):
        min_y = y

delta_x = round(max_x - min_x, 10)
delta_y = round(max_y - min_y, 10)
if(delta_x > delta_y):
    scale = map_size_x / delta_x
else:
    scale = map_size_y / delta_y
length_x = round(scale * delta_x)
length_y = round(scale * delta_y)
print("Max X: {}, Min X: {}".format(max_x, min_x))
print("Max Y: {}, Min Y: {}".format(max_y, min_y))
print("length_x: {}, length_y: {}".format(length_x, length_y))



file_out = filename + "_out.csv"
new_array = []
with open(file_out, 'w') as write_obj:
    for row in list_of_rows:
        y = float(row[latitude_column])
        x = float(row[longitude_column])
        if ((x != 200) and (y != 200)):
            # x = (round(((x - min_x) / delta_x)*map_size_x))
            # y = (round(((y - min_y) / delta_y)*map_size_y))
            x = round((x - min_x) * scale)
            y = round((y - min_y) * scale)

            # if (1):
            if (CheckValidPoint(abs(x-last_x), abs(y - last_y))):
                last_x = x
                last_y = y
                plot_x = x + round(x_margin + (map_size_x - length_x)/2)
                plot_y = y + round(y_margin + (map_size_y - length_y)/2)
                write_obj.write(str(plot_x) + "," +
                                str(plot_y) + '\n')
                new_array.append([plot_x, plot_y])
print("New row size = ", len(new_array))

#----------------------------------------------------------
""" PLot the map """

for n in range(0, len(new_array)-2):
    x1 = new_array[n][0] 
    x2 = new_array[n+1][0] 
    y1 = new_array[n][1] 
    y2 = new_array[n+1][1] 
    y_values = [y1, y2]
    x_values = [x1, x2]
    # print(x_values, y_values)
    plt.plot(x_values, y_values)

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 10,
        }


if (X_and_Y):
    tempStr = "and"    
else:
    tempStr = "or"

# file_out = filename + ".jpg"
file_out = filename + "_"  + str(ThresholdX) + tempStr + str(ThresholdY) + ".jpg"
plt.title(filename, fontsize=10)
plt.grid(True)
plt.text(10, 10, "total segment: " +str(len(new_array)), fontdict = font)
plt.text(10, 30, "X:" +str(ThresholdX) + " " + tempStr + " Y:" +str(ThresholdY), fontdict = font)
plt.axis('scaled')
plt.xlim(0, x_size)
plt.ylim(0, y_size)
plt.savefig(file_out, dpi=300)


# just a little bit modification on the main.py

        
        
        
    