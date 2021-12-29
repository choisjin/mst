#-*- coding:utf-8 -*-
import rospy
from std_msgs.msg import Int64MultiArray
import Adafruit_PCA9685 

pwm = Adafruit_PCA9685.PCA9685() 
pwm.set_pwm_freq(60) 

midScreenX = 640/2    # 화면 x축 중앙
midScreenY = 480/2    # 화면 y축 중앙
midScreenWindow = 40  # 객체를 인식한 사각형이 중앙에서 벗어날 수 있는 여유 값

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
        self._sub_x = rospy.Subscriber('/servo_x3', Int64MultiArray, self.callback, queue_size=1) # 객체인식 바운딩박스 x,y,w,h 토픽
        self.servo_x = 320   # servo_x defalt position
        self.servo_y = 390
        pwm.set_pwm(1, 0, self.servo_x)
        pwm.set_pwm(0, 0, self.servo_y)
    
    def callback(self,servo_msg):
        x = servo_msg.data[0]
        y = servo_msg.data[1]
        w = servo_msg.data[2]
        h = servo_msg.data[3]
        
        self.servo_x1 = int(x+w/2)
        self.servo_y1 = int(y+h/2)
               
        if self.servo_x1 < midScreenX-midScreenWindow:
            self.servo_x += 1    
            pwm.set_pwm(1, 0, self.servo_x)
  
        elif self.servo_x1 > midScreenX+midScreenWindow:
            self.servo_x -= 1
            pwm.set_pwm(1, 0, self.servo_x)  
                        
        if self.servo_y1 > midScreenY+midScreenWindow:
            self.servo_y += 1
            pwm.set_pwm(0, 0, self.servo_y) 

        elif self.servo_y1 < midScreenY-midScreenWindow:
            self.servo_y -= 1
            pwm.set_pwm(0, 0, self.servo_y)      
     
    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('Servo_Move')
    node = Servo_Subscriber()
    node.main()