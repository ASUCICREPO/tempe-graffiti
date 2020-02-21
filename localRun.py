import mxnet as mx
import matplotlib.pyplot as plot
import cv2
import numpy as np
from mxnet.io import DataBatch

net = mx.mod.Module.load('./image-classification', 1)
image_l = 64
image_w = 64
net.bind(for_training=False, data_shapes=[('data', (1, 3, image_l, image_w))], label_shapes=net._label_shapes)


def get_image(url, show=False):
    # download and show the image
    fname = mx.test_utils.download(url)
    img = cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB)
    if img is None:
        return None
    if show:
        plot.imshow(img)
        plot.axis('off')
    # convert into format (batch, RGB, width, height)
    img = cv2.resize(img, (64, 64))
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = img[np.newaxis, :]
    return img


def predict(url, labels):
    img = get_image(url, show=True)
    # compute the predict probabilities
    net.forward(DataBatch([mx.nd.array(img)]))
    # net.forward(list([mx.nd.array(img)]))
    prob = net.get_outputs()[0].asnumpy()

    # print the top-5
    prob = np.squeeze(prob)
    a = np.argsort(prob)[::-1]

    for i in a[0:5]:
        print('probability=%f, i=%s' % (prob[i], i))
        # print('probability=%f, class=%s' % (prob[i], labels[i]))

    print('probability of non-graffiti=%f, i=%s' % (prob[1], 1))


labels = ['graffiti', 'not_graffiti']
predict('https://sagemaker-graffiti-images.s3.amazonaws.com/001.graffiti/GraffitiFeature.jpg', labels)