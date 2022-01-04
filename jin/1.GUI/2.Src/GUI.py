#-*- coding:utf-8 -*-

# GUI관련 모듈
import sys
from PyQt5.QtWidgets import QDialog, QWidget, QDesktopWidget
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

# Topic통신 관련 모듈
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray

class MianWindow(QWidget):
    def __init__(self):
        super(MianWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Main')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        width = 200
        height = 100
        self.setFixedSize(width, height)
        vbox = QtWidgets.QVBoxLayout()
    
        btn_camera1 = QtWidgets.QPushButton("Camera 1")
        btn_camera2 = QtWidgets.QPushButton("Camera 2")

        vbox.addWidget(btn_camera1)
        vbox.addWidget(btn_camera2)

        btn_camera1.clicked.connect(self.openCameraViewer1)
        btn_camera2.clicked.connect(self.openCameraViewer2)
        self.move(600, 400)
        self.setLayout(vbox)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    # 카메라 선택
    def openCameraViewer1(self):
        cam_num = 1
        
        #self.close()    
        rospy.init_node('Face_Tracking', anonymous=True)
        self.second = Tracking_Camera(cam_num)
        self.second.exec_()               
 
    def openCameraViewer2(self):
        cam_num = 2
        
        #self.close()    
        rospy.init_node('Face_Tracking', anonymous=True)
        self.second = Tracking_Camera(cam_num)
        self.second.exec_()             

class Tracking_Camera(QDialog, QWidget):
    def __init__(self, camera):
        super(Tracking_Camera, self).__init__()
        
        self.setWindowTitle('Camera%d' % camera)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.camera=camera
        if camera == 1 :
            self._sub = rospy.Subscriber('/camera1/usb_cam1/image_raw', Image, self.callback, queue_size=10)
        
        elif camera == 2 :
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=10)
        
        self.bridge = CvBridge()
         
        vbox = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.setLayout(vbox)
        
        vbox.addWidget(self.label)
        vbox.addWidget(self.label)
        
        self.center()
        self.show()    

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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

            pub = rospy.Publisher('servo_x3', UInt16MultiArray, queue_size=1)
            my_msg = UInt16MultiArray()
            my_msg.data = [x,y,w,h]
            pub.publish(my_msg)
            print(my_msg)
        #이미지 출력
        if self.camera == 1:
            width = 640
            height = 480
        
        elif self.camera == 2:
            width = 320
            height = 240
        
        self.label.resize(width, height)
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB) 
        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = MianWindow()
    sys.exit(app.exec_())