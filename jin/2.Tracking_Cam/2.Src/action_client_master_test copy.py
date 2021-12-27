#! /usr/bin/env python

from __future__ import print_function
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import actionlib

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import actionlib_tutorials.msg
import Adafruit_PCA9685


servo_x = 320   # servo_x defalt position
servo_y = 390   # servo_y defalt position

pwm = Adafruit_PCA9685.PCA9685() 
#pwm.set_pwm(1, 0, servo_x)  # servo_x positionin itialize
#pwm.set_pwm(0, 0, servo_y)  # servo_y positionin itialize

pwm.set_pwm_freq(60)  

midScreenX = (640/2)    # screen x mid
midScreenY = (480/2)    # screen y mid
midScreenWindow = 35    # correction

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def servo_client():
    while 1:
        if servo_x1 < midScreenX-midScreenWindow:
            servo_x += 1
            pwm.set_pwm(1, 0, servo_x)
        elif servo_x1 > midScreenX+midScreenWindow:
            servo_x -= 1
            pwm.set_pwm(1, 0, servo_x
        if servo_y1 > midScreenY+midScreenWindow:
            servo_y += 1
            pwm.set_pwm(0, 0, servo_y
        elif servo_y1 < midScreenY-midScreenWindow:
            servo_y -= 1
            pwm.set_pwm(0, 0, servo_y)  

    pwm.set_pwm(1, -90, 130) 
    pwm.set_pwm(0, -90, 130) 

def fibonacci_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('fibonacci', actionlib_tutorials.msg.FibonacciAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = actionlib_tutorials.msg.FibonacciGoal(order=20)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('action_client_master_test_py')
        result = servo_client()
    except rospy.ROSInterruptException:
        pass