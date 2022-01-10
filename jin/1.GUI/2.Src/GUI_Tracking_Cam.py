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
from std_msgs.msg import UInt16MultiArray, Int8MultiArray
import numpy as np

class LoginForm(QtWidgets.QDialog):         # 로그인 화면
    def __init__(self):                     # 로그인 화면 셋팅
        super(LoginForm, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        
        self.setWindowTitle('Login Window')
        
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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        global Main_width
        global Main_height
        Main_width = 175
        Main_height = 160
        self.setFixedSize(Main_width, Main_height)
        self.setGeometry(Position.x(), Position.y(), Main_width, Main_height)
        self.setToolBar()      
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        
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
        self.DataReset()
        self.ComboBoxInit()
        self.cb.activated[str].connect(self.Select_Cam)

        self.show()                                 # MainWindow 창 띄움

    def setToolBar(self):                           # 툴바 셋팅
        exitAction = QtWidgets.QAction(
            QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/exit.png'),
             'Exit', self)                          # 툴바 아이콘 이미지 삽입
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

    def DataReset(self):                            # 입력 데이터 초기화
        self.cam_select = 0                         # Camera 선택 초기화
        self.train = 0                              # Train 선택 초기화
        self.filePath.clear()                       # Train 파일 경로 초기화
        self.video = 0                              # Video 선택 초기화
        self.videoPath.clear()                      # Video 파일 경로 초기화

    def ComboBoxInit(self):                         # ComboBox 초기화
        self.cb.clear()                             # ComboBox 모두 지우기
        combo_num = 2                               # ComboBox 생성 갯수
        combo_init = 0                              
        self.cb.setStyleSheet('QComboBox {background-color: #FFFFFF; color: Black;}')
        self.cb.addItem('Select Camera...')         # Default Item 생성
        while combo_init < combo_num :              # ComboBox 생성
            combo_init += 1
            self.cb.addItem('Camera%d' % combo_init) 

    def Insert_Train(self):
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
            self.cam_num = 0
            self.ComboBoxInit()
    
    def Logout(self):
        self.logout = LoginForm()
        
        self.close()
        if self.logout_signal == 1:
            self.logout.show()
        else:
            self.show()
            
    def Select_Cam(self, cam_num):
        if cam_num == 'Select Camera...':
            self.DataReset()
        else:
            self.cam_num = cam_num[-1]
            self.cam_num = int(self.cam_num)
            self.cam_select = 1            
    
    def Start_btn(self):
        if self.cam_select == 1 and self.train == 1:
            rospy.init_node('Tracking_Cam', anonymous=True)
            Tracking_Camera(self.cam_num)
            self.DataReset()
            self.ComboBoxInit()
            print('Train_Cam')
        elif self.cam_select == 1:
            rospy.init_node('Normal_Cam', anonymous=True)
            Normal_Camera(self.cam_num)
            self.DataReset()
            self.ComboBoxInit()
            print('Normal_Cam')
        else:
            if self.train == 1 and self.video == 1:
                print('Train & video')
                Tracking_Video()
                self.DataReset()
                self.ComboBoxInit()
            elif self.train == 0 and self.video == 1:
                print('video only')
                Normal_Video()
                self.DataReset()   

    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.logout_signal=1
            sys.exit()
        else:
            self.logout_signal=2
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
            sys.exit()

class Normal_Video(QtWidgets.QDialog):
    def __init__(self):
        super(Normal_Video, self).__init__()
        self.setWindowTitle('Normal_Video')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)        
        
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
        self.video_speed = 0.01 # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
        while True:
            self.ret, frame = self.cap.read()
            if not self.ret:
                self.close()
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.label.setPixmap(pixmap)

            sleep(self.video_speed) 
            cv2.waitKey(0)
        
        self.cap.release()
    
    # def closeEvent(self, event):
        # quit_msg = "Want to exit?"
        # reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
# 
        # if reply == QtWidgets.QMessageBox.Yes:          
            # event.accept()
        # else:
            # event.ignore()
            # self.video = True
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cap.release()

class Tracking_Video(QtWidgets.QDialog):
    def __init__(self):
        super(Tracking_Video, self).__init__()
        self.setWindowTitle('Tracking_Video_Viewer')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        
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
            
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.label.setPixmap(pixmap)
            
            sleep(video_speed) 
            cv2.waitKey(0)
        
        self.cap.release()
    
    # def closeEvent(self, event):
        # quit_msg = "Want to exit?"
        # reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
# 
        # if reply == QtWidgets.QMessageBox.Yes:          
            # event.accept()
        # else:
            # event.ignore()
            # self.video = True
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cap.release()

class Camera_Control(QtWidgets.QDialog):
    def __init__(self):
        super(Camera_Control, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)        
        
        height = 90
        self.setFixedSize(Main_width, height)
        self.setGeometry(Position.x(), Position.y()+Main_height+10, Main_width, height)

        self.button_Up = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/up.png'),'', self)
        self.button_Up.resize(40, 40)
        self.button_Up.move(67.5, 5)
        self.button_Up.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Up.setFocusPolicy(Qt.ClickFocus)
        self.button_Up.clicked.connect(self.Manual_Up)

        self.button_Down = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/down.png'),'', self)
        self.button_Down.resize(40, 40)
        self.button_Down.move(67.5, 46)
        self.button_Down.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Down.setFocusPolicy(Qt.ClickFocus)
        self.button_Down.clicked.connect(self.Manual_Down)

        self.button_Right = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/right.png'),'', self)
        self.button_Right.resize(40, 40)
        self.button_Right.move(108, 46)
        self.button_Right.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Right.setFocusPolicy(Qt.ClickFocus)
        self.button_Right.clicked.connect(self.Manual_Right)

        self.button_Left = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/icon/Direction/left.png'),'', self)
        self.button_Left.resize(40, 40)
        self.button_Left.move(26.5, 46)
        self.button_Left.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Left.setFocusPolicy(Qt.ClickFocus)
        self.button_Left.clicked.connect(self.Manual_Left)

        self.show()
    
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

    def Manual_Up(self):
        y = 1
        pub = rospy.Publisher('manual_control', Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [0, y]
        pub.publish(my_msg)

    def Manual_Down(self):
        y = -1
        pub = rospy.Publisher('manual_control', Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [0, y]
        pub.publish(my_msg)

    def Manual_Right(self):
        x = 1
        pub = rospy.Publisher('manual_control', Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [x, 0]
        pub.publish(my_msg)

    def Manual_Left(self):
        x = -1
        pub = rospy.Publisher('manual_control', Int8MultiArray, queue_size=1)
        my_msg = Int8MultiArray()
        my_msg.data = [x, 0]
        pub.publish(my_msg)

class Cam_Btn_Set():
    def cam_btn_set(self):
        self.button_REC = QtWidgets.QPushButton('REC', self)
        self.button_REC.resize(65, 30)
        self.button_REC.move(430, 485)
        self.button_REC.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_REC.clicked.connect(self.ChangeREC)        

        self.button_Auto = QtWidgets.QPushButton('Auto', self)
        self.button_Auto.resize(65, 30)
        self.button_Auto.move(500, 485)
        self.button_Auto.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Auto.clicked.connect(self.ChangeAuto)

        self.button_Exit = QtWidgets.QPushButton('Exit', self)
        self.button_Exit.resize(65, 30)
        self.button_Exit.move(570, 485)
        self.button_Exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Exit.clicked.connect(self.Exit_cam)

        self.manual = 0
    
    def ChangeREC(self):
        self.button_REC.setText("Stop")
        self.button_REC.clicked.connect(self.ReturnREC)

    def ReturnREC(self):
        self.button_REC.setText("REC")
        self.button_REC.clicked.connect(self.ChangeREC)

    def ChangeAuto(self):
        self.button_Auto.setText("Manual")
        self.control = Camera_Control()
        self.manual = 1
        self.button_Auto.clicked.connect(self.ReturnAuto)

    def ReturnAuto(self):
        self.button_Auto.setText("Auto")
        self.control.close()
        self.button_Auto.clicked.connect(self.ChangeAuto)

    def Exit_cam(self):
        if self.manual == 1:
            self.close()
            self.control.close()
        else:
            self.close()

class Normal_Camera(QtWidgets.QDialog, Cam_Btn_Set):
    def __init__(self, camera):
        super(Normal_Camera, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.camera=camera  
        if camera == 1 :
            self._sub = rospy.Subscriber('/camera1/usb_cam1/image_raw', Image, self.callback, queue_size=1)
        elif camera == 2 :
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)
        
        self.bridge = CvBridge()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)

        self.cam_btn_set()

        self.show()    

    def callback(self, data):  
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
           
        self.label.resize(640, 480)
        img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB) 
        img = cv2.flip(img, 1)
        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        pixmap = pixmap.scaledToWidth(640)
        self.label.setPixmap(pixmap)

    # def closeEvent(self, event):
        # quit_msg = "Want to exit?"
        # reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
# 
        # if reply == QtWidgets.QMessageBox.Yes:
            # event.accept()
            # self.cv_image = False
        # else:
            # event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.Exit_cam()
            self.close()

class Tracking_Camera(QtWidgets.QDialog, Cam_Btn_Set):
    def __init__(self, camera):
        super(Tracking_Camera, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.camera=camera  
        if self.camera == 1 :
            self._sub = rospy.Subscriber('/camera1/usb_cam1/image_raw', Image, self.callback, queue_size=1)
        elif self.camera == 2 :
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)
        
        self.bridge = CvBridge()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)

        self.cam_btn_set()

        self.show()    

    def callback(self, data):  
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            
        faceCascade = cv2.CascadeClassifier(path1[0])
        self.cv_image = np.uint8(self.cv_image)
        self.faces = faceCascade.detectMultiScale(self.cv_image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
        self.f = 1
        if self.f == 1:
            for (x,y,w,h) in self.faces:
                cv2.rectangle(self.cv_image,(x,y),(x+w,y+h),(0,255,0),1)

                pub = rospy.Publisher('servo_x3', UInt16MultiArray, queue_size=10)
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
            print('11')
        else:
            print('333')
    
    # def closeEvent(self, event):
        # quit_msg = "Want to exit?"
        # reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
# 
        # if reply == QtWidgets.QMessageBox.Yes:
            # event.accept()
            # self.cv_image = False
        # else:
            # event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.f = 2
            print('2')
            self.Exit_cam()
            self.close()    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = LoginForm()
    init.show()
    sys.exit(app.exec_())