import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from generate_xml_self import write_xml
import json
from pprint import pprint

# global constants
img = None
tl_list = []
br_list = []
object_list = []

# constants
image_folder = 'test/out'
savedir = 'annotations/test'
obj = 'split_AC'


def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(obj)


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'y':
        data = json.load(open('test/json/' + img.name.replace('jpg', 'json')))
        for i in range(len(data)):
            tl_list.append((int(data[i]['topleft']['x']),int(data[i]['topleft']['y'])))
            br_list.append((int(data[i]['bottomright']['x']),int(data[i]['bottomright']['y'])))
            object_list.append(obj)
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close()
            
    
    elif event.key == 'n':
        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress_2)
    elif event.key == 'd':
            os.remove(img.path)
            tl_list = []
            br_list = []
            object_list = []
            img = None
            plt.close()

def onkeypress_2(event):
    global object_list
    global tl_list
    global br_list
    global img   

    if event.key == 'q':
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close()
    elif event.key == 'd':
        os.remove(img.path)
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close()
    elif event.key == 'u':
        tl_list = []
        br_list = []
        object_list = []



def toggle_selector(event):
    toggle_selector.RS.set_active(True)


if __name__ == '__main__':
    for n, image_file in enumerate(os.scandir(image_folder)):
        img = image_file
        print (img.name)
        fig, ax = plt.subplots(1)
        mngr = plt.get_current_fig_manager()
        #mngr.window.wm_geometry(250, 120, 1280, 1024)
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)

        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            drawtype='box', useblit=True,
            button=[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True
        )
        key = plt.connect('key_press_event', onkeypress)
        plt.show()