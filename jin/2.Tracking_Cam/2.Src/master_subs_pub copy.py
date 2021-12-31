#-*- coding:utf-8 -*-
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import UInt8MultiArray

class Rasp_Cam_Subscriber():
    def __init__(self):
        self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=10)
        self.bridge = CvBridge()

    def callback(self, image_msg):  
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        faceCascade = cv2.CascadeClassifier('/home/jin/mst/jin/2.Tracking_Cam/2.Src/Data/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )
        
        # 얼굴인식 후 사각형 그리기
        for (x,y,w,h) in faces:
            cv2.rectangle(cv_image,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)

            pub = rospy.Publisher('servo_x3', UInt8MultiArray, queue_size=10)
            my_msg = UInt8MultiArray()
            my_msg.data = [x,y,w,h]
            pub.publish(my_msg)

        # 이미지 출력
        cv2.imshow('Face_Tracking', cv_image)
        k = cv2.waitKey(1) & 0xff
        
    # 토픽 끊기지 않게 하기위한 스핀명령    
    def main(self):
        rospy.spin()

# 클래스 내 함수 실행 
if __name__ == '__main__':
    rospy.init_node('Face_Tracking')
    node = Rasp_Cam_Subscriber()
    node.main()