#-*- coding:utf-8 -*-
import rospy, cv2, Adafruit_PCA9685 
from std_msgs.msg import UInt16MultiArray, Int8MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError




1111





class Cam_Publisher():
    def __init__(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 20)
        subs_start = 1
        rospy.init_node("webcam_pub", anonymous=True)
        image_pub = rospy.Publisher("cam_num1", Image, queue_size=1)

        bridge = CvBridge()

        while not rospy.is_shutdown():
            ret, cv_image = cap.read()
            image_pub.publish(bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            if subs_start ==1:
                self.servo = Servo_Subscriber()
                subs_start = 0
        cap.release()
        cv2.destroyAllWindows()

class Servo_Subscriber():
    def __init__(self):
        self.Servo_subs = rospy.Subscriber('/servo_controller_%s' % Camera_number, UInt16MultiArray, self.callback, queue_size=1) # 객체인식 바운딩박스 x,y,w,h 토픽
        self._Manual_subs = rospy.Subscriber('/manual_control_%s' % Camera_number, Int8MultiArray, self.callback1, queue_size=1)
        self.servo_x = 320   # servo_x defalt position
        self.servo_y = 390
        pwm.set_pwm(1, 0, self.servo_x)
        pwm.set_pwm(0, 0, self.servo_y)
        
    def callback(self, servo_msg):
        print(servo_msg)
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

    def callback1(self, manual_msg):
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

    def main(self):
        rospy.spin()

if __name__ == '__main__':
    node = Cam_Publisher()
    rospy.init_node('Servo_Move')