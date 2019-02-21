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
from flask_restful import Resource, Api
from werkzeug import secure_filename
import ast

options = {
    'model': 'cfg/tiny-yolo-voc-1c.cfg',
    'load': 27625,
    'threshold': 0.1,
}
options2 = {
    'model': 'cfg/tiny-yolo-voc-2c.cfg',
    'load': 15600,
    'threshold': 0.1,
}
tfnet = TFNet(options)
tfnet2 = TFNet(options2)

app = Flask(__name__)
api=Api(app)


class JSON(Resource):
    def post(self):
        file = request.files['img']
        file_name = "frames/"+file.filename
        file.save(file_name)
        imgcv = cv2.imread(file_name)
        results = tfnet.return_predict(imgcv)
        results2 = tfnet2.return_predict(imgcv)
        if len(results2) > 0:
            results2[0]['label'] = 'TV'
        # r = ri.stdout.read()
        # r2 = ri2.stdout.read()
        # r = r.replace("[","")
        # r = r.replace("]","")
        # r = r.replace('"','')
        # r2 = r2.replace("[","")
        # r2 = r2.replace("]","")
        # r2 = r2.replace('"','')
        # results = ast.literal_eval(r)
        # results2 = ast.literal_eval(r2)
        print (results)
        print (type(results))
        print (results2)
        print (type(results2))
        if len(results) != 0 and len(results2) != 0:
            if float(results[0]['confidence']) >= float(results2[0]['confidence']):
                return str(results)
            else:
                return str(results2)
        elif len(results) == 0:
            return str(results2)
        elif len(results2) == 0:
            return str(results)
        else:
            return str(results)


api.add_resource(JSON, '/json')

if __name__ == "__main__":
    app.run(host='localhost', debug=True)