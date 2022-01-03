#-*- coding:utf-8 -*-
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt8MultiArray
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class Rasp_Cam1_Subscriber():
    def __init__(self, camera):
        self.camera=camera
        if camera == 1 :
            self._sub = rospy.Subscriber('/camera1/usb_cam1/image_raw', Image, self.callback, queue_size=10)
        elif camera == 2 :
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=10)
        
        self.bridge = CvBridge()

    def callback(self, data):  
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        faceCascade = cv2.CascadeClassifier('/home/jin/mst/jin/2.Tracking_Cam/2.Src/Data/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
        
        #얼굴인식 후 사각형 그리기
        for (x,y,w,h) in faces:
            cv2.rectangle(cv_image,(x,y),(x+w,y+h),(0,255,0),1)
            cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),1)

            pub = rospy.Publisher('servo_x3', UInt8MultiArray, queue_size=10)
            my_msg = UInt8MultiArray()
            my_msg.data = [x,y,w,h]
            pub.publish(my_msg)

        #이미지 출력
        if self.camera == 1:
            width = 640
            height = 480
        elif self.camera == 2:
            width = 320
            height = 240
        
        label.resize(width, height)
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB) 
        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        label.setPixmap(pixmap)
        print(label)
        print(type(label))
        #이미지 출력
        # cv2.imshow('Camera%d' % self.camera, cv_image)
        # k = cv2.waitKey(1) & 0xff
        # if k == 27:
            # cv2.destroyAllWindows()
            
def cam1(args):
    if __name__ == '__main__':
        rospy.init_node('Face_Tracking', anonymous=True)
        #try:
        #    rospy.spin()
        #except KeyboardInterrupt:
        #    print("Shutting down")
        cam_num = 1
        node = Rasp_Cam1_Subscriber(cam_num)
        win = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        vbox.addWidget(label)
        win.setLayout(vbox)
        win.show()

def cam2(args):
    if __name__ == '__main__':
        rospy.init_node('Face_Tracking', anonymous=True)
        #try:
        #    rospy.spin()
        #except KeyboardInterrupt:
        #    print("Shutting down")
        cam_num = 2
        node = Rasp_Cam1_Subscriber(cam_num)
        win = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        vbox.addWidget(label)
        win.setLayout(vbox)
        win.show()

def stop(args):
    rospy.signal_shutdown()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel()
    
    btn_cmera1 = QtWidgets.QPushButton("Camera 1")
    btn_cmera2 = QtWidgets.QPushButton("Camera 2")
    btn_stop = QtWidgets.QPushButton("Stop") 
    
    vbox.addWidget(label)
    vbox.addWidget(btn_cmera1)
    vbox.addWidget(btn_cmera2)
    vbox.addWidget(btn_stop)
    
    win.setLayout(vbox)
    win.show()

    btn_cmera1.clicked.connect(cam1)
    btn_cmera2.clicked.connect(cam2)
    btn_stop.clicked.connect(stop)
    sys.exit(app.exec_())