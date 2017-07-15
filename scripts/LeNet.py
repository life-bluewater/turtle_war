#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L


class LeNet(chainer.Chain):

    def __init__(self):
        super(LeNet, self).__init__(
            conv1=F.Convolution2D(3, 20, 5),
            conv2=F.Convolution2D(20, 50, 5),
            fc3=F.Linear(None, 500),
            fc4=F.Linear(500, 10)
        )
        self.train = True

    def __call__(self, x, t):
        h = F.max_pooling_2d(model.conv1(x), 2, stride=2)
        h = F.max_pooling_2d(model.conv2(h), 2, stride=2)
        h = F.relu(model.fc3(h))
        h = self.fc4(h)

        self.loss = F.softmax_cross_entropy(h, t)
        self.accuracy = F.accuracy(h, t)

        if self.train:
            return self.loss
        else:
            self.pred = F.softmax(h)
            return self.pred

model = LeNet()
