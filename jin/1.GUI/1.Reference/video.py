#-*- coding:utf-8 -*-
import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import rospy
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray


class Rasp_Cam_Subscriber(QtCore.QObject):

    flag = 0
    
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self):
        super(Rasp_Cam_Subscriber, self).__init__(parent)
        self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=10)
        self.bridge = CvBridge()
    
    def callback(self, image_msg):  
        global cv_image
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

    @QtCore.pyqtSlot()
    def startVideo(self):
        
        faceCascade = cv2.CascadeClassifier('/home/jin/mst/jin/2.Tracking_Cam/2.Src/Data/haarcascade_frontalface_default.xml')
        faces = faceCascade.detectMultiScale(cv_image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
        
        # 얼굴인식 후 사각형 그리기
        for (x,y,w,h) in faces:
            cv2.rectangle(cv_image,(x,y),(x+w,y+h),(0,255,0),1)

            pub = rospy.Publisher('servo_x3', UInt16MultiArray, queue_size=10)
            my_msg = UInt16MultiArray()
            my_msg.data = [x,y,w,h]
            pub.publish(my_msg)
        
        width = 640
        height = 480
        label.resize(width, height)
        
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB) 
        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        label.setPixmap(pixmap)

def camera1():
    rospy.init_node('Face_Tracking')
    app = QtWidgets.QApplication([])
    win = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel()
    vbox.addWidget(label)    
    win.setLayout(vbox)
    win.show()
    #def start(self):
    #     global running
    #     running = True
    #     th = threading.Thread(target=self.callback)
    #     th.start()
    #     print("started..")

    # def onExit(self):
    #     print("exit")
    #     self.stop()
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel()
    btn_cmera1 = QtWidgets.QPushButton("Camera 1")
    #btn_cmera2 = QtWidgets.QPushButton("Camera 2")
    vbox.addWidget(label)
    vbox.addWidget(btn_cmera1)
    #vbox.addWidget(btn_cmera2)
    win.setLayout(vbox)
    win.show()

    btn_cmera1.clicked.connect(camera1)
    # btn_stop.clicked.connect(node.stop)
    # app.aboutToQuit.connect(node.onExit)

    sys.exit(app.exec_())