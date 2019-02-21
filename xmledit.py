import os
import xml.etree.ElementTree as xml

def updateXML(filename):
    tree = xml.ElementTree(file=filename)
    root = tree.getroot()

    for folder in root.iter("folder"):
        folder.text = 'images'
 
    tree = xml.ElementTree(root)
    with open(xml_file_path, "wb") as fh:
        tree.write(fh)

if __name__ == "__main__":
    source_directory = 'annotations'

    for filename in os.listdir(source_directory):
        
        if not filename.endswith('.xml'):
            continue

        xml_file_path = os.path.join(source_directory, filename)
        updateXML(xml_file_path)