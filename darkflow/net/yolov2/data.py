from ...utils.pascal_voc_clean_xml import pascal_voc_clean_xml
from numpy.random import permutation as perm
from ..yolo.predict import preprocess
from ..yolo.data import shuffle
from copy import deepcopy
import pickle
import numpy as np
import os, os.path
import xml.etree.ElementTree as et
import subprocess
import json
import csv

row = 1

def _batch(self, chunk):
    """
    Takes a chunk of parsed annotations
    returns value for placeholders of net's 
    input & loss layer correspond to this chunk
    """
    meta = self.meta
    labels = meta['labels']
    
    H, W, _ = meta['out_size']
    C, B = meta['classes'], meta['num']
    anchors = meta['anchors']

    # preprocess
    jpg = chunk[0]; w, h, allobj_ = chunk[1]
    allobj = deepcopy(allobj_)
    path = os.path.join(self.FLAGS.dataset, jpg)
    print (jpg)
    print (len([name for name in os.listdir('/home/ubuntu/Documents/darkflow-master/ckpt')])) 
    #if len([name for name in os.listdir('/home/ubuntu/Documents/darkflow-master/ckpt')]) > 4:
    xml_name = jpg.split('.')[0] + '.xml'
    xml_file = et.parse('/home/ubuntu/Documents/darkflow-master/annotations_r/' + xml_name).getroot()
    if len(xml_file) == 5:
        subprocess.call(['cp','/home/ubuntu/Documents/darkflow-master/images/test/'+jpg,'/home/ubuntu/Documents/darkflow-master/test/out/'])
    
    img = self.preprocess(path, allobj)

    # Calculate regression target
    cellx = 1. * w / W
    celly = 1. * h / H
    for obj in allobj:
        centerx = .5*(obj[1]+obj[3]) #xmin, xmax
        centery = .5*(obj[2]+obj[4]) #ymin, ymax
        cx = centerx / cellx
        cy = centery / celly
        if cx >= W or cy >= H: return None, None
        obj[3] = float(obj[3]-obj[1]) / w
        obj[4] = float(obj[4]-obj[2]) / h
        obj[3] = np.sqrt(obj[3])
        obj[4] = np.sqrt(obj[4])
        obj[1] = cx - np.floor(cx) # centerx
        obj[2] = cy - np.floor(cy) # centery
        obj += [int(np.floor(cy) * W + np.floor(cx))]

    # show(im, allobj, S, w, h, cellx, celly) # unit test

    # Calculate placeholders' values
    probs = np.zeros([H*W,B,C])
    confs = np.zeros([H*W,B])
    coord = np.zeros([H*W,B,4])
    proid = np.zeros([H*W,B,C])
    prear = np.zeros([H*W,4])
    for obj in allobj:
        probs[obj[5], :, :] = [[0.]*C] * B
        probs[obj[5], :, labels.index(obj[0])] = 1.
        proid[obj[5], :, :] = [[1.]*C] * B
        coord[obj[5], :, :] = [obj[1:5]] * B
        prear[obj[5],0] = obj[1] - obj[3]**2 * .5 * W # xleft
        prear[obj[5],1] = obj[2] - obj[4]**2 * .5 * H # yup
        prear[obj[5],2] = obj[1] + obj[3]**2 * .5 * W # xright
        prear[obj[5],3] = obj[2] + obj[4]**2 * .5 * H # ybot
        confs[obj[5], :] = [1.] * B

    # Finalise the placeholders' values
    upleft   = np.expand_dims(prear[:,0:2], 1)
    botright = np.expand_dims(prear[:,2:4], 1)
    wh = botright - upleft; 
    area = wh[:,:,0] * wh[:,:,1]
    upleft   = np.concatenate([upleft] * B, 1)
    botright = np.concatenate([botright] * B, 1)
    areas = np.concatenate([area] * B, 1)

    # value for placeholder at input layer
    inp_feed_val = img
    # value for placeholder at loss layer 
    loss_feed_val = {
        'probs': probs, 'confs': confs, 
        'coord': coord, 'proid': proid,
        'areas': areas, 'upleft': upleft, 
        'botright': botright
    }

    return inp_feed_val, loss_feed_val

def check_iou():
    csvfile = open('check.csv','a')
    csvwriter = csv.writer(csvfile)
    subprocess.call(['/home/ubuntu/Documents/darkflow-master/flow','--imgdir','/home/ubuntu/Documents/darkflow-master/test/out','--model','/home/ubuntu/Documents/darkflow-master/cfg/tiny-yolo-voc-1c.cfg','--load','-1','--json'])
    for image in os.scandir('/home/ubuntu/Documents/darkflow-master/test/out'):
        if '.' in image.name:
            data = json.load(open('/home/ubuntu/Documents/darkflow-master/test/out/out/'+image.name.split('.')[0]+'.json'))
            xml_file = et.parse('/home/ubuntu/Documents/darkflow-master/annotations_r/' + image.name.split('.')[0]+'.xml').getroot()
            csvrow = [image.name]
            print (csvrow)
            if len(data) > 0:
                csvrow.append(xml_file[4][4][0].text)
                csvrow.append(xml_file[4][4][1].text)
                csvrow.append(xml_file[4][4][2].text)
                csvrow.append(xml_file[4][4][3].text)
                csvrow.append(data[0]['topleft']['x'])
                csvrow.append(data[0]['topleft']['y'])
                csvrow.append(data[0]['bottomright']['x'])
                csvrow.append(data[0]['bottomright']['y'])
            csvwriter.writerow(csvrow)
            print (csvrow)
            subprocess.call(['rm','/home/ubuntu/Documents/darkflow-master/test/out/'+image.name])
            subprocess.call(['rm','/home/ubuntu/Documents/darkflow-master/test/out/out/'+image.name.split('.')[0]+'.json'])
    csvfile.close()   