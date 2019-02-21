import os

for imfile in os.scandir('annotations_r'):
    name = imfile.name.replace('xml','jpg')
    os.rename('images/olx_images_jpg/' + name, 'images/test/' + name)