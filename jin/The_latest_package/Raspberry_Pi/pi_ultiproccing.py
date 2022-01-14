#-*- coding:utf-8 -*-
import rospy, cv2, Adafruit_PCA9685 
from std_msgs.msg import UInt16MultiArray, Int8MultiArray, Int8
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from multiprocessing import Process

global Camera_number
Camera_number = '1'

midScreenX = 320/2    # 화면 x축 중앙
midScreenY = 240/2    # 화면 y축 중앙
midScreenWindow = 17  # 객체를 인식한 사각형이 중앙에서 벗어날 수 있는 여유 값

pwm = Adafruit_PCA9685.PCA9685() 
pwm.set_pwm_freq(60) 

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

class Cam_Publisher():
    def __call__(self):
        cap = cv2.VideoCapture(0)               
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 20)    
        
        rospy.init_node("cam_pub", anonymous=True)
        image_pub = rospy.Publisher("cam_num%s" % Camera_number, Image, queue_size=1)

        bridge = CvBridge()

        while not rospy.is_shutdown():
            ret, cv_image = cap.read()
            image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))

        cap.release()
        cv2.destroyAllWindows()

class Servo_Subscriber():
    def __call__(self):
        rospy.init_node('servo_subs', anonymous=True)
        
        self.Servo_subs = rospy.Subscriber('/servo_controller_%s' % Camera_number, UInt16MultiArray, self.callback, queue_size=1)
        
        self.servo_x = 320
        self.servo_y = 390
        pwm.set_pwm(1, 0, self.servo_x)
        pwm.set_pwm(0, 0, self.servo_y)
        
        self.manual_checker = 0    
        
        rospy.spin()
   
    def callback(self, servo_msg):
        self.manual_check_subs = rospy.Subscriber('/manual%s_check' % Camera_number, Int8, self.callback_checker, queue_size=1)

        if self.manual_checker == 1:
            self.manual_subs = rospy.Subscriber('/manual%s_axis' % Camera_number,  UInt16MultiArray, self.callback_manual_axis, queue_size=1)

        elif self.manual_checker == 0:        
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
    
            servo_axis_pub = rospy.Publisher('servo%s_axis' % Camera_number,  UInt16MultiArray, queue_size=1)
            servo_axis_msg = UInt16MultiArray()
            servo_axis_msg.data = [self.servo_x, self.servo_y]
            servo_axis_pub.publish(servo_axis_msg)
        
    def callback_checker(self, check_msg):
        self.manual_checker = check_msg.data
    
    def callback_manual_axis(self, axis_msg):
        self.servo_x = axis_msg.data[0]
        self.servo_y = axis_msg.data[1]

class Manual_Subscriber():
    def __call__(self): 
        self.manual_checker = 0
        rospy.init_node('manual_subs', anonymous=True)
        self.Manual_subs = rospy.Subscriber('/manual_control_%s' % Camera_number,  Int8MultiArray, self.callback_manual, queue_size=1)
        self.servo_subs = rospy.Subscriber('/servo%s_axis' % Camera_number,  UInt16MultiArray, self.callback_servo_axis, queue_size=1)
        rospy.spin()

    def callback_manual(self, manual_msg): 
        self.manual_check_subs = rospy.Subscriber('/manual%s_check' % Camera_number, Int8, self.callback_checker, queue_size=1)

        x = manual_msg.data[0]
        y = manual_msg.data[1]    
        self.servo_x1 = x
        self.servo_y1 = y
        
        if self.servo_x1 == 1:
            self.servo_x += 1
            pwm.set_pwm(1, 0, self.servo_x)
        elif self.servo_x1 == -1:
            self.servo_x -= 1
            pwm.set_pwm(1, 0, self.servo_x)
        elif self.servo_y1 == 1:
            self.servo_y -= 1
            pwm.set_pwm(0, 0, self.servo_y)
        elif self.servo_y1 == -1:
            self.servo_y += 1
            pwm.set_pwm(0, 0, self.servo_y)
        
        manual_axis_pub = rospy.Publisher('manual%s_axis' % Camera_number,  UInt16MultiArray, queue_size=1)
        manual_axis_msg =  UInt16MultiArray()
        manual_axis_msg.data = [self.servo_x, self.servo_y]
        manual_axis_pub.publish(manual_axis_msg)

    def callback_checker(self, check_msg):
        self.manual_checker = check_msg.data

    def callback_servo_axis(self, axis_msg):
        self.servo_x = axis_msg.data[0]
        self.servo_y = axis_msg.data[1]

try:    
    p1 = Process(target = Cam_Publisher())      # Cam_data Publisher
    p2 = Process(target = Servo_Subscriber())   # Tracking_data Subscriber
    p3 = Process(target = Manual_Subscriber())  # Manual_control_data Subscriber

    p1.start()
    p2.start()
    p3.start()

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    p1.join()
    p2.join()
    p3.join()

    print("exit program")