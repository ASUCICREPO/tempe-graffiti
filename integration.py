from threading import Thread
import os
import shutil
import random
import subprocess



def send_to_RabbitMQ(): 
    command = r"C:/Users/cic/anaconda3/envs/cic_tempe/python.exe c:/Users/cic/Projects/tempe-graffiti/report_graffiti.py"
    print(command)
    proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    out,err = proc.communicate()

def capture_image_from_camera():
    command = r"C:/Users/cic/anaconda3/envs/cic_tempe/python.exe c:/Users/cic/Projects/tempe-graffiti/Image_Capture_ML.py &"
    print(command)
    proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    out,err = proc.communicate()

Thread(target = capture_image_from_camera).start()
Thread(target = send_to_RabbitMQ).start()