import mxnet as mx
import matplotlib.pyplot as plot
import cv2
import numpy as np
from mxnet.io import DataBatch
import time
import boto3
from os import listdir,chdir,walk
from os.path import abspath,dirname,join,basename
import operator
import datetime
import glob
# the digit denotes the epoch (starts with 0) which had best result on val set
net = mx.mod.Module.load('./image-classification', 19)
image_l = 224
image_w = 224
net.bind(for_training=False, data_shapes=[('data', (1, 3, image_l, image_w))], label_shapes=net._label_shapes)

def get_image(fname, show=False):
    # download and show the image
    # try:
    #     fname = mx.test_utils.download(url)
    # except:
    #     fname = mx.test_utils.download(fname=url)
    img = cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB)
    if img is None:
        return None
    if show:
        plot.imshow(img)
        plot.axis('off')
        plot.show()
    # convert into format (batch, RGB, width, height)
    img = cv2.resize(img, (180, 320))
    img = np.swapaxes(img, 0, 2)
    # cv2.imwrite('compressed.png', img)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img


def predict(url):
    # global net
    start_time = time.time()

    img = get_image(url, show=False)
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
    #     f.write(','.join([url, str(end_time - start_time),"\n"]))
    return labels[index], value,prob[0],prob[1],end_time


g = 'graffiti'
ng = 'notgraffiti'
labels = [g, ng]
true_pos , true_neg , false_pos , false_neg  = 0,0,0,0
# flags to check one sample of each category
# get test files from directory ../sagemaker-graffiti-images/test/*
# test_dir = join(dirname(abspath(__file__)),'sagemaker-graffiti-images','image-classification-transfer-learning','test')
test_dir = join(dirname(abspath(__file__)),'sagemaker-graffiti-images','split','test')
# print("\ntestdir",test_dir)
false_pos_list,false_neg_list = [],[]
time_taken = 0
for root, dirs, files in walk(test_dir):
    actual_class = basename(root)
    # print("\nfolder: ",actual_class,"Number of images: %s\n" %len(files))
    for file in files:
        abs_path = join(root,file)
        # print("File: ",abs_path)
        prediction, confidence, pg, png, tme = predict(abs_path)
        if prediction == g and actual_class == g:
            true_pos +=1
        elif prediction == ng and actual_class == ng:
            true_neg +=1
        elif prediction == g and actual_class == ng:
            false_pos  +=1
            false_pos_list.append(','.join([abs_path,str(int(pg*100)),str(int(png*100))]))
        elif prediction == ng and actual_class == g:
            false_neg +=1
            false_neg_list.append(','.join([abs_path,str(int(pg*100)),str(int(png*100))]))
        time_taken += tme 
now = datetime.datetime.now()
with open(("wrong_classification_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+".csv"),"w+") as f:
    f.write("False Negatives,graffiti,notgraffiti\n")
    for line in false_neg_list:
        f.write(f"{line}\n")
    f.write("\n")
    f.write("False Positives,graffiti,notgraffiti\n")
    for line in false_pos_list:
        f.write(f"{line}\n")
precision = true_pos/(true_pos+false_pos)
recall = true_pos/(true_pos+false_neg)
f1_score = (2*precision*recall)/(precision+recall)
print("\n","true_pos: " , true_pos , "true_neg: ", true_neg , "false_pos: ", false_pos , "false_neg: ", false_neg)
print("precision: ",precision," recall: ", recall," f1_score: ", f1_score,"\n")
print("Avg Time_taken: ", time_taken/((true_pos)+(true_neg)+(false_neg)+(false_pos)))

print("\nEXIT PROGRAM")