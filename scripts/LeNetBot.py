#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random
import time
import mnistRecog

from abstractBot import *
from geometry_msgs.msg import Twist

class RandomBot(AbstractBot):

    def imageCallback(self, data):
        try:
            im_raw = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        except CvBridgeError as e:
            print(e)

        im_resize = cv2.resize(im_raw,(28,28))

        ret = self.lr.recog(im_resize)
        speed = 0
        turn = 0

        sign = ''
        if ret == 2:
          speed = -0.4
          turn = 0
          sign = '\|/'
        elif ret == 4:
          speed = 0.4
          turn = 1.
          sign = '<-'
        elif ret == 6:
          speed = 0.4
          turn = -1.
          sign = '->'
        else:
          speed = 0.4
          turn = 0
          sign = '/|\\'

        twist = Twist()
        twist.linear.x = speed; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z =turn 

        self.vel_pub.publish(twist)

        font = cv2.FONT_HERSHEY_PLAIN
        score_color = (0,255,255)
        cv2.putText(im_raw,sign,(250,250),font, 7,score_color)
        cv2.imshow("Image window", im_raw)
        cv2.waitKey(3)

        print(sign)




    def strategy(self):
        return

        r = rospy.Rate(100)
        
        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0

        surplus = 0

        UPDATE_FREQUENCY = 1
        update_time = 0

        while not rospy.is_shutdown():
            if self.center_bumper or self.left_bumper or self.right_bumper:
                update_time = time.time()
                rospy.loginfo('bumper hit!!')
                x = 0
                th = 3
                control_speed = -1
                control_turn = 0
            
            elif time.time() - update_time > UPDATE_FREQUENCY:
                update_time = time.time()
                
                value = random.randint(1,1000)
                if value < 500:
                    x = 1
                    th = 0

                elif value < 750:
                    x = 0
                    th = 3

                elif value < 1000:
                    x = 0
                    th = -3
                else:
                    x = 0
                    th = 0

            target_speed = x
            target_turn = th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            twist = Twist()
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
            #print(twist)
        
            self.vel_pub.publish(twist)

            r.sleep()
    def initLenetRecog(self, home_dir):
        self.lr = mnistRecog.LenetRecog(home_dir)

if __name__ == '__main__':
    rospy.init_node('random_bot')
    home_dir = rospy.get_param('/randomBot/home_dir', './')
    print(home_dir)

    bot = RandomBot('Random')
    bot.initLenetRecog(home_dir)
    #bot.strategy()
    rospy.spin()

