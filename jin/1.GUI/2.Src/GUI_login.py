#-*- coding:utf-8 -*-

# GUI관련 모듈
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

# Topic통신 관련 모듈
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray

class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setWindowTitle('Login Window')
        width = 200
        height = 150
        self.setFixedSize(width, height)
        
        layout = QtWidgets.QGridLayout()

        logo_label = QtWidgets.QLabel(self)
        logo_label.move(70, 7)
        pixmap = QtGui.QPixmap('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/mst.png')
        logo_label.setPixmap(pixmap)

        label_name = QtWidgets.QLabel('<font size="2"> ID </font>')
        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setPlaceholderText('Enter your ID')
        layout.addWidget(label_name, 3, 0)
        layout.addWidget(self.lineEdit_username, 3, 1)
        
        label_password = QtWidgets.QLabel('<font size="2"> PW </font>')
        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText('Enter your pw')
        layout.addWidget(label_password, 4, 0)
        layout.addWidget(self.lineEdit_password, 4, 1)
        
        button_login = QtWidgets.QPushButton('Login')
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 5, 0, 1, 2)
        layout.setRowMinimumHeight(2, 30)
        
        self.setLayout(layout)
        self.center()
    
    def check_password(self):
        msg = QtWidgets.QMessageBox()

        if self.lineEdit_username.text() == 'choi3206' and self.lineEdit_password.text() == '0608':
            # msg.setText('Success')
            # msg.exec_()
            self.close()
            self.init = MainWindow()
            
        
        else :
            msg.setText('Check your ID, PW')
            msg.exec_()
            
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())    

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        width = 200
        height = 100
        self.setFixedSize(width, height)
        vbox = QtWidgets.QVBoxLayout()
        cb = QtWidgets.QComboBox(self)
        cb.resize(180, 30)
        cb.move(10,10)
        #cb.addItem("카메라를 선택해 주세요.")
        cb.addItem('Camera1')        
        cb.addItem('Camera2')
        
        cb.activated[str].connect(self.openCameraViewer)
        print(cb.activated[str])
        #btn_camera1 = QtWidgets.QPushButton("Camera 1")
        #btn_camera2 = QtWidgets.QPushButton("Camera 2")

        #vbox.addWidget(btn_camera1)
        #vbox.addWidget(btn_camera2)

        #btn_camera1.clicked.connect(self.openCameraViewer1)
        #btn_camera2.clicked.connect(self.openCameraViewer2)
        self.center()
        self.setLayout(vbox)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    # 카메라 선택
    def openCameraViewer(self, cam_num):
        if cam_num == 'Camera1':
            cam_num = 1
        elif cam_num == 'Camera2':
            cam_num = 2

        rospy.init_node('Face_Tracking', anonymous=True)
        self.second = Tracking_Camera(cam_num)
        self.second.exec_()                       

class Tracking_Camera(QtWidgets.QDialog):
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
        
        self.center()
        self.show()    

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
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

            pub = rospy.Publisher('servo_x3', UInt16MultiArray, queue_size=10)
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
    init = LoginForm()
    init.show()
 
    
    sys.exit(app.exec_())