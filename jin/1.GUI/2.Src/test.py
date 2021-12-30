#-*- coding:utf-8 -*-
import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import cv_bridge

import rospy
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

# class Rasp_Cam_Subscriber():
#     def __init__(self):
        
#         self.selecting_sub_image = "compressed" # 토픽선택 compressed or raw
 
#         if self.selecting_sub_image == "compressed":
#             self._sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, self.callback, queue_size=1)
#         else:
#             self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)
 
#             self.bridge = CvBridge()

#     def callback(self, image_msg):  
 
#         if self.selecting_sub_image == "compressed":
#             # 토픽데이터 cv용 데이터로 컨버팅
#             np_arr = np.fromstring(image_msg.data, np.uint8)
#             cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
#         elif self.selecting_sub_image == "raw":
#             cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        
    
#     def main(self):
#         rospy.spin()

class ShowVideo(QtCore.QObject):
    def __init__(self):
        
        self.selecting_sub_image = "compressed" # 토픽선택 compressed or raw
 
        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)
 
            self.bridge = CvBridge()
    
    @QtCore.pyqtSlot()
    def callback(self, image_msg):  
 
        if self.selecting_sub_image == "compressed":
            # 토픽데이터 cv용 데이터로 컨버팅
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        
        #    cv2.imshow('Face_Tracking', cv_image)
        #    k = cv2.waitKey(1) & 0xff

        width = 480
        height = 680
        color_swapped_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        qt_image1 = QtGui.QImage(color_swapped_image.data,
                                width,
                                height,
                                color_swapped_image.strides[0],
                                QtGui.QImage.Format_RGB888)
        self.VideoSignal1.emit(qt_image1)
        
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(25, loop.quit) #25 ms
        loop.exec_()
    
        #camera = cv2.VideoCapture(0)
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


if __name__ == '__main__':
    rospy.init_node('Face_Tracking')
    #node = Rasp_Cam_Subscriber()
    #node.main()    
    
    app = QtWidgets.QApplication(sys.argv)

    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer1 = ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)

    #push_button1 = QtWidgets.QPushButton('Start')
    #push_button1.clicked.connect(vid.callback)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    vertical_layout.addLayout(horizontal_layout)
    #vertical_layout.addWidget(push_button1)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())