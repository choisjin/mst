#-*- coding:utf-8 -*-
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int64MultiArray

class Rasp_Cam_Subscriber():
    def __init__(self):
        
        self.selecting_sub_image = "compressed" # 토픽선택 compressed or raw
 
        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)
 
            self.bridge = CvBridge()

    def callback(self, image_msg):  
 
        if self.selecting_sub_image == "compressed":
            # 토픽데이터 cv용 데이터로 컨버팅
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        elif self.selecting_sub_image == "raw":
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
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = cv_image[y:y+h, x:x+w]        

            pub = rospy.Publisher('servo_x3', Int64MultiArray, queue_size=10)
            my_msg = Int64MultiArray()
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