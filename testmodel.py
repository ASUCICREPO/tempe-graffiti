import mxnet as mx
import matplotlib.pyplot as plot
import cv2
import numpy as np
from mxnet.io import DataBatch
import time
import boto3
from os import listdir,chdir
from os.path import abspath,dirname,join

net = mx.mod.Module.load('./image-classification', 8)
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


def predict(url, labels):
    start_time = time.time()

    img = get_image(url, show=False)
    # compute the predict probabilities
    net.forward(DataBatch([mx.nd.array(img)]))
    # net.forward(list([mx.nd.array(img)]))
    prob = net.get_outputs()[0].asnumpy()

    # print the top-5
    prob = np.squeeze(prob)
    a = np.argsort(prob)[::-1]

    print("Total size of the features = %s" %(len(a)))
    for i in a[0:5]:
        print('probability=%f, label=%s' % (prob[i], labels[i]))

    # print('probability of graffiti=%f, i=%s' % (prob[0], labels[0]))
    # print('probability of non-graffiti=%f, i=%s' % (prob[1], labels[1]))
    end_time = time.time()
    print("Total execution time: {} seconds".format(end_time - start_time))


labels = ['graffiti', 'not_graffiti']
chdir(join(dirname(dirname(abspath(__file__))),'sagemaker-graffiti-images','001.graffiti'))
for file in listdir('.'):
    predict(abspath(file),labels)

print("EXIT PROGRAM")