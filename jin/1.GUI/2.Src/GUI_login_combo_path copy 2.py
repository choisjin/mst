#-*- coding:utf-8 -*-

# GUI관련 모듈
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from time import sleep

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
        height = 170
        self.setFixedSize(width, height)
        
        # 카메라선택 ComboBox
        cb = QtWidgets.QComboBox(self)
        cb.resize(180, 30)
        cb.move(10,10)

        cb.addItem('Select Camera.')
        cb.addItem('Camera1')        
        cb.addItem('Camera2')
        
        cb.activated[str].connect(self.Select_arg)
        
        # Train파일 경로 출력
        self.filePath = QtWidgets.QLineEdit(self)
        self.filePath.resize(180, 30)
        self.filePath.setPlaceholderText('train file name..')
        self.filePath.move(10,50)
        
        # Video파일 경로 출력
        self.videoPath = QtWidgets.QLineEdit(self)
        self.videoPath.resize(180, 30)
        self.videoPath.setPlaceholderText('video file name..')
        self.videoPath.move(10,90)
        
        # Train_File 선택 버튼
        self.object_file = QtWidgets.QPushButton("Insert", self)
        self.object_file.resize(55,30)
        self.object_file.move(10,130)
        self.object_file.clicked.connect(self.Insert_Train)
        
        # Video 선택 버튼
        video_file = QtWidgets.QPushButton("Video", self)
        video_file.resize(60,30)
        video_file.move(70,130)        
        video_file.clicked.connect(self.Insert_Video)
        
        # Start 버튼
        start_btn = QtWidgets.QPushButton("Strat", self)
        start_btn.resize(55,30)
        start_btn.move(135,130)
        start_btn.clicked.connect(self.Start_btn)
        
        self.train = 0
        self.video = 0
        self.cam_num = 0
        self.center()       # MainWindow 창 화면 중앙에 위치
        self.show()         # MainWindow 창 띄움

    # 화면 중앙에 창 띄우는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def Insert_Train(self):
        global path1
        path1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'xml File(*.xml)')
        self.filePath.setText(path1[0])
        self.train = 1
    
    def Insert_Video(self):
        global path
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'mp4 File(*.mp4)')
        self.videoPath.setText(path[0])
        self.video = 1

    
    def Select_arg(self, cam_num):
        if cam_num == 'Camera1':
            self.cam_num = 1

        elif cam_num == 'Camera2':
            self.cam_num = 2

    def Start_btn(self):    
        if self.cam_num == 1 and self.train == 1:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Tracking_Camera(self.cam_num)
            self.filePath.clear()
            self.train = 0
            self.cam_num = 0
            print('cam1 & train')
            #self.second.exec_()
            
        
        elif self.cam_num == 2 and self.train == 1:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Tracking_Camera(self.cam_num)
            self.filePath.clear()
            self.train = 0
            self.cam_num = 0
            print('cam2 & train')
            #self.second.exec_()
                    

        elif self.cam_num == 1:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Normal_Camera(self.cam_num)
            self.cam_num = 0
            print('cam1 & normal')
            #self.second.exec_()

        elif self.cam_num == 2:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Normal_Camera(self.cam_num)
            self.cam_num = 0
            print('cam2 & normal')   
            #self.second.exec_()

        else:
            if self.train == 1 and self.video == 1:
                self.second = Tracking_Video()
                self.filePath.clear()
                self.videoPath.clear()
                self.train = 0
                self.video = 0
                print('Train & video')
                #self.second.exec_()

            elif self.train == 0 and self.video == 1:
                self.second = Normal_Video()
                self.videoPath.clear()
                self.video = 0            
                print('video only')
                #self.second.exec_()                    

class Normal_Video(QtWidgets.QDialog):
    def __init__(self):
        super(Normal_Video, self).__init__()
        
        self.setWindowTitle('Video_Viewer')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        vbox = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel()
        self.setLayout(vbox)
        
        vbox.addWidget(self.label)
        
        self.center()
        self.show()
        self.video()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

    def video(self):
        cap = cv2.VideoCapture(path[0])
        cap.set(3,640) # set Width
        cap.set(4,480) # set Height
        self.video_speed = 0.01

        while True:
            self.ret, frame = cap.read()
            if self.ret:
                self.label.resize(640, 480)            
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.label.setPixmap(pixmap)

                sleep(self.video_speed) # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
            if cv2.waitKey(0) == ord('q'):               
                break  
        cap.release()
        cv2.destroyAllWindows()
    


class Tracking_Video(QtWidgets.QDialog):
    def __init__(self):
        super(Tracking_Video, self).__init__()
        
        self.setWindowTitle('Tracking_Video_Viewer')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        vbox = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel()
        self.setLayout(vbox)
        
        vbox.addWidget(self.label)
        
        self.center()
        self.show()
        self.video()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topRight())

    def video(self):
        self.cap = cv2.VideoCapture(path[0])
        self.cap.set(3,640) # set Width
        self.cap.set(4,480) # set Height
        self.video_speed = 0.01
        faceCascade = cv2.CascadeClassifier(path1[0])

        while True:
            ret, frame = self.cap.read()
            faces = faceCascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
            
            if ret:
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)      
                
                self.label.resize(640, 480)            
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.label.setPixmap(pixmap)

                sleep(self.video_speed) # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
                if cv2.waitKey(0) == ord('q'):               
                    break  
        
        self.cap.release()
        cv2.destroyAllWindows()

        
class Normal_Camera(QtWidgets.QDialog):
    def __init__(self, camera):
        super(Normal_Camera, self).__init__()
        
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
            
        faceCascade = cv2.CascadeClassifier(path1[0])
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
            #print(my_msg)
        
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