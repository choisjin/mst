#-*- coding:utf-8 -*-
# GUI관련 모듈
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

# Topic통신 관련 모듈
import os, sys
import rospy, cv2
import cv2
import numpy as np

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray, Int8MultiArray
from time import sleep
import datetime

class Background_Set():                                     # 배경화면 셋팅
    def background_set(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

class LoginForm(QtWidgets.QDialog, Background_Set):         # 로그인 화면
    def __init__(self):                     # 로그인 화면 셋팅
        super(LoginForm, self).__init__()
        
        self.background_set()
        
        width = 265
        height = 110
        
        self.setFixedSize(width, height)

        logo_label = QtWidgets.QLabel(self)
        logo_label.resize(100, 100)
        logo_label.move(160, 5)
        pixmap = QtGui.QPixmap('/home/jin/mst/jin/1.GUI/2.Src/icon/Finder_baby.png')
        logo_label.setPixmap(pixmap)

        self.label_name = QtWidgets.QLabel('<font size="2"> ID </font>', self)
        self.label_name.resize(20, 30)
        self.label_name.move(10, 5)

        self.lineEdit_username = QtWidgets.QLineEdit(self)
        self.lineEdit_username.setPlaceholderText('Enter your ID')
        self.lineEdit_username.resize(125, 30)
        self.lineEdit_username.move(30, 5)                
        
        self.label_password = QtWidgets.QLabel('<font size="2"> PW </font>', self)
        self.label_password.resize(20, 30)
        self.label_password.move(5, 40)   

        self.lineEdit_password = QtWidgets.QLineEdit(self)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText('Enter your pw')
        self.lineEdit_password.resize(125, 30)
        self.lineEdit_password.move(30, 40)

        self.button_login = QtWidgets.QPushButton('Login', self)
        self.button_login.clicked.connect(self.check_password)
        self.button_login.resize(60, 30)
        self.button_login.move(30, 75)
        self.button_login.setStyleSheet('QPushButton {background-color: #000000; color: white;}')

        self.button_exit = QtWidgets.QPushButton('Exit', self)
        self.button_exit.clicked.connect(self.close)
        self.button_exit.resize(60, 30)
        self.button_exit.move(95, 75)
        self.button_exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        
        self.center()
        
        global Position
        Position = self.qr.topRight()

    def check_password(self):
        msg = QtWidgets.QMessageBox()

        if self.lineEdit_username.text() == 'choi3206' and self.lineEdit_password.text() == '0608':
            self.close()
            self.init = MainWindow()
        else :
            msg.setText('Check your ID, PW')
            msg.exec_()
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()
            
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topRight())    

    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.check_password()
        
        elif e.key() == Qt.Key_Escape:
            self.close()        

class MainWindow(QtWidgets.QMainWindow, Background_Set):    # 기능선택 화면
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        global Main_width
        global Main_height

        self.background_set()
        
        Main_width = 175
        Main_height = 160
        self.setFixedSize(Main_width, Main_height)
        self.setGeometry(Position.x(), Position.y(), Main_width, Main_height)
        self.setToolBar()      

        Path_width = 165
        Path_height = 30
        
    # Train파일 경로 출력
        self.filePath = QtWidgets.QLineEdit(self)
        self.filePath.resize(Path_width, Path_height)
        self.filePath.setPlaceholderText('Train file name...')
        self.filePath.move(5, 75)

    # Video파일 경로 출력
        self.videoPath = QtWidgets.QLineEdit(self)
        self.videoPath.resize(Path_width, Path_height)
        self.videoPath.setPlaceholderText('Video file name...')
        self.videoPath.move(5, 110)

    # 카메라선택 ComboBox
        self.cb = QtWidgets.QComboBox(self)
        self.cb.resize(Path_width, Path_height)
        self.cb.move(5, 40)
        #self.DataReset()
        self.ComboBoxInit()
        self.cb.activated[str].connect(self.Select_Cam)

        self.train = 0
        self.video = 0
        self.cam_num = 0
    
        self.show()                                 # MainWindow 창 띄움

    def setToolBar(self):                           # 툴바 셋팅
        exitAction = QtWidgets.QAction(
            QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/exit.png'), 'Exit', self)   # 툴바 아이콘 이미지 삽입
        exitAction.setShortcut('Ctrl+Q')            # 툴바 단축키 설정
        exitAction.setStatusTip('Exit')             # 상태창 메세지
        exitAction.setToolTip('Ctrl+Q')             # 툴팁 메세지
        exitAction.triggered.connect(self.close)    # 툴바 클릭시 발생 이벤트

        logoutAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/logout.png'), 'Logout', self)
        logoutAction.setShortcut('Ctrl+L')
        logoutAction.setStatusTip('Logout')
        logoutAction.setToolTip('Ctrl+L')
        logoutAction.triggered.connect(self.Logout)

        trainAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/train_open.png'), 'Train', self)
        trainAction.setShortcut('Ctrl+T')
        trainAction.setStatusTip('Train File Open')
        trainAction.setToolTip('Ctrl+T')
        trainAction.triggered.connect(self.Insert_Train)
        
        videoAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/video_open.png'), 'Video', self)
        videoAction.setShortcut('Ctrl+O')
        videoAction.setStatusTip('Video File Open')
        videoAction.setToolTip('Ctrl+O')
        videoAction.triggered.connect(self.Insert_Video)        
        
        stratAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/play.png'), 'Start', self)
        stratAction.setShortcut('Ctrl+S')
        stratAction.setStatusTip('Start Application')
        stratAction.setToolTip('Ctrl+S')
        stratAction.triggered.connect(self.Start_btn)        
        
        self.statusBar()

        self.toolbar = self.addToolBar('ToolBar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(stratAction)
        self.toolbar.addAction(trainAction)
        self.toolbar.addAction(videoAction)
        self.toolbar.addAction(logoutAction)
        self.toolbar.addAction(exitAction)

    def ComboBoxInit(self):                         # ComboBox 초기화
        self.cb.clear()                             # ComboBox 모두 지우기
        self.cam_num = 0
        combo_num = 2                               # ComboBox 생성 갯수
        combo_init = 0                              
        self.cb.setStyleSheet('QComboBox {background-color: #FFFFFF; color: Black;}')
        self.cb.addItem('Select Camera...')         # Default Item 생성
        while combo_init < combo_num :              # ComboBox 생성
            combo_init += 1
            self.cb.addItem('Camera%d' % combo_init) 

    def Insert_Train(self):
        self.filePath.clear()
        global path1
        path1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'xml File(*.xml)')
        self.filePath.setText(path1[0])
        if path1[0] == '':
            self.train = 0
        else:
            self.train = 1
    
    def Insert_Video(self):
        global path
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'mp4 File(*.mp4)')
        self.videoPath.setText(path[0])
        if path[0] == '':
            self.video = 0
        else:
            self.video = 1
            self.cam_select = 0
            self.ComboBoxInit()
    
    def Logout(self):
        self.logout = LoginForm()
        
        self.close()
        if self.logout_signal == 1:
            self.logout.show()
        else:
            self.show()
            
    def Select_Cam(self, cam_num):
        self.videoPath.clear()
        if cam_num == 'Select Camera...':
            self.cam_select = 0
        else:
            self.cam_num = cam_num[-1]
            self.cam_num = int(self.cam_num)
            self.cam_select = 1            
    
    def Start_btn(self):
        self.filePath.clear()
        if self.cam_select == 1 and self.train == 1: 
            print('Train_Cam')
            self.train = 0
            rospy.init_node('Tracking_Cam', anonymous=False)
            Tracking_Camera(self.cam_num)
        elif self.cam_select == 1:
            print('Normal_Cam')
            rospy.init_node('Tracking_Cam', anonymous=False)
            Normal_Camera(self.cam_num)
        else:
            if self.train == 1 and self.video == 1:
                print('Train & video')
                self.train = 0
                Tracking_Video()
            elif self.train == 0 and self.video == 1:
                print('video only')
                Normal_Video() 

    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.logout_signal=1
        else:
            self.logout_signal=2
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

class Capture_Rec():
    def args(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')       # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False         # 녹화 유무 변수 초기화

    def image_cap(self):
        print('Image Capture!')
        
    def cam_rec(self):
        print('Video Capture!')

class Cam_Btn_Set():                                        # Cam 조작 화면 버튼
    def cam_btn_set(self, camera):
        self.Camera_contol_num = camera
        
        self.button_Auto = QtWidgets.QPushButton('Auto', self)
        self.button_Auto.resize(65, 30)
        self.button_Auto.move(290, 485)
        self.button_Auto.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Auto.clicked.connect(self.controller_open)

        self.button_Cap = QtWidgets.QPushButton('Capture', self)
        self.button_Cap.resize(65, 30)
        self.button_Cap.move(360, 485)
        self.button_Cap.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Cap.clicked.connect(self.camera_cap)

        self.button_REC = QtWidgets.QPushButton('REC', self)
        self.button_REC.resize(65, 30)
        self.button_REC.move(430, 485)
        self.button_REC.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_REC.clicked.connect(self.rec_strat)

        self.button_Stop = QtWidgets.QPushButton('Stop', self)
        self.button_Stop.resize(65, 30)
        self.button_Stop.move(500, 485)
        self.button_Stop.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Stop.clicked.connect(self.rec_stop)    

        self.button_Exit = QtWidgets.QPushButton('Exit', self)
        self.button_Exit.resize(65, 30)
        self.button_Exit.move(570, 485)
        self.button_Exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Exit.clicked.connect(self.exit_cam)

        self.manual = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')         # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False                                   # 녹화 유무 변수 초기화
        self.now = datetime.datetime.now().strftime("MST_CAP-%Y-%m-%d-%H:%M:%S")

    def camera_cap(self):
        print('Video Capture!')
        cv2.imwrite("/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Capture_Video/" + str(self.now) + ".png", self.frame)

    def rec_strat(self):
        self.button_REC.setEnabled(False)
        print('Recording Start!')
        self.record = True
        self.video = cv2.VideoWriter("/home/jin/mst/jin/1.GUI/2.Src/Recording_Video/" + str(self.now) + ".avi", self.fourcc, 30.0, (self.frame.shape[1], self.frame.shape[0]))        
        self.button_REC.setText("REC...")

    def rec_stop(self):
        self.button_REC.setEnabled(True)
        print('Recording Stop!')
        self.record = False
        self.video.release()
        self.button_REC.setText("REC")

    def controller_open(self):
        self.button_Auto.setText("Manual")
        self.control = Camera_Control(self.Camera_contol_num)
        self.manual = 1
        self.button_Auto.clicked.connect(self.controller_close)

    def controller_close(self):
        self.button_Auto.setText("Auto")
        self.control.close()
        self.button_Auto.clicked.connect(self.controller_open)

    def exit_cam(self):
        if self.manual == 1:
            self.close()
            self.control.close()
        else:
            self.close()

class Video_Btn_Set():                                        # Video 조작 화면 버튼
    def video_btn_set(self):        
        self.button_Cap = QtWidgets.QPushButton('Capture', self)
        self.button_Cap.resize(65, 30)
        self.button_Cap.move(360, 485)
        self.button_Cap.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Cap.clicked.connect(self.video_cap)

        self.button_REC = QtWidgets.QPushButton('REC', self)
        self.button_REC.resize(65, 30)
        self.button_REC.move(430, 485)
        self.button_REC.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_REC.clicked.connect(self.rec_strat)

        self.button_Stop = QtWidgets.QPushButton('Stop', self)
        self.button_Stop.resize(65, 30)
        self.button_Stop.move(500, 485)
        self.button_Stop.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Stop.clicked.connect(self.rec_stop)        

        self.button_Exit = QtWidgets.QPushButton('Exit', self)
        self.button_Exit.resize(65, 30)
        self.button_Exit.move(570, 485)
        self.button_Exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Exit.clicked.connect(self.exit_cam)

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')         # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False                                   # 녹화 유무 변수 초기화
        self.now = datetime.datetime.now().strftime("MST_CAP-%Y-%m-%d-%H:%M:%S")

    def video_cap(self):
        print('Video Capture!')
        cv2.imwrite("/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Capture_Video/" + str(self.now) + ".png", self.frame)

    def rec_strat(self):
        self.button_REC.setEnabled(False)
        print('Recording Start!')
        self.record = True
        self.video = cv2.VideoWriter("/home/jin/mst/jin/1.GUI/2.Src/Recording_Video/" + str(self.now) + ".avi", self.fourcc, 30.0, (self.frame.shape[1], self.frame.shape[0]))        
        self.button_REC.setText("REC...")

    def rec_stop(self):
        self.button_REC.setEnabled(True)
        print('Recording Stop!')
        self.record = False
        self.video.release()
        self.button_REC.setText("REC")

    def exit_cam(self):
        self.close()

class Normal_Video(QtWidgets.QDialog, Video_Btn_Set, Background_Set):      # Only Video
    def __init__(self):
        super(Normal_Video, self).__init__()
        self.setWindowTitle('Normal_Video')
        self.background_set()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)

        vbox = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)
        
        vbox.addWidget(self.label)

        self.video_btn_set()
        self.show()
        self.video_convert()

    def video_convert(self):
        self.cap = cv2.VideoCapture(path[0])
        self.video_speed = 0.01                             # 배속조절 1프레임당 0.01초  0.02 = 0.5배속

        while True:
            self.ret, self.frame = self.cap.read()  
            
            if self.record == True:
                self.video.write(self.frame)            
            
            if not self.ret:
                if self.record == True:
                    print('Recording Stop!')
                    self.record = False
                    self.video.release()
                    self.close()
                else:
                    self.close()
                break
            
            self.label.resize(640, 480)
            img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            pixmap = pixmap.scaledToWidth(640)
            self.label.setPixmap(pixmap)
            sleep(self.video_speed)
            cv2.waitKey(1)

        self.cap.release()
        cv2.destroyAllWindows()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            if self.record == True:
                print('Recording Stop!')
                self.record = False
                self.video.release()
                self.cap.release()
                self.close()
            else:
                self.cap.release()
                self.close()

class Tracking_Video(QtWidgets.QDialog, Background_Set):    # Train & Video
    def __init__(self):
        super(Tracking_Video, self).__init__()
        self.background_set()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)

        self.show()  
        self.video()

    def video(self):
        self.cap = cv2.VideoCapture(path[0])
        video_speed = 0.01 # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
        faceCascade = cv2.CascadeClassifier(path1[0])
        while True:
            self.ret, frame = self.cap.read()
            faces = faceCascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
            
            if not self.ret:
                self.close()
                break
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)      
            
            self.label.resize(640, 480)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            pixmap = pixmap.scaledToWidth(640)
            self.label.setPixmap(pixmap)
            
            sleep(video_speed) 
            cv2.waitKey(0)
        
        self.cap.release()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cap.release()

class Camera_Control(QtWidgets.QDialog, Background_Set):    # Cam 수동조작 & 방향키
    def __init__(self, Camera_control_num):
        super(Camera_Control, self).__init__()
        self.background_set()
        
        self.Camera_control_num = Camera_control_num
        print('Cam_Control_Num : %d' % self.Camera_control_num)

        height = 90
        self.setFixedSize(Main_width, height)
        self.setGeometry(Position.x(), Position.y()+Main_height+10, Main_width, height)

        self.button_Up = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/up.png'),'', self)
        self.button_Up.resize(40, 40)
        self.button_Up.move(67.5, 5)
        self.button_Up.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Up.setFocusPolicy(Qt.NoFocus)
        self.button_Up.clicked.connect(self.Manual_Up)

        self.button_Down = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/down.png'),'', self)
        self.button_Down.resize(40, 40)
        self.button_Down.move(67.5, 46)
        self.button_Down.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Down.setFocusPolicy(Qt.NoFocus)
        self.button_Down.clicked.connect(self.Manual_Down)

        self.button_Right = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/right.png'),'', self)
        self.button_Right.resize(40, 40)
        self.button_Right.move(108, 46)
        self.button_Right.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Right.setFocusPolicy(Qt.NoFocus)
        self.button_Right.clicked.connect(self.Manual_Right)

        self.button_Left = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/left.png'),'', self)
        self.button_Left.resize(40, 40)
        self.button_Left.move(26.5, 46)
        self.button_Left.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Left.setFocusPolicy(Qt.NoFocus)
        self.button_Left.clicked.connect(self.Manual_Left)

        self.show()

    def Manual_Up(self):
        y = 1
        pub = rospy.Publisher('manual_control%d'%self.Camera_control_num, Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [0, y]
        pub.publish(my_msg)

    def Manual_Down(self):
        y = -1
        pub = rospy.Publisher('manual_control%d'%self.Camera_control_num, Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [0, y]
        pub.publish(my_msg)

    def Manual_Right(self):
        x = 1
        pub = rospy.Publisher('manual_control%d'%self.Camera_control_num, Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [x, 0]
        pub.publish(my_msg)

    def Manual_Left(self):
        x = -1
        pub = rospy.Publisher('manual_control%d'%self.Camera_control_num, Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [x, 0]
        pub.publish(my_msg)

    def keyPressEvent(self, k):
        if k.key() == Qt.Key_Escape:
            self.close()
        elif k.key() == Qt.Key_Up:
            self.Manual_Up()
        elif k.key() == Qt.Key_Down:
            self.Manual_Down()
        elif k.key() == Qt.Key_Right:
            self.Manual_Right()
        elif k.key() == Qt.Key_Left:
            self.Manual_Left()

class Normal_Camera(QtWidgets.QDialog, Cam_Btn_Set, Background_Set):    # Only Cam
    def __init__(self, camera):
        super(Normal_Camera, self).__init__()
        self.background_set()

        self.camera=camera  
        self._sub = rospy.Subscriber('/camera%s/usb_cam%s/image_raw' % (str(camera), str(camera)), Image, self.callback, queue_size=1)
        
        self.bridge = CvBridge()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)
        
        self.cam_btn_set(camera)
        self.show()    

    def callback(self, data):  
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        self.ret = self.cv_image in self.bridge.imgmsg_to_cv2(data, "bgr8")

        if not self.ret == False:
            print(self.cv_image)
        else :
            print('None')

        if self.record == True:
            self.video.write(self.cv_image)

        self.label.resize(640, 480)
        img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB) 
        img = cv2.flip(img, 1)
        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        pixmap = pixmap.scaledToWidth(640)
        self.label.setPixmap(pixmap)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.Exit_cam()
            self.close()

class Tracking_Camera(QtWidgets.QDialog, Cam_Btn_Set, Background_Set):  # Train & Video
    def __init__(self, camera):
        super(Tracking_Camera, self).__init__()
        self.background_set()

        self.camera=camera  
        self._sub = rospy.Subscriber('/camera%s/usb_cam%s/image_raw' % (str(camera), str(camera)), Image, self.callback, queue_size=1)
        
        self.bridge = CvBridge()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)
        
        self.cam_btn_set(camera)

        self.show()     

    def callback(self, data):  
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            # if path1[0] == '':        # Tracking cam 중단
                # exit()            
            faceCascade = cv2.CascadeClassifier(path1[0])

            self.cv_image = np.uint8(self.cv_image)
            faces = faceCascade.detectMultiScale(self.cv_image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))

            for (x,y,w,h) in faces:
                cv2.rectangle(self.cv_image,(x,y),(x+w,y+h),(0,255,0),1)
                pub = rospy.Publisher('Servo_Cam%d' % self.camera, UInt16MultiArray, queue_size=1)
                self.my_msg = UInt16MultiArray()
                self.my_msg.data = [x,y,w,h]
                pub.publish(self.my_msg)
        
            self.label.resize(640, 480)
            img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB) 
            img = cv2.flip(img, 1)
            img_h,img_w,img_c = img.shape
            qImg = QtGui.QImage(img.data, img_w, img_h, img_w*img_c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            pixmap = pixmap.scaledToWidth(640)
            self.label.setPixmap(pixmap)
            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.Exit_cam()
            self.close()    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = LoginForm()
    init.show()
    sys.exit(app.exec_())