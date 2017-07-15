#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
How to run：
Multi Layer Perceptron
>> python test.py --model MLP.py
Deep Convolutional Neural Network
>> python test.py --model LeNet.py
GPU mode
>> python test.py --gpu 0
'''

import argparse
import imp
import numpy as np
import os
import cv2
import chainer

from os import path
from chainer import cuda
from chainer import serializers
from chainer import Variable

class LenetRecog():
    def __init__(self, homedir = './'):
        self.homedir = homedir
        self.model = self.get_model()
        self.model.train = False

    def get_model(self, model_ = 'LeNet.py', test_model = 'epoch-30.model'):
        '''
        optimizer(最適化方法)の指定
        '''
        model_fn = os.path.basename(model_)
        print(self.homedir+model_)
        model = imp.load_source(model_fn.split('.')[0], self.homedir + model_).model
        serializers.load_hdf5(self.homedir + test_model, model)

        return model

    def recog(self, img):

        img = np.asarray(img, dtype=np.float32)
        # cpuの場合はnumpy配列で計算
        xp = np 
        x = img.reshape((1,3,28,28))
        x /= 255.
        t = np.asarray([0], dtype=np.int32)
        volatile = 'off'
        x = Variable(xp.asarray(x), volatile=volatile)
        t = Variable(xp.asarray(t), volatile=volatile)
        pred = self.model(x, t).data
        pred = pred.mean(axis=0)
        #print(pred.argmax() )
        #print(pred)

        return pred.argmax()

