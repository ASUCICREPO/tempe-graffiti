Steps to create Rec file:
—————————————
exampleDir is the name of the directory in the current folder path
Create lst file - python im2rec.py ./fileName ./exampleDir/ --recursive --list --num-thread 8
Create rec file - python im2rec.py ./fileName ./exampleDir/ --recursive --pass-through --pack-label --num-thread 8

Command 1. creates a .lst object
Command 2. creates a .rec file using the .lst object

Unzip tag.gz file on mac/linux:
-------------------------------
tar xf model_25_Feb.tar.gz 

# from cic dir
python .\rec\im2rec.py ./rec/tempe-graffiti-train .\sagemaker-graffiti-images\Train\ --recursive --list --num-thread 8
python .\rec\im2rec.py ./rec/tempe-graffiti-train .\sagemaker-graffiti-images\Train\ --recursive --pass-through --pack-label --num-thread 8