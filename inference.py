import mxnet as mx
import cv2
import numpy as np
from mxnet.io import DataBatch
from os import listdir,chdir,remove
from os.path import abspath,dirname,join,basename,expanduser
from operator import itemgetter
from shutil import move
import time
# the digit denotes the epoch (starts with 0) which had best result on val set
net = mx.mod.Module.load('./image-classification', 17)
image_l = 224
image_w = 224
net.bind(for_training=False, data_shapes=[('data', (1, 3, image_l, image_w))], label_shapes=net._label_shapes)

def get_image(fname, show=False):
    img = cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB)
    if img is None:
        return None
    # convert into format (batch, RGB, width, height)
    img = cv2.resize(img, (image_l, image_w))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img
def predict(url):
    # global net
    img = get_image(url, show=False)
    # compute the predict probabilities
    net.forward(DataBatch([mx.nd.array(img)]))
    prob = net.get_outputs()[0].asnumpy()
    prob = np.squeeze(prob)
    classes = np.argsort(prob)[::-1]
    index, value = max(enumerate(prob), key=itemgetter(1))
    return labels[index]


g = 'graffiti'
ng = 'notgraffiti'
labels = [g, ng]
images_dir = expanduser("~/captured") # 'C://cic//tempe-graffiti//sagemaker-graffiti-images//classified_copy//graffiti' 
graffiti_dir = expanduser("~/graffiti") #'C://cic//tempe-graffiti//sagemaker-graffiti-images//testinference' 
time_taken = 0
try:
    while True:
        images = listdir(images_dir)
        if images:
            for image in images:
                abs_path = join(images_dir,image)
                prediction = predict(abs_path)
                if prediction is g:
                    try:
                        move(abs_path, graffiti_dir)
                    except Exception as err:
                        print(err, "\ncould not move image to graffiti dir",image)
                else:
                    try:
                        # move(abs_path, images_dir)
                        remove(abs_path)
                    except Exception as err:
                        print(err,"\ncould not remove image from captured dir",image)
        else:
            time.sleep(10)
except KeyboardInterrupt:
    print("EXIT PROGRAM")
