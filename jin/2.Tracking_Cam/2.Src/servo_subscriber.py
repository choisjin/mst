#-*- coding:utf-8 -*-
import sys
import rospy
import cv2
from std_msgs.msg import Int64
#import time
import Adafruit_PCA9685 

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm = Adafruit_PCA9685.PCA9685() 
pwm.set_pwm_freq(60) 

class Servo_Subscriber():
    def __init__(self):
        self._sub_x = rospy.Subscriber('/servo_x3', Int64, self.callback, queue_size=1)
        self._sub_y = rospy.Subscriber('/servo_y3', Int64, self.callback, queue_size=1)
    
    def callback(self,servo_msg):
        sub_x=self._sub_x.data
        sub_y=self._sub_y.data
        #self._sub_y=int(self._sub_y)
        print(sub_x)
        print(sub_y)
        #print(type(sub_x))        
        #pwm.set_pwm(1, 0, sub_x)
    
    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('Servo_Move')
    node = Servo_Subscriber()
    node.main()