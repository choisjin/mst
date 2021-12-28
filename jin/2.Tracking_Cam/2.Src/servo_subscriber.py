#-*- coding:utf-8 -*-
import sys
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int64
from std_msgs.msg import String
import time
import Adafruit_PCA9685 

pwm = Adafruit_PCA9685.PCA9685() 
pwm.set_pwm_freq(60) 
midScreenX = (640/2)    # screen x mid
midScreenY = (480/2)    # screen y mid
midScreenWindow = 30    # correctio

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

class Servo_Subscriber():
    def __init__(self):
        self._sub_x = rospy.Subscriber('/servo_x3', Int64, self.callback, queue_size=1)
        
        #print(self._sub_x)
        #print(type(self._sub_x))
        # print(int(self._sub_x))
        # print(type(int(self._sub_x)))
    
    def callback(self,servo_msg):
        servo_x = 320   # servo_x defalt position
        servo_y = 390

        for (x,y,w,h) in servo_msg.data:
            servo_x1 = int(x+w/2)
            servo_y1 = int(y+h/2)

            if servo_x1 < midScreenX-midScreenWindow:
                servo_x += 1    
                pwm.set_pwm(1, 0, servo_x)                

            elif servo_x1 > midScreenX+midScreenWindow:
                servo_x -= 1
                pwm.set_pwm(1, 0, servo_x)                                
 
            if servo_y1 > midScreenY+midScreenWindow:
                servo_y += 1
                pwm.set_pwm(0, 0, servo_y)                           

            elif servo_y1 < midScreenY-midScreenWindow:
                servo_y -= 1
                pwm.set_pwm(0, 0, servo_y)      
        #self._sub_y=int(self._sub_y)
                
        #pwm.set_pwm(1, 0, sub_x)
        #pwm.set_pwm(0, 0, int(self._sub_y))
    
    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('Servo_Move')
    node = Servo_Subscriber()
    node.main()