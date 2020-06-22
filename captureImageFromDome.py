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




capture = cv2.VideoCapture('rtsp://root:asucic2020@192.168.0.17/live.sdp')
img_counter=0
frame_rate = 8
prev = 0
while True:
    time_elapsed = time.time() - prev
    graffiti_dir = os.path.expanduser("~\\Projects\\tempe-graffiti\\graffiti") # 'C://cic//tempe-graffiti//sagemaker-graffiti-images//testinference' # 
    ret, frame = capture.read()
    if time_elapsed > 1./frame_rate:
        prev = time.time()
        img_name = "opencv_frame_"+datetime.now().strftime("%d_%b_%Y_%H_%M_%S.%f)")+"{}.png".format(img_counter)
        cv2.imwrite(os.path.join(graffiti_dir ,img_name), frame)
        print("{} written!".format(img_name))
        img_counter += 1


        

capture.release()
cv2.destroyAllWindows()