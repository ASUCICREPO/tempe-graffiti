import cv2
import numpy as np
import os
import time
from datetime import datetime
import mxnet as mx
import matplotlib.pyplot as plot
import cv2
import numpy as np
from mxnet.io import DataBatch
import boto3
from os import listdir,chdir,walk
from os.path import abspath,dirname,join,basename
import operator
import os
import shutil
import random
import subprocess

import glob

net = mx.mod.Module.load('./image-classification', 17)
image_l = 224
image_w = 224
net.bind(for_training=False, data_shapes=[('data', (1, 3, image_l, image_w))], label_shapes=net._label_shapes)

def get_image(img, show=False):
    # download and show the image
    # try:
    #     fname = mx.test_utils.download(url)
    # except:
    #     fname = mx.test_utils.download(fname=url)
    if img is None:
        return None
    if show:
        plot.imshow(img)
        plot.axis('off')
        plot.show()
    # convert into format (batch, RGB, width, height)
    img = cv2.resize(img, (224, 224))
    img = np.swapaxes(img, 0, 2)
    # cv2.imwrite('compressed.png', img)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img

def predict(original_image):
    # global net
    start_time = time.time()


    img = get_image(original_image, show=False)
    # compute the predict probabilities
    net.forward(DataBatch([mx.nd.array(img)]))
    # net.forward(list([mx.nd.array(img)]))
    prob = net.get_outputs()[0].asnumpy()
    # print the top-2
    prob = np.squeeze(prob)
    classes = np.argsort(prob)[::-1]

    # print("Total size of the features = %s" %(len(classes)))
    index, value = max(enumerate(prob), key=operator.itemgetter(1))

    # for i in classes:
        # print('probability=%f, label=%s' % (prob[i], labels[i]))

    end_time = time.time()
    # print("Total execution time: {} seconds".format(end_time - start_time))

    # with open(("errors/classification_time.csv"),"a") as f:
    #     f.write(','.join([url, str(end_time - start_time),""]))
    return labels[index], value,prob[0],prob[1],(end_time - start_time)

g = 'graffiti'
ng = 'notgraffiti'
labels = [g, ng]
true_pos , true_neg , false_pos , false_neg  = 0,0,0,0


flag=0
capture = cv2.VideoCapture('rtsp://root:asucic2020@169.254.172.31/live.sdp')
img_counter=0
frame_rate = 5
prev = 0
while True:
    time_elapsed = time.time() - prev
    graffiti_dir = os.path.expanduser("~\\Projects\\tempe-graffiti\\graffiti") # 'C://cic//tempe-graffiti//sagemaker-graffiti-images//testinference' # 
    ret, frame = capture.read()
    if time_elapsed > 1./frame_rate:
        prev = time.time()
        prediction, confidence, pg, png, tme = predict(frame)
        print(prediction)
        if prediction == g and flag==0:
            flag=1
            img_name = "opencv_frame_"+datetime.now().strftime("%d_%b_%Y_%H_%M_%S.%f)")+"{}.png".format(img_counter)
            cv2.imwrite(os.path.join(graffiti_dir ,img_name), frame)
            print("{} written!".format(img_name))
            img_counter += 1
        else:
            if prediction == ng:
                flag=0
            


        

capture.release()
cv2.destroyAllWindows()