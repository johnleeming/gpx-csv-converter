from xml.dom import minidom
import csv
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

input_file = filedialog.askopenfilename(initialdir = "/home/pi/acc_data", title = "Select File to Analyse", )

output_file_name = input_file + '.csv'

with open(input_file, "r") as gpx_in:
    gpx_string = gpx_in.read()

mydoc = minidom.parseString(gpx_string)

trkpt = mydoc.getElementsByTagName("trkpt")
row_list = []

columns = ["timestamp", "latitude", "longitude", "elevation", "cadence"]


# parse trackpoint elements. Search for child elements in each trackpoint so they stay in sync.
for elem in trkpt:
    etimestamp=elem.getElementsByTagName("time")
    timestamp=None
    for selem in etimestamp:
        timestamp=(selem.firstChild.data)

    lat=(elem.attributes["lat"].value)
    lng=(elem.attributes["lon"].value)
    
    eelevation=elem.getElementsByTagName("ele")
    elevation=None
    for selem in eelevation:
        elevation=(selem.firstChild.data)
       
    ecadence=elem.getElementsByTagName("ns3:cad")
    cadence=None
    for selem in ecadence:
        cadence=(selem.firstChild.data)            
    this_row = [timestamp, lat, lng, elevation, cadence]
    row_list.append(this_row)

with open(output_file_name, "x") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(columns)
    writer.writerows(row_list) 
