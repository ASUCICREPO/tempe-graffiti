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

net = mx.mod.Module.load('./image-classification', 15)
image_l = 256
image_w = 256
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
    img = cv2.resize(img, (256, 256))
    img = np.swapaxes(img, 0, 2)
    # cv2.imwrite('compressed.png', img)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img


def predict(url):
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
    return labels[index], value


g = 'graffiti'
ng = 'notgraffiti'
labels = [g, ng]
true_pos , true_neg , false_pos , false_neg  = 0,0,0,0
# flags to check one sample of each category
true_pos_flag , true_neg_flag , false_pos_flag , false_neg_flag  = False,False,False,False
_dict = {}
# get test files from directory ../sagemaker-graffiti-images/test/*
test_dir = join(dirname(dirname(abspath(__file__))),'sagemaker-graffiti-images','image-classification-transfer-learning','test')
print("\ntestdir",test_dir)
for root, dirs, files in walk(test_dir):
    actual_class = basename(root)
    print("\nfolder: ",actual_class)
    print("\nNumber of images: %s\n" %len(files))
    for file in files:
        abs_path = join(root,file)
        # print("File: ",abs_path)
        prediction, confidence = predict(abs_path)
        if prediction == actual_class and prediction == g:
            true_pos +=1
            if not true_pos_flag:
                true_pos_flag = True
                print(abs_path, "   Actual: ", actual_class, "   Prediction: ", prediction, "   Confidence", confidence)
        elif prediction == actual_class and prediction == ng:
            true_neg +=1
            if not true_neg_flag:
                true_neg_flag = True
                print(abs_path, "   Actual: ", actual_class, "   Prediction: ", prediction, "   Confidence", confidence)
        elif prediction != actual_class and prediction == ng:
            false_neg +=1
            if not false_neg_flag:
                false_neg_flag = True
                print(abs_path, "   Actual: ", actual_class, "   Prediction: ", prediction, "   Confidence", confidence)
        elif prediction != actual_class and prediction == g:
            false_pos  +=1
            if not false_pos_flag:
                false_pos_flag = True
                print(abs_path, "   Actual: ", actual_class, "   Prediction: ", prediction, "   Confidence", confidence)
        _dict[abs_path] = [prediction == actual_class , prediction , confidence]
precision = true_pos/(true_pos+false_pos)
recall = true_pos/(true_pos+false_neg)
f1_score = (2*precision*recall)/(precision+recall)
print("\n","true_pos: " , true_pos , "true_neg: ", true_neg , "false_pos: ", false_pos , "false_neg: ", false_neg)
print("precision: ",precision," recall: ", recall," f1_score: ", f1_score,"\n")
print("EXIT PROGRAM")