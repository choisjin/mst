#-*- coding:utf-8 -*-
import rospy
import cv2, sys
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class Rasp_Cam_Subscriber():
    def __init__(self, camera):
        self.camera=camera
        self._sub = rospy.Subscriber('/cam_num_1', Image, self.callback, queue_size=10)
        
        self.bridge = CvBridge()
        
    def callback(self, data):  
        while True:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

            faceCascade = cv2.CascadeClassifier('/home/jin/mst/jin/The_latest_package/Data/Train/haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(self.cv_image, scaleFactor=1.2,minNeighbors=5, minSize=(60, 60))
            # 얼굴인식 후 사각형 그리기
            for (x,y,w,h) in faces:
                cv2.rectangle(self.cv_image,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),1)
                print(faces)
            cv2.imshow('Face_Tracking', self.cv_image)
            k = cv2.waitKey(1) & 0xff
    


# 클래스 내 함수 실행 
if __name__ == '__main__':
    rospy.init_node('Face_Tracking', anonymous=True)
    cam_num = 1
    node = Rasp_Cam_Subscriber(cam_num)
    rospy.spin()
    #sys.exit(node.exec_())