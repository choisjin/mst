#-*- coding:utf-8 -*-
import sys, rospy, cv2, Adafruit_PCA9685 
from std_msgs.msg import UInt16MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


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

class Background_Set():                                                 # 배경화면 셋팅
    def background_set(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

class System_On():
    def system_on(self):
        self.cam_pub = Cam_Publisher()
        self.tracking_sub = Tracking_Subscriber()
        self.manual_sub = Manual_Subscriber()
        self.cam_init = Cam_Init()

class Raspberry_Pi(System_On, object):
    def __init__(self):                                 # 로그인 화면 셋팅
        super(Raspberry_Pi, self).__init__()
        
        #Background_Set.background_set()   

        width = 70
        height = 140
        #self.setFixedSize(width, height)

        self.button_sys_on = QtWidgets.QPushButton('on', self)
        self.button_sys_on.clicked.connect(self.system_on())
        self.button_sys_on.resize(60, 30)
        self.button_sys_on.move(5, 5)
        self.button_sys_on.setStyleSheet('QPushButton {background-color: #000000; color: white;}')

        self.button_exit = QtWidgets.QPushButton('Exit', self)
        self.button_exit.clicked.connect(self.close)
        self.button_exit.resize(60, 30)
        self.button_exit.move(5, 70)
        self.button_exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')        

        self.center()

    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topRight())

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



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = Raspberry_Pi()
    init.show()
    sys.exit(app.exec_())