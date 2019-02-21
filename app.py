from __future__ import print_function
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
from flask_uploads import UploadSet, configure_uploads
import sys
import json
from darkflow.net.build import TFNet
import cv2
from io import BytesIO
import time
from PIL import Image
import numpy as np

options = {
    'model': 'cfg/tiny-yolo-voc-1c.cfg',
    'load': 27625,
    'threshold': 0.1,
}

tfnet = TFNet(options)

app = Flask(__name__)

files = UploadSet('files')
app.config['UPLOADED_FILES_DEST'] = 'frames'
configure_uploads(app, files)

@app.route('/', methods=['POST'])
def events():
	filename = files.save(request.files['file'])
	filename = "frames/"+filename
	imgcv = cv2.imread(filename)
	results = tfnet.return_predict(imgcv)
	print(results)
	with open('data.json', 'w') as outfile:
		outfile.write(str(results))
	return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)