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
net = mx.mod.Module.load('./image-classification', 17)
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
    img = cv2.resize(img, (224, 224))
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
    #     f.write(','.join([url, str(end_time - start_time),""]))
    return labels[index], value,prob[0],prob[1],(end_time - start_time)


g = 'graffiti'
ng = 'notgraffiti'
labels = [g, ng]
true_pos , true_neg , false_pos , false_neg  = 0,0,0,0
# flags to check one sample of each category
# get test files from directory ../sagemaker-graffiti-images/test/*
# test_dir = join(dirname(abspath(__file__)),'sagemaker-graffiti-images','image-classification-transfer-learning','test')

print("Welcome to Graffiti Image Classification")
print("1-View the Model's Precision ")
print("2-Image Prediction")
val=input("Press 1 or 2 \n")

while True:
    if val=="1":
        test_dir = join(dirname(abspath(__file__)),'sagemaker-graffiti-images','split','test')
        false_pos_list,false_neg_list = [],[]
        time_taken = 0
        for root, dirs, files in walk(test_dir):
            actual_class = basename(root)
            # print("folder: ",actual_class,"Number of images: %s" %len(files))
            for file in files:
                abs_path = join(root,file)
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
        with open(("errors/wrong_classification_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+".csv"),"w+") as f:
            f.write("False Negatives,graffiti,notgraffiti")
            for line in false_neg_list:
                f.write(line)
            f.write("")
            f.write("False Positives,graffiti,notgraffiti")
            for line in false_pos_list:
                f.write(line)
        precision = (true_pos/(true_pos+false_pos))*100
        recall = (true_pos/(true_pos+false_neg))*100
        f1_score = (2*precision*recall)/(precision+recall)
        print("","true_pos: " , true_pos , "\ntrue_neg: ", true_neg , "\nfalse_pos: ", false_pos , "\nfalse_neg: ", false_neg)
        print("\nprecision: ",precision,"\nrecall: ", recall)
        print("\nAvg Time_taken:", time_taken/(true_pos+true_neg+false_neg+false_pos),"\n")
    if(val=="2"):
        test_dir = join(dirname(abspath(__file__)),'sagemaker-graffiti-images','google','testing')
        false_pos_list,false_neg_list = [],[]
        time_taken = 0
        for root, dirs, files in walk(test_dir):
            actual_class = basename(root)
            # print("folder: ",actual_class,"Number of images: %s" %len(files))
            for file in files:
                abs_path = join(root,file)
                print("--------------------------------------------------")
                print("File: ",abs_path)
                prediction, confidence, pg, png, tme = predict(abs_path)
                print("Prediction: ",prediction)
        print("")
    print("1-View the Model's Precision ")
    print("2-Image Prediction")
    val=input("Press 1 or 2 \n")





print("EXIT PROGRAM")
