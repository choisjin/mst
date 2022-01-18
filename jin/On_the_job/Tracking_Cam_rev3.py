#-*- coding:utf-8 -*-
# GUI관련 모듈
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl

# Topic통신 관련 모듈
import os, sys, rospy, cv2, datetime
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray
from time import sleep

class Background_Set():                                                 # 배경화면 셋팅
    def background_set(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

class LoginForm(QtWidgets.QDialog, Background_Set):                     # 로그인 화면
    def __init__(self):                                 # 로그인 화면 셋팅
        super(LoginForm, self).__init__()
        
        self.background_set()
        
        width = 265
        height = 110
        self.setFixedSize(width, height)

        logo_label = QtWidgets.QLabel(self)
        logo_label.resize(100, 100)
        logo_label.move(160, 5)
        pixmap = QtGui.QPixmap('/home/jin/mst/jin/The_latest_package/Data/Image/Logo.png')
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

    def check_password(self):                           # ID, PW 확인
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
            sys.exit()        

class MainWindow(QtWidgets.QMainWindow, Background_Set):                # 기능선택 화면
    def __init__(self):                                 
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):                                   # 기능선택 화면 셋팅
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
        self.filePath = QtWidgets.QLineEdit(self)   # Train파일 경로 출력
        self.filePath.resize(Path_width, Path_height)
        self.filePath.setPlaceholderText('Train file name...')
        self.filePath.move(5, 75)

        self.videoPath = QtWidgets.QLineEdit(self)  # Video파일 경로 출력
        self.videoPath.resize(Path_width, Path_height)
        self.videoPath.setPlaceholderText('Video file name...')
        self.videoPath.move(5, 110)

        self.cb = QtWidgets.QComboBox(self)         # 카메라선택 ComboBox
        self.cb.resize(Path_width, Path_height)
        self.cb.move(5, 40)
        self.ComboBoxInit()
        self.cb.activated[str].connect(self.Select_Cam)
 
        self.train = 0
        self.video = 0
        self.cam_num = 0
        self.cam_select = 0
        self.logout_num = 0
        self.show()                                 # MainWindow 창 띄움

    def setToolBar(self):                               # 툴바 셋팅
        exitAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Toolbar/exit.png'), 'Exit', self)   # 툴바 아이콘 이미지 삽입
        exitAction.setShortcut('Ctrl+Q')            # 툴바 단축키 설정
        exitAction.setStatusTip('Exit')             # 상태창 메세지
        exitAction.setToolTip('Ctrl+Q')             # 툴팁 메세지
        exitAction.triggered.connect(self.exit_btn) # 툴바 클릭시 발생 이벤트

        logoutAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Toolbar/logout.png'), 'Logout', self)
        logoutAction.setShortcut('Ctrl+L')
        logoutAction.setStatusTip('Logout')
        logoutAction.setToolTip('Ctrl+L')
        logoutAction.triggered.connect(self.Logout)

        trainAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Toolbar/train_open.png'), 'Train', self)
        trainAction.setShortcut('Ctrl+T')
        trainAction.setStatusTip('Train File Open')
        trainAction.setToolTip('Ctrl+T')
        trainAction.triggered.connect(self.Insert_Train)
        
        videoAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Toolbar/video_open.png'), 'Video', self)
        videoAction.setShortcut('Ctrl+O')
        videoAction.setStatusTip('Video File Open')
        videoAction.setToolTip('Ctrl+O')
        videoAction.triggered.connect(self.Insert_Video)        
        
        stratAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Toolbar/play.png'), 'Start', self)
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

    def ComboBoxInit(self):                             # ComboBox 초기화
        self.cb.clear()                             # ComboBox 모두 지우기
        self.cam_num = 0
        combo_num = 2                               # ComboBox 생성 갯수
        combo_init = 0                              
        self.cb.setStyleSheet('QComboBox {background-color: #FFFFFF; color: Black;}')
        self.cb.addItem('Select Camera...')         # Default Item 생성
        
        while combo_init < combo_num :              # ComboBox 생성
            combo_init += 1
            self.cb.addItem('Camera%d' % combo_init) 

    def Insert_Train(self):                             # Train 파일 오픈
        global path1

        self.filePath.clear()
        path1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'xml File(*.xml)')
        self.filePath.setText(path1[0])
        
        if path1[0] == '':
            self.train = 0
        else:
            self.train = 1
    
    def Insert_Video(self):                             # Video 파일 오픈
        global path
        
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'mp4 File(*.mp4)')
        self.videoPath.setText(path[0])
 
        if path[0] == '':
            self.video = 0
        else:
            self.video = 1
            self.cam_select = 0
            self.ComboBoxInit()
    
    def Logout(self):                                   # Logout 기능
        quit_msg = "Want to Logout?"
        reply = QtWidgets.QMessageBox.question(self, 'Logout', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)        

        if reply == QtWidgets.QMessageBox.Yes:
            self.hide()
            init.show()

    def Select_Cam(self, cam_num):                      # Cam 선택 및 초기화
        self.videoPath.clear()
        
        if cam_num == 'Select Camera...':
            self.cam_select = 0
        else:
            self.cam_num = cam_num[-1]
            self.cam_num = int(self.cam_num)
            self.cam_select = 1            
    
    def Start_btn(self):                                # 기능 실행
        self.filePath.clear()
       
        if self.cam_select == 1 and self.train == 1:
            print('Train_Cam')
            self.train = 0
            Tracking_Camera(self.cam_num)
        elif self.cam_select == 1:
            print('Normal_Cam')
            Normal_Camera(self.cam_num)
        else:
            if self.train == 1 and self.video == 1:
                print('Train & video')
                self.train = 0
                Tracking_Video()
            elif self.train == 0 and self.video == 1:
                print('video only')
                Normal_Video()
    
    def exit_btn(self):
        self.close()
    
    def closeEvent(self, event):
        quit_msg = "Want to Exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        
        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeEvent(e)

    def __del__(self):
            print('All_sys_init...')

class Cam_Btn_Set():                                                    # Cam 조작 화면 버튼
    def cam_btn_set(self, camera):                      # Cam 조작 버튼 셋팅
        self.camera = camera
        
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

        self.manual = 1
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')         # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False                                   # 녹화 유무 변수 초기화
        self.button_Stop.setEnabled(False)
        self.now = datetime.datetime.now().strftime("MST_CAP-%Y-%m-%d-%H:%M:%S")

    def camera_cap(self):                               # Cam 캡쳐 기능
        print('Capture file save : ' + '/home/jin/mst/jin/The_latest_package/Storage_camera/')
        cv2.imwrite("/home/jin/mst/jin/The_latest_package/Storage_camera/" + str(self.now) + ".png", self.cv_image)

    def rec_strat(self):                                # Cam 녹화 시작
        self.button_REC.setEnabled(False)
        self.button_Stop.setEnabled(True)
        print('Recording Start!')
        self.record = True
        self.video = cv2.VideoWriter("/home/jin/mst/jin/The_latest_package/Storage_camera/" + str(self.now) + ".avi", self.fourcc, 20.0, (self.img.shape[1], self.img.shape[0]))        
        self.button_REC.setText("REC...")

    def rec_stop(self):                                 # Cam 녹화 중지
        self.button_REC.setEnabled(True)
        self.button_Stop.setEnabled(False)
        print('Record file save : '+ '/home/jin/mst/jin/The_latest_package/Storage_camera/')
        self.record = False
        self.video.release()
        self.button_REC.setText("REC")

    def controller_open(self):                          # Cam 수동조작 화면 오픈
        if self.manual == 1:
            self.button_Auto.setText("Manual")
            self.tracking_on_off = 0
            self.control = Camera_Control(self.camera)
            self.manual = 0
        else:
            self.button_Auto.setText("Auto")
            self.control.close()
            self.tracking_on_off = 1
            self.manual = 1

    def exit_cam(self):
        self.cam_init = Cam_init(self.camera)
        if self.manual == 0 and self.record == True:
            print('Recording Stop!')
            self.record = False
            self.tracking_on_off = 0
            self.control.close()
            self.finder.close()
            self.close() 
        elif self.record == True:
            print('Recording Stop!')
            self.record = False
            self.tracking_on_off = 0
            self.finder.close()
            self.close() 
        elif self.manual == 0:
            self.tracking_on_off = 0
            self.control.close()
            self.finder.close()
            self.close()                
        else:
            self.tracking_on_off = 0
            self.finder.close()
            self.close() 

class Cam_init(object):                                                 # Cam 위치 초기화
    def __init__(self, camera):
        super(Cam_init, self).__init__()
        self.camera = camera
        cam_init_pub = rospy.Publisher('cam_init_%d' % self.camera, UInt16MultiArray, queue_size=2)
        my_msg = UInt16MultiArray()
        my_msg.data = [320, 390]
        cam_init_pub.publish(my_msg)
        sleep(1)
        cam_init_pub.publish(my_msg)

class Video_Btn_Set():                                                  # Video 조작 화면 버튼
    def video_btn_set(self):                            # Video 조작 버튼 셋팅
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


        self.button_Video_Post_Skip = QtWidgets.QPushButton('-10', self)
        self.button_Video_Post_Skip.resize(30, 30)
        self.button_Video_Post_Skip.move(5, 485)
        self.button_Video_Post_Skip.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        #self.button_Video_Post_Skip.clicked.connect()

        self.button_Video_Rewind = QtWidgets.QPushButton('되', self)
        self.button_Video_Rewind.resize(30, 30)
        self.button_Video_Rewind.move(45, 485)
        self.button_Video_Rewind.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        #self.button_Video_Rewind.clicked.connect()

        self.button_Video_Start = QtWidgets.QPushButton('St', self)
        self.button_Video_Start.resize(30, 30)
        self.button_Video_Start.move(85, 485)
        self.button_Video_Start.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        #self.button_Video_Start.clicked.connect()

        self.button_Video_Fast_Forward = QtWidgets.QPushButton('빨', self)
        self.button_Video_Fast_Forward.resize(30, 30)
        self.button_Video_Fast_Forward.move(125, 485)
        self.button_Video_Fast_Forward.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        #self.button_Video_Fast_Forward.clicked.connect()

        self.button_Video_Next_Skip = QtWidgets.QPushButton('+10', self)
        self.button_Video_Next_Skip.resize(30, 30)
        self.button_Video_Next_Skip.move(165, 485)
        self.button_Video_Next_Skip.setStyleSheet('QPushButton {background-color: #000000; color: white;}')

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')       # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False 
        self.button_Stop.setEnabled(False)                  # 녹화 유무 변수 초기화
        self.now = datetime.datetime.now().strftime("MST_CAP-%Y-%m-%d-%H:%M:%S")

    def video_cap(self):                                # Video 캡쳐 기능
        print('Capture file save : ' + '/home/jin/mst/jin/The_latest_package/Storage_video/')
        cv2.imwrite("/home/jin/mst/jin/The_latest_package/Storage_video/" + str(self.now) + ".png", self.frame)

    def rec_strat(self):                                # Video 녹화 시작
        self.button_REC.setEnabled(False)
        self.button_Stop.setEnabled(True)
        print('Recording Start!')
        self.record = True
        self.video = cv2.VideoWriter("/home/jin/mst/jin/The_latest_package/Storage_video/" + str(self.now) + ".avi", self.fourcc, 30.0, (self.frame.shape[1], self.frame.shape[0]))        
        self.button_REC.setText("REC...")

    def rec_stop(self):                                 # Video 녹화 중지
        self.button_REC.setEnabled(True)
        self.button_Stop.setEnabled(False)
        print('Record file save : '+ '/home/jin/mst/jin/The_latest_package/Storage_video/')
        self.record = False
        self.video.release()
        self.button_REC.setText("REC")

    def exit_cam(self):
        if self.record == True:
            print('Recording Stop!')
            self.record = False
            self.video.release()
            self.cap.release()
            self.finder.close()
            global normal_check
            normal_check = 0
            self.close()
        else:
            self.cap.release()
            self.finder.close()
            normal_check = 0
            self.close()

class Tracking_Finder(QtWidgets.QDialog, Background_Set):               # 객체 인식시 로그 발생창
    def __init__(self):
        super(Tracking_Finder, self).__init__()
        self.background_set()

        height = 250
        self.setFixedSize(Main_width, height)
        self.setGeometry(Position.x(), Position.y()+Main_height+10, Main_width, height)

        self.tb = QtWidgets.QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.tb, 0)
        self.setLayout(vbox)
        self.show()

    def append_text(self, args):
        self.tb.append(args)

class Video_Controller():
    def video_control_btn_set(self):
        self.lab_time = QtWidgets.QLabel('00:00', self)
        self.lab_time.resize(60, 20)
        self.lab_time.move(5, 460)
        self.lab_time.setStyleSheet("background-color: #000000;" "color: white;")
        
        self.Video_Slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.Video_Slider.resize(630, 5)
        self.Video_Slider.move(70, 470)
        self.Video_Slider.setStyleSheet("background-color: #000000;" "color: white;")
        
        #self.Video_Slider.valueChanged(self.getDuration)
        #self.Video_Slider.valueChanged(self.getPosition)
        
        #self.Video_Slider.valueChanged(self.getDuration())
        #self.Video_Slider.setValue(self.getPosition())
        #self.Video_Slider.sliderMoved.connect(self.updatePosition())

    def getDuration(self):
        length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.Video_Slider.setRange(0, length)
        self.Video_Slider.setEnabled(True)
        self.displayTime(self.cap)
    
    def getPosition(self, p):
        self.Video_Slider.setValue(p)
        self.displayTime(self.Video_Slider.setMaximum()-p)
    
    def displayTime(self):
        run_time = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        minutes = int(run_time/60000)
        seconds = int((run_time-minutes*60000)/1000)
        self.lab_time.setText('{}:{}'.format(minutes, seconds))
    
    def updatePosition(self, v):
        self.Video_Slider.setValue(v)
        self.displayTime(self.Video_Slider.setMaximum()-v)

class Normal_Video(QtWidgets.QDialog, Video_Btn_Set, Video_Controller, Background_Set):   # Only Video 조작 화면
    def __init__(self):                                 # Video 화면 셋팅
        super(Normal_Video, self).__init__()
        self.background_set()

        self.finder = Tracking_Finder()
        self.finder.close()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)

        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)

        self.lab_time = QtWidgets.QLabel('00:00:00 // 00:00:00', self)
        self.lab_time.resize(100, 20)
        self.lab_time.move(5, 460)
        self.lab_time.setStyleSheet("background-color: #000000;" "color: white;")
        
        self.Video_Slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.Video_Slider.resize(520, 10)
        self.Video_Slider.move(110, 465)
        #self.Video_Slider.setStyleSheet("background-color: #000000;" "color: white;")

        self.video_btn_set()
        self.show()
        self.video_convert()

    def video_convert(self):                            # Video 데이터 Qt 데이터로 변환
        self.cap = cv2.VideoCapture(path[0])
        
        self.video_speed = 0.0                           # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
        self.Video_Slider.sliderMoved.connect(self.slider_change)
        #self.Video_Slider.valueChanged.connect(self.slider_change)
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.Video_Slider.setRange(0, self.total_frame)
        self.Video_Slider.setEnabled(True)
        
        self.run_time = self.total_frame/self.fps
        run_hours = int(self.run_time/3600)
        run_minutes = int((self.run_time-run_hours*3600)/60)
        self.run_seconds = int(self.run_time-(run_hours*3600)-(run_minutes*60))

        while True:
            self.ret, self.frame = self.cap.read()
            if self.fps == 0:
                pass
            else:
                play_time = self.cap.get(cv2.CAP_PROP_POS_MSEC)
                hour = int(play_time/60000/60000)
                minutes = int(play_time/60000)
                seconds = int((play_time-minutes*60000)/1000)

                self.Video_Slider.setValue(self.total_frame/self.run_time*seconds)
                self.lab_time.setText('{}:{}:{} // {}:{}:{}'.format(hour, minutes, seconds, run_hours, run_minutes, self.run_seconds))

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
            self.pixmap = QtGui.QPixmap.fromImage(qImg)
            self.pixmap = self.pixmap.scaledToWidth(640)
            self.pixmap = self.pixmap.scaledToHeight(480)
            self.label.setPixmap(self.pixmap)
            sleep(self.video_speed)

            if self.record == True:
                self.video.write(self.frame)

            cv2.waitKey(1)

        self.cap.release()
    
    def slider_change(self, v):
        print(v)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, v);
        #self.cap.set(cv2.CAP_PROP_POS_AVI_RATIO, v);
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            if self.record == True:
                print('Recording Stop!')
                self.record = False
                self.finder.close()
                self.close()
                self.video.release()
                self.cap.release()
            else:
                self.close()
                self.cap.release()
                self.finder.close()

    def __del__(self):
        print('Video_sys_init...')

class Tracking_Video(QtWidgets.QDialog, Video_Btn_Set, Background_Set): # Train & Video 조작 화면
    def __init__(self):                                 # Train & Video 화면 셋팅
        super(Tracking_Video, self).__init__()
        self.background_set()

        self.finder = Tracking_Finder()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)

        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)

        self.video_btn_set()
        self.show()
        self.video_convert()

    def video_convert(self):                            # Video 데이터 Qt 데이터로 변환
        self.cap = cv2.VideoCapture(path[0])
        self.video_speed = 0.015 # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
        faceCascade = cv2.CascadeClassifier(path1[0])
        face_count = 0

        while True:
            self.ret, self.frame = self.cap.read()
            faces = faceCascade.detectMultiScale(self.frame, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
            now = datetime.datetime.now().strftime("%m-%d-%H:%M:%S")

            if not self.ret:
                if self.record == True:
                    print('Recording Stop!')
                    self.record = False
                    self.video.release()
                    self.cap.release()
                    self.close()
                else:
                    self.cap.release()
                    self.close()
                break

            if faces == ():
                face_count = 0

            for (x,y,w,h) in faces:
                face_count += 1
                if face_count == 50:
                    getmsg = now
                    self.finder.append_text(getmsg)
                    face_count = 0
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),1)

            if self.record == True:
                self.video.write(self.frame)

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

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            if self.record == True:
                print('Recording Stop!')
                self.record = False
                self.video.release()
                self.cap.release()
                self.finder.close()
                self.close()
            else:
                self.cap.release()
                self.finder.close()
                self.close()

    def __del__(self):
        print('Video_sys_init...')

class Normal_Camera(QtWidgets.QDialog, Cam_Btn_Set, Background_Set):    # Only Cam 조작 화면
    def __init__(self, camera):                         # Only Cam 화면 셋팅 및 Cam데이터 Subs
        super(Normal_Camera, self).__init__()
        self.background_set()

        self.finder = Tracking_Finder()
        self.finder.close()
        
        self.camera = camera  
        rospy.init_node('cam_sub%s' % camera, anonymous = False)
        self._sub = rospy.Subscriber('/cam_num%s' % camera, Image, self.callback, queue_size=1)
        
        self.bridge = CvBridge()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)
        global normal_check
        normal_check = 1

        self.cam_btn_set(camera)
        self.show()    

    def callback(self, data):                           # Cam 데이터 Qt 변환
        self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        if self.record == True:
            self.video.write(self.cv_image)
        
        self.label.resize(640, 480)
        self.img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB) 
        self.img = cv2.flip(self.img, 1)
        h,w,c = self.img.shape
        qImg = QtGui.QImage(self.img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        pixmap = pixmap.scaledToWidth(640)
        self.label.setPixmap(pixmap)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cam_init = Cam_init(self.camera)
            self._sub.unregister()
            if self.manual == 0 and self.record == True:
                print('Recording Stop!')
                self.record = False
                self.control.close()
                self.finder.close()
                global normal_check
                normal_check = 0
                self.close() 
            elif self.record == True:
                print('Recording Stop!')
                self.record = False
                self.finder.close()
                normal_check = 0
                self.close() 
            elif self.manual == 0:
                self.control.close()
                self.finder.close()
                normal_check = 0
                self.close()                
            else:
                self.finder.close()
                normal_check = 0
                self.close()

    def __del__(self):
        print('Camera_sys_init...')

class Tracking_Camera(QtWidgets.QDialog, Cam_Btn_Set, Background_Set):  # Train & Video 조작 화면
    def __init__(self, camera):                         # Train & Video 화면 셋팅 및 Cam데이터 Subs
        super(Tracking_Camera, self).__init__()
        self.background_set()

        self.finder = Tracking_Finder()

        self.camera = camera
        rospy.init_node('cam_sub%s' % camera, anonymous = False)
        self._sub = rospy.Subscriber('/cam_num%s' % camera, Image, self.callback, queue_size=1)

        self.bridge = CvBridge()

        width = 640
        height = 480 + 40
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)

        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)

        self.cam_btn_set(camera)

        self.show()

        global normal_check
        normal_check = 0

        self.servo_x = 320
        self.servo_y = 390

        self.tracking_on_off = 1

        self.face_count = 0
        self.init_count = 0

    def callback(self, data):                           # Cam 데이터 Qt 데이터로 변환 및 객체 인식에 따른 모터 구동 Pub
        midScreenX = 320/2    # 화면 x축 중앙
        midScreenY = 240/2    # 화면 y축 중앙
        midScreenWindow = 17  # 객체를 인식한 사각형이 중앙에서 벗어날 수 있는 여유 값

        self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.cv_image = np.uint8(self.cv_image)
        faceCascade = cv2.CascadeClassifier(path1[0])
        faces = faceCascade.detectMultiScale(self.cv_image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))

        if faces == ():
                self.face_count = 0    

        for (x,y,w,h) in faces:
            self.face_count += 1

            if self.face_count == 50:
                now = datetime.datetime.now().strftime("%m-%d-%H:%M:%S")
                getmsg = now
                self.finder.append_text(getmsg)
                self.face_count = 0
            elif faces == ():
                self.face_count = 0
           
            cv2.rectangle(self.cv_image,(x,y),(x+w,y+h),(0,255,0),1)

            if self.tracking_on_off == 1:
                self.servo_x1 = int(x+w/2)
                self.servo_y1 = int(y+h/2)

                if self.servo_x1 < midScreenX-midScreenWindow:
                    self.servo_x += 1
                elif self.servo_x1 > midScreenX+midScreenWindow:
                    self.servo_x -= 1
                if self.servo_y1 > midScreenY+midScreenWindow:
                    self.servo_y += 1
                elif self.servo_y1 < midScreenY-midScreenWindow:
                    self.servo_y -= 1

                if self.servo_x > 500:
                    print('Max_X_value!!!')
                    self.servo_x = 500
                elif self.servo_y < 170:
                    print('Min_X_value!!!')
                    self.servo_x = 170
                if self.servo_y > 450 :
                    print('Max_Y_value!!!')
                    self.servo_y = 450
                elif self.servo_y < 310:
                    print('Min_Y_value!!!')
                    self.servo_y = 310

                self.cam_tracking_pub = rospy.Publisher('cam_tracking%d' % self.camera, UInt16MultiArray, queue_size=1)
                self.my_msg = UInt16MultiArray()
                self.my_msg.data = [self.servo_x, self.servo_y]
                self.cam_tracking_pub.publish(self.my_msg)

                global manual_servo_x
                global manual_servo_y
                manual_servo_x = self.servo_x
                manual_servo_y = self.servo_y
            else :
                pass

        manual_servo_x = self.servo_x
        manual_servo_y = self.servo_y

        if self.tracking_on_off == 0:
            self.manual_subs = rospy.Subscriber('/manual_control_%s' % self.camera,  UInt16MultiArray, self.callback_manual, queue_size=1)
                    
        if self.record == True:
            self.video.write(self.cv_image)

        self.label.resize(640, 480)
        self.img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
        self.img = cv2.flip(self.img, 1)
        h,w,c = self.img.shape
        qImg = QtGui.QImage(self.img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        pixmap = pixmap.scaledToWidth(640)
        self.label.setPixmap(pixmap)

    def callback_manual(self, manual_msg):
                    self.servo_x = manual_msg.data[0]
                    self.servo_y = manual_msg.data[1]

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cam_init = Cam_init(self.camera)
            self._sub.unregister()
            self.cam_tracking_pub.unregister()
            if self.manual == 0 and self.record == True:
                print('Recording Stop!')
                self.record = False
                self.tracking_on_off = 0
                self.control.close()
                self.finder.close()
                self.close()
            elif self.record == True:
                print('Recording Stop!')
                self.record = False
                self.tracking_on_off = 0
                self.finder.close()
                self.close()
            elif self.manual == 0:
                self.control.close()
                self.tracking_on_off = 0
                self.finder.close()
                self.close()
            else:
                self.tracking_on_off = 0
                self.finder.close()
                self.close()
    
    def __del__(self):
        print('Camera_sys_init...')
        
class Camera_Control(QtWidgets.QDialog, Background_Set):                # Cam 수동조작 & 방향키
    def __init__(self, camera):             # Cam 수동조작 화면 셋팅
        super(Camera_Control, self).__init__()
        self.background_set()

        self.camera = camera
        print('Cam_Control_Num : %d' % self.camera)

        height = 90
        self.setFixedSize(Main_width, height)
        self.setGeometry(Position.x(), Position.y()+520-height, Main_width, height)

        self.button_Up = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/up.png'),'', self)
        self.button_Up.resize(40, 40)
        self.button_Up.move(67.5, 5)
        self.button_Up.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Up.setFocusPolicy(Qt.NoFocus)
        self.button_Up.clicked.connect(lambda:self.Manual(1))

        self.button_Down = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/down.png'),'', self)
        self.button_Down.resize(40, 40)
        self.button_Down.move(67.5, 46)
        self.button_Down.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Down.setFocusPolicy(Qt.NoFocus)
        self.button_Down.clicked.connect(lambda:self.Manual(2))

        self.button_Right = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/right.png'),'', self)
        self.button_Right.resize(40, 40)
        self.button_Right.move(108, 46)
        self.button_Right.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Right.setFocusPolicy(Qt.NoFocus)
        self.button_Right.clicked.connect(lambda:self.Manual(3))

        self.button_Left = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/left.png'),'', self)
        self.button_Left.resize(40, 40)
        self.button_Left.move(26.5, 46)
        self.button_Left.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Left.setFocusPolicy(Qt.NoFocus)
        self.button_Left.clicked.connect(lambda:self.Manual(4))
        
        if normal_check == 1:
            self.servo_x = 320
            self.servo_y = 390
        else:
            pass
        self.show()

    def Manual(self, args):                             # Cam 수동조작 Topic 발행
        self.args = args
        if not normal_check == 1:
            self.servo_x = manual_servo_x
            self.servo_y = manual_servo_y
        else:
            pass 

        if self.args == 1:
             self.servo_y -= 1
        elif self.args == 2:
            self.servo_y += 1
        elif self.args == 3:
            self.servo_x += 1
        elif self.args == 4:
            self.servo_x -= 1
        
        if self.servo_x > 500:
            print('Max_X_value!!!')
            self.servo_x = 500
        elif self.servo_x < 200:
            print('Min_X_value!!!')
            self.servo_x = 200

        if self.servo_y > 450 :
            print('Max_Y_value!!!')
            self.servo_y = 450
        elif self.servo_y < 310:
            print('Min_Y_value!!!')
            self.servo_y = 310
        
        self.manual_control_pub = rospy.Publisher('manual_control_%d' % self.camera, UInt16MultiArray, queue_size=1)
        my_msg = UInt16MultiArray()
        my_msg.data = [self.servo_x, self.servo_y]
        self.manual_control_pub.publish(my_msg)

    def keyPressEvent(self, k):                         # Cam 키보드 조작
        if k.key() == Qt.Key_Escape:
            self.close()
        elif k.key() == Qt.Key_Up:
           self.Manual(1)
        elif k.key() == Qt.Key_Down:
            self.Manual(2)
        elif k.key() == Qt.Key_Right:
            self.Manual(3)
        elif k.key() == Qt.Key_Left:
            self.Manual(4)

    def __del__(self):
        print('Controller_init...')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = LoginForm()
    init.show()
    sys.exit(app.exec_())