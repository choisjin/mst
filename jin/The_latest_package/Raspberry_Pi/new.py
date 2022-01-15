#-*- coding:utf-8 -*-
import rospy, cv2, Adafruit_PCA9685 
from std_msgs.msg import UInt16MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
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
        cap = cv2.VideoCapture(1)               
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 30)    
        
        rospy.init_node("cam_pub", anonymous = False)
        image_pub = rospy.Publisher("cam_num%s" % Camera_number, Image, queue_size=1)

        bridge = CvBridge()

        while not rospy.is_shutdown():
            ret, cv_image = cap.read()
            image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))

        cap.release()
        cv2.destroyAllWindows()

    def __def__(self):
        print("p1_exit")
        
class Tracking_Subscriber():
    def __call__(self): 
        rospy.init_node('tracking_subs', anonymous = False)
        self.tracking_subs = rospy.Subscriber('/cam_tracking%s' % Camera_number,  UInt16MultiArray, self.callback_manual, queue_size=1)

        rospy.spin()

    def callback_manual(self, manual_msg): 
        servo_x = manual_msg.data[0]
        servo_y = manual_msg.data[1]    
        pwm.set_pwm(1, 0, servo_x)
        pwm.set_pwm(0, 0, servo_y)

    def __def__(self):
        print("p2_exit")

class Manual_Subscriber():
    def __call__(self): 
        rospy.init_node('manual_subs', anonymous = False)
        self.manual_subs = rospy.Subscriber('/manual_control_%s' % Camera_number,  UInt16MultiArray, self.callback_manual, queue_size=1)

        rospy.spin()

    def callback_manual(self, manual_msg): 
        servo_x = manual_msg.data[0]
        servo_y = manual_msg.data[1]    
        pwm.set_pwm(1, 0, servo_x)
        pwm.set_pwm(0, 0, servo_y)

    def __def__(self):
        print("p3_exit")

class Cam_Init():
    def __call__(self):
        rospy.init_node('cam_init_subs', anonymous = False)
        self.cma_init_subs = rospy.Subscriber('/cam_init_%s' % Camera_number,  UInt16MultiArray, self.callback_manual, queue_size=2)

        rospy.spin()

    def callback_manual(self, manual_msg): 
        servo_x = manual_msg.data[0]
        servo_y = manual_msg.data[1]    
        pwm.set_pwm(1, 0, servo_x)
        pwm.set_pwm(0, 0, servo_y)
    
    def __def__(self):
        print("p4_exit")
try:    
    p1 = Process(target = Cam_Publisher())          # Cam_data Publisher
    p2 = Process(target = Tracking_Subscriber())    # Tracking_data Subscriber
    p3 = Process(target = Manual_Subscriber())      # Manual_control_data Subscriber
    p4 = Process(target = Cam_Init())               # Cam_position init

    p1.start()
    p2.start()
    p3.start()
    p4.start()

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    print("exit program")
