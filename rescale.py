import os
import shutil
import random
import subprocess
import glob
from skimage.transform import resize
from os.path import abspath,dirname,join,basename
import imageio
import numpy as np
from skimage import img_as_ubyte


proj_dir = os.path.dirname(os.path.abspath(__file__))
s3_dir = os.path.join(proj_dir,'sagemaker-graffiti-images')
dataset_dir = os.path.join(s3_dir ,'classified')
resized_dir = os.path.join(s3_dir ,'resized')
if os.path.exists(resized_dir):
    os.rename(resized_dir,str(resized_dir+"_bkp"))
os.makedirs(resized_dir)
classes = os.listdir(dataset_dir)
for _class in classes:
    os.makedirs(os.path.join(resized_dir,_class))

for root, dirs, files in os.walk(dataset_dir):
    actual_class = basename(root)
    print("\nfolder: ",actual_class)
    print("\nNumber of images: %s\n" %len(files))

    for image in files:
        abs_image = join(root, image)
        # print(abs_image)
        new_image = abs_image.replace('classified','resized')
        try:
            resize_image =  resize(imageio.imread(abs_image), (224,224),
                       anti_aliasing=True)
            imageio.imwrite(new_image, img_as_ubyte(resize_image))#.astype(np.uint8))
        except:
            print(abs_image)

print("\nSaved %s images in %s\n" %len(files) %resized_dir)

    