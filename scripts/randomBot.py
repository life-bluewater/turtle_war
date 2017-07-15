#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random
import time

from abstractBot import *
from geometry_msgs.msg import Twist

class RandomBot(AbstractBot):
    
    def strategy(self):
        r = rospy.Rate(100)
        
        target_speed = 0
        target_turn = 0
        control_speed = 0
        control_turn = 0

        surplus = 0

        UPDATE_FREQUENCY = 1
        update_time = 0

        while not rospy.is_shutdown():            
            if time.time() - update_time > UPDATE_FREQUENCY:
                if self.left_bumper:
					update_time = time.time()
	                rospy.loginfo('turn left!!')
	                x = -0.5
	                th = 3
	            elif self.right_bumper:
	                update_time = time.time()
	                rospy.loginfo('turn right!!')
	                x = -0.5   
	                th = -3
                pass
            else:
                update_time = time.time()                
                rospy.loginfo('free!!')
                x = 1       
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

if __name__ == '__main__':
    rospy.init_node('random_bot')
    bot = RandomBot('Random')
    bot.strategy()
