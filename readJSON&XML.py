import os, os.path
import xml.etree.ElementTree as et
import subprocess
import json
import csv

csvfile = open('check.csv','a')
csvwriter = csv.writer(csvfile)
for image in os.scandir('17mar-combined/images'):
    if '.' in image.name:
        data = json.load(open('17mar-combined/images/out/'+image.name.split('.')[0]+'.json'))
        xml_file = et.parse('17mar-combined/annotations/' + image.name.split('.')[0]+'.xml').getroot()
        csvrow = [image.name]
        print (csvrow)
        csvrow.append(xml_file[4][4][0].text)
        csvrow.append(xml_file[4][4][1].text)
        csvrow.append(xml_file[4][4][2].text)
        csvrow.append(xml_file[4][4][3].text)
        if len(data) > 0:
            csvrow.append(data[0]['topleft']['x'])
            csvrow.append(data[0]['topleft']['y'])
            csvrow.append(data[0]['bottomright']['x'])
            csvrow.append(data[0]['bottomright']['y'])
        else:
            csvrow.append(0)
            csvrow.append(0)
            csvrow.append(0)
            csvrow.append(0)
        csvwriter.writerow(csvrow)
        print (csvrow)
csvfile.close()