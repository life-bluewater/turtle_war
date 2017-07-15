#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class Convert:
    def __init__(self):
        self.n = 0
        self.label = 5

        self.bridge = CvBridge()

        self.vel_pub = rospy.Subscriber('/mobile_base/commands/velocity', Twist,self.twistCallback)

        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.imageCallback)

    def twistCallback(self, data):
        x = data.linear.x
        z = data.angular.z
        if z >  0.5 :
            self.label = 4
        elif z < -0.5 :
            self.label = 6
        elif x > 0.4 :
            self.label = 8
        elif x < -0.3 :
            self.label = 2
        else:
            self.label = 5
        pass

    def imageCallback(self, data):
        if self.label == 5:
            print("label = 5")
            return

        try:
            im_raw = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        im_resize = cv2.resize(im_raw,(28,28))

        im_id = ("00000000" + str(self.n))[-6:]
        img_name = "./img/" + str(self.label) + "_" + im_id+".png"

        cv2.imwrite(img_name, im_resize)
        print("saveimage " + img_name)

        self.n += 1
        pass


if __name__ == '__main__':
    rospy.init_node('bag2img')

    cc = Convert()

    rospy.spin()

