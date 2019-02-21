import os
import xml.etree.ElementTree

xml_dir = "annotations/"
img_dir = "images/learning"

for img in os.scandir(img_dir):
    try:
        e = xml.etree.ElementTree.parse(xml_dir + img.name[:-4] + "xml").getroot()
    except:
        print (img.name)