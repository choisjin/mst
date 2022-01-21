#-*- coding:utf-8 -*-
# GUI관련 모듈
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

# Topic통신 관련 모듈
import os, sys, rospy, cv2, datetime, time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16MultiArray
from time import sleep
import pymysql



class Background_Set():                                                 # 배경화면 셋팅
    def background_set(self):
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

class LoginForm(QtWidgets.QDialog, Background_Set):                     # 로그인 화면
    def __init__(self):                                 # 로그인 화면 셋팅
        super(LoginForm, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
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
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.background_set()
        
        Main_width = 175
        Main_height = 175
        self.setFixedSize(Main_width, Main_height)
        self.setGeometry(Position.x(), Position.y(), Main_width, Main_height)
        self.setToolBar()      

        Path_width = 165
        Path_height = 25
        self.filePath = QtWidgets.QLineEdit(self)   # Train파일 경로 출력
        self.filePath.resize(Path_width, Path_height)
        self.filePath.setPlaceholderText('Train file name...')
        self.filePath.move(5, 70)

        self.videoPath = QtWidgets.QLineEdit(self)  # Video파일 경로 출력
        self.videoPath.resize(Path_width, Path_height)
        self.videoPath.setPlaceholderText('Video file name...')
        self.videoPath.move(5, 130)

        self.cb = QtWidgets.QComboBox(self)         # 카메라선택 ComboBox
        self.cb.resize(Path_width, Path_height)
        self.cb.move(5, 40)
        self.ComboBoxInit()
        self.cb.activated[str].connect(self.Select_Cam)
 
        self.peple_select_cb = QtWidgets.QComboBox(self)         # 카메라선택 ComboBox
        self.peple_select_cb.resize(Path_width, Path_height)
        self.peple_select_cb.move(5, 100)
        self.People_ComboBoxInit()
        self.peple_select_cb.activated[str].connect(self.Select_People)

        self.people_select = 0
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
        need_num = 2
        combo_num = 0                               # ComboBox 생성 갯수                              
        self.cb.setStyleSheet('QComboBox {background-color: #FFFFFF; color: Black;}')
        self.cb.addItem('Select Camera...')         # Default Item 생성
        for combo_num in range(1, need_num+1):              # ComboBox 생성
            self.cb.addItem('Camera%d' % combo_num) 

    def People_ComboBoxInit(self):
        self.peple_select_cb.clear()
        self.peple_select_cb.setStyleSheet('QComboBox {background-color: #FFFFFF; color: Black;}')
        self.peple_select_cb.addItem('Select People...')
        self.peple_select_cb.addItem('Man')
        self.peple_select_cb.addItem('Woman')
        self.peple_select_cb.addItem('Kid')

    def Insert_Train(self):                             # Train 파일 오픈
        global path1

        self.filePath.clear()
        path1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'mp4 File(*.xml)') #################################### 파일 확장자 변경 한태민
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
    
    def Select_People(self, people):
        if people == 'Select People...':
            self.people_select = 0
        elif people == 'Man':
            self.people_select = 1
        elif people == 'Woman':
            self.people_select = 2
        elif people == 'Kid':
            self.people_select = 3

    def Start_btn(self):                                # 기능 실행
        self.filePath.clear()

        if self.cam_select == 1 and self.train == 1:
            print('Train_Cam')
            self.train = 0
            self.peple_select_cb.clear()
            self.People_ComboBoxInit()
            Tracking_Camera(self.cam_num, self.people_select)
        elif self.cam_select == 1:
            print('Normal_Cam')
            Normal_Camera(self.cam_num)
        else:
            if self.train == 1 and self.video == 1:
                print('Train & video')
                self.train = 0
                self.peple_select_cb.clear()
                self.People_ComboBoxInit()
                Tracking_Video(self.cam_num, self.people_select)
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
        
        self.button_Auto = QtWidgets.QPushButton('', self)
        self.button_Auto.resize(32, 32)
        self.button_Auto.move(440, 5)
        self.button_Auto.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/joypad.png'); border: none;")
        self.button_Auto.clicked.connect(self.controller_open)

        self.button_Finder = QtWidgets.QPushButton('', self)
        self.button_Finder.resize(32, 32)
        self.button_Finder.move(477, 5)
        self.button_Finder.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/finder.png'); border: none;")
        self.button_Finder.clicked.connect(self.finder_open)

        self.button_Cap = QtWidgets.QPushButton('', self)
        self.button_Cap.resize(32, 32)
        self.button_Cap.move(519, 5)
        self.button_Cap.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/capture.png'); border: none;")
        self.button_Cap.clicked.connect(self.camera_cap)

        self.button_REC = QtWidgets.QPushButton('', self)
        self.button_REC.resize(32, 32)
        self.button_REC.move(561, 5)
        self.button_REC.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/REC.png'); border: none;")
        self.button_REC.clicked.connect(self.rec)     

        self.button_Exit = QtWidgets.QPushButton('', self)
        self.button_Exit.resize(32, 32)
        self.button_Exit.move(603, 5)
        self.button_Exit.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/exit.png'); border: none;")
        self.button_Exit.clicked.connect(self.exit_cam)

        global cam_window_x
        global cam_window_y
        self.cam_window = self.pos()
        cam_window_x = self.cam_window.x()
        cam_window_y = self.cam_window.y()

        self.control = 0
        self.finder = 0
        self.manual = 1
        self.finder_status = 1
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')         # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False                                   # 녹화 유무 변수 초기화
        self.start_btn_status = 0
        self.now = datetime.datetime.now().strftime("MST_CAP-%Y-%m-%d-%H:%M:%S")

    def camera_cap(self):                               # Cam 캡쳐 기능
        print('Capture file save : ' + '/home/jin/mst/jin/The_latest_package/Storage_camera/')
        cv2.imwrite("/home/jin/mst/jin/The_latest_package/Storage_camera/" + str(self.now) + ".png", self.cv_image)

    def rec(self):                                      # Video 녹화 시작/중지
        if self.start_btn_status == 0:
            self.button_REC.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/STOP.png'); border: none;")
            print('Recording Start!')
            self.record = True
            self.video = cv2.VideoWriter("/home/jin/mst/jin/The_latest_package/Storage_camera/" + str(self.now) + ".avi", self.fourcc, 30.0, (self.cv_image.shape[1], self.cv_image.shape[0]))        
            self.start_btn_status = 1
        else:
            self.button_REC.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/REC.png'); border: none;")
            print('Record file save : '+ '/home/jin/mst/jin/The_latest_package/Storage_camera/')
            self.record = False
            self.video.release()
            self.start_btn_status = 0

    def controller_open(self):                          # Cam 수동조작 화면 오픈
        if self.manual == 1:
            self.tracking_on_off = 0
            self.control = Camera_Control(self.camera)
            self.manual = 0
        else:
            self.control.close()
            self.tracking_on_off = 1
            self.manual = 1

    def finder_open(self):                              # 객체 추적 로그 화면 오픈
        if self.finder_status == 1:
            self.finder = Tracking_Finder(self.camera)
            self.finder_status = 0
        else:
            self.finder.close()
            self.finder_status = 1

    def exit_cam(self):
        self.cam_init = Cam_init(self.camera)
        self._sub.unregister()
        if self.manual == 0 and self.record == True and self.finder_status == 0:
            print('Recording Stop!')
            self.record = False
            self.tracking_on_off = 0
            self.control.close()
            self.finder.close()
            self.close()
        elif self.manual == 0 and self.record == True:
            print('Recording Stop!')
            self.record = False
            self.tracking_on_off = 0
            self.control.close()
            self.close()
        elif self.record == True and self.finder_status == 0:
            print('Recording Stop!')
            self.record = False
            self.finder.close()
            self.close()
        elif self.manual == 0 and self.finder_status == 0:
            self.tracking_on_off = 0
            self.control.close()
            self.finder.close()
            self.close()
        elif self.finder_status == 0:
            self.finder.close()
            self.close()
        elif self.record == True:
            print('Recording Stop!')
            self.record = False
            self.tracking_on_off = 0
            self.close()
        elif self.manual == 0:
            self.control.close()
            self.tracking_on_off = 0
            self.close()
        else:
            self.tracking_on_off = 0
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
    def video_btn_set(self, camera):                            # Video 조작 버튼 셋팅
        self.camera = camera
        self.button_video_speed_down = QtWidgets.QPushButton('', self)
        self.button_video_speed_down.resize(32, 32)
        self.button_video_speed_down.move(5, 5)
        self.button_video_speed_down.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/minor10.png'); border: none;")
        self.button_video_speed_down.clicked.connect(self.video_speed_down)
        
        self.button_video_speed_up = QtWidgets.QPushButton('', self)
        self.button_video_speed_up.resize(32, 32)
        self.button_video_speed_up.move(42, 5)
        self.button_video_speed_up.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/plus10.png'); border: none;")
        self.button_video_speed_up.clicked.connect(self.video_speed_up)
        
        self.button_Video_Start = QtWidgets.QPushButton('', self)
        self.button_Video_Start.resize(32, 32)
        self.button_Video_Start.move(79, 5)
        self.button_Video_Start.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/pause_b.png'); border: none;")
        self.button_Video_Start.clicked.connect(self.video_start_stop)

        self.button_Finder = QtWidgets.QPushButton('', self)
        self.button_Finder.resize(32, 32)
        self.button_Finder.move(482, 5)
        self.button_Finder.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/finder.png'); border: none;")
        self.button_Finder.clicked.connect(self.finder_open)

        self.button_Cap = QtWidgets.QPushButton('', self)
        self.button_Cap.resize(32, 32)
        self.button_Cap.move(519, 5)
        self.button_Cap.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/capture.png'); border: none;")
        self.button_Cap.clicked.connect(self.video_cap)

        self.button_REC = QtWidgets.QPushButton('', self)
        self.button_REC.resize(32, 32)
        self.button_REC.move(561, 5)
        self.button_REC.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/REC.png'); border: none;")
        self.button_REC.clicked.connect(self.rec)     

        self.button_Exit = QtWidgets.QPushButton('', self)
        self.button_Exit.resize(32, 32)
        self.button_Exit.move(603, 5)
        self.button_Exit.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/exit.png'); border: none;")
        self.button_Exit.clicked.connect(self.exit_cam)

        global Video_window_x
        global Video_window_y
        self.Video_window = self.pos()
        Video_window_x = self.Video_window.x()
        Video_window_y = self.Video_window.y()

        self.finder = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')       # 인코딩 방식 설정 FourCC(Four Character Code)
        self.record = False 
        self.rec_btn_status = 0
        self.start_btn_status = 0
        self.finder_status = 1
        self.now = datetime.datetime.now().strftime("MST_CAP-%Y-%m-%d-%H:%M:%S")

    def video_speed_up(self):                           # Video 속도 빠르게
        print('speed up!')
        self.video_speed -= 0.005
        
        if self.video_speed < 0.006:
            self.video_speed = 0.005 
            print('Max speed')
    
    def video_speed_down(self):                         # Video 속도 느리게
        print('speed down!')
        self.video_speed += 0.005

        if self.video_speed > 0.06:
            self.video_speed = 0.06
            print('Min speed')

    def video_start_stop(self):                         # Video 녹화 시작
        if self.start_btn_status == 0:
            self.button_Video_Start.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/play.png'); border: none;")
            self.pause= True
            self.stop_start_status = 1
            print('Video Stop!')
            self.start_btn_status = 1
        else:
            self.button_Video_Start.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/pause_b.png'); border: none;")
            self.pause= False
            self.stop_start_status = 0
            print('Video Start!')
            self.start_btn_status = 0

    def finder_open(self):                              # 객체 추적 로그 화면 오픈
        if self.finder_status == 1:
            self.finder = Tracking_Finder(self.camera)
            self.finder_status = 0
        else:
            self.finder_status = 1
            self.finder.close()

    def video_cap(self):                                # Video 캡쳐 기능
        print('Capture file save : ' + '/home/jin/mst/jin/The_latest_package/Storage_video/')
        cv2.imwrite("/home/jin/mst/jin/The_latest_package/Storage_video/" + str(self.now) + ".png", self.frame)

    def rec(self):                                      # Video 녹화 시작/중지
        if self.rec_btn_status == 0:
            self.button_REC.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/STOP.png'); border: none;")
            print('Recording Start!')
            self.record = True
            self.video = cv2.VideoWriter("/home/jin/mst/jin/The_latest_package/Storage_video/" + str(self.now) + ".avi", self.fourcc, 30.0, (self.frame.shape[1], self.frame.shape[0]))        
            self.rec_btn_status = 1
        else:
            self.button_REC.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/REC.png'); border: none;")
            print('Record file save : '+ '/home/jin/mst/jin/The_latest_package/Storage_video/')
            self.record = False
            self.video.release()
            self.rec_btn_status = 0

    def exit_cam(self):
        if self.record == True and self.finder_status == 0:
            print('Recording Stop!')
            self.record = False
            self.video.release()
            self.cap.release()
            self.finder.close()
            #self.people_select = 0
            self.close()
        elif self.record == True:
            print('Recording Stop!')
            self.record = False
            self.video.release()
            self.cap.release()
            #self.people_select = 0
            self.close()
        elif self.finder_status == 0:
            self.cap.release()
            self.finder.close()
            #self.people_select = 0
            self.close()
        else:
            self.cap.release()
            #self.people_select = 0
            self.close()

class Tracking_Finder(QtWidgets.QDialog, Background_Set):               # 객체 인식시 로그 확인 화면
    def __init__(self, camera):
        super(Tracking_Finder, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.background_set()

        width = 175
        height = 205
        self.setFixedSize(width, height)
        if not camera == 0:
            self.setGeometry(cam_window_x + 650, cam_window_y + 180, width, height)
        else:
            self.setGeometry(Video_window_x + 650, Video_window_y + 180, width, height)
        self.tb = QtWidgets.QTextEdit()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.tb, 0)
        self.setLayout(vbox)
        self.show()

    def append_text(self, args):
        self.tb.append(args)

class Normal_Video(QtWidgets.QDialog, Video_Btn_Set, Background_Set):   # Only Video 조작 화면
    def __init__(self):                                 # Video 화면 셋팅
        super(Normal_Video, self).__init__()
        self.background_set()

        width = 640
        height = 480
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)

        self.video_speed = 0.02                         # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
        self.waitkey = 1
        self.pause = False
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0, 0)

        self.lab_time = QtWidgets.QLabel('', self)
        self.lab_time.resize(100, 20)
        self.lab_time.move(114, 1)
        self.lab_time.setStyleSheet("font: 8pt;" "font-weight: bold;" "color: black;")
        
        self.Video_Slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.Video_Slider.resize(363, 10)
        self.Video_Slider.move(114, 17)

        self.video_btn_set()
        self.button_Finder.setEnabled(False)
        self.button_Finder.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/finder_none.png'); border: none;")
        self.show()
        self.video_convert()

    def video_convert(self):                            # Video 데이터 Qt 데이터로 변환
        self.cap = cv2.VideoCapture(path[0])

        self.Video_Slider.sliderMoved.connect(self.slider_change)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.Video_Slider.setRange(0, self.total_frame)
        self.Video_Slider.setEnabled(True)
        
        while True:
            self.ret, self.frame = self.cap.read()
            
            if not self.ret:
                if self.record == True:
                    print('Recording Stop!')
                    self.record = False
                    self.video.release()
                    self.close()
                else:
                    self.close()
                break
            
            if self.fps == 0:
                pass
            else:
                self.run_time = self.total_frame/self.fps
                run_hours = int(self.run_time/3600)
                run_minutes = int((self.run_time-run_hours*3600)/60)
                self.run_seconds = int(self.run_time-(run_hours*3600)-(run_minutes*60))
               
                play_time = self.cap.get(cv2.CAP_PROP_POS_MSEC)
                hour = int(play_time/3600000)
                minutes = int((play_time-hour*3600000)/60000)
                seconds = int((play_time-(hour*3600000)-(minutes*60000))/1000)
                count = play_time/1000

                self.Video_Slider.setValue(self.total_frame/self.run_time*count)
                self.lab_time.setText('{}:{}:{} / {}:{}:{}'.format(hour, minutes, seconds, run_hours, run_minutes, self.run_seconds))

            self.label.resize(640, 480)
            img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            self.pixmap = QtGui.QPixmap.fromImage(qImg)
            self.pixmap = self.pixmap.scaledToWidth(640)
            self.label.setPixmap(self.pixmap)
            sleep(self.video_speed)

            if self.record == True:
                self.video.write(self.frame)

            if self.pause == True:
                self.cap.set(1, self.total_frame/self.run_time*count)

            cv2.waitKey(1)

        self.cap.release()
    
    def slider_change(self, v):
        self.cap.set(1, v);
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            if self.record == True:
                print('Recording Stop!')
                self.record = False
                self.video.release()
                self.cap.release()
                self.close()
            else:
                self.close()
                self.cap.release()

    def __del__(self):
        print('Video_sys_init...')

class Tracking_Video(QtWidgets.QDialog, Video_Btn_Set, Background_Set): # Train & Video 조작 화면
    def __init__(self, camera, people):                                 # Train & Video 화면 셋팅
        super(Tracking_Video, self).__init__()
        self.background_set()

        self.people_select = people

        width = 640
        height = 480
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)

        self.video_speed = 0.02                         # 배속조절 1프레임당 0.01초  0.02 = 0.5배속
        self.pause = False

        self.label = QtWidgets.QLabel(self)
        self.label.move(0, 0)

        self.lab_time = QtWidgets.QLabel('', self)
        self.lab_time.resize(100, 20)
        self.lab_time.move(114, 1)
        self.lab_time.setStyleSheet("font: 8pt;" "font-weight: bold;" "color: black;")

        self.Video_Slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.Video_Slider.resize(363, 10)
        self.Video_Slider.move(114, 17)
        
        self.video_btn_set(camera)
        self.show()
        self.video_convert()

    def video_convert(self):                            # Video 데이터 Qt 데이터로 변환 및 객체 추적 정보 Publish
        self.cap = cv2.VideoCapture(path[0])
        
        self.Video_Slider.sliderMoved.connect(self.slider_change)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.Video_Slider.setRange(0, self.total_frame)
        self.Video_Slider.setEnabled(True)

        faceCascade = cv2.CascadeClassifier(path1[0])
        
        self.face_count = 0
        self.stop_start_status = 0
        self.get_target = 0
        self.miss_count = 1
        self.catch_count = 0

        while True:
            self.ret, self.frame = self.cap.read()
            # scaleFactor = 작은 크기의 윈도우를 이용하여 객체를 검출하고 이후  scaleFactor값의 비율로 검색 윈도우를
            # 확대하면서 여러 번 객체를 검출(최소 1이상).
            # minNeighbors = 검출할 객체 영역에서 얼마나 많은 사각형이 중복되어 검출되어야 객체로 인지할지를 지정.
            # minSize, maxSize = 검출할 객체의 최소, 최대 크기
            faces = faceCascade.detectMultiScale(self.frame, scaleFactor=1.3, minNeighbors=4, minSize=(50, 50))
            now = datetime.datetime.now()

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
            
            if self.fps == 0:
                pass
            else:
                self.run_time = self.total_frame/self.fps
                run_hours = int(self.run_time/3600)
                run_minutes = int((self.run_time-run_hours*3600)/60)
                self.run_seconds = int(self.run_time-(run_hours*3600)-(run_minutes*60))
               
                play_time = self.cap.get(cv2.CAP_PROP_POS_MSEC)
                hours = int(play_time/3600000)
                minutes = int((play_time-hours*3600000)/60000)
                seconds = int((play_time-(hours*3600000)-(minutes*60000))/1000)
                count = play_time/1000

                self.Video_Slider.setValue(self.total_frame/self.run_time*count)
                self.lab_time.setText('{}:{}:{} / {}:{}:{}'.format(hours, minutes, seconds, run_hours, run_minutes, self.run_seconds))

            if faces == ():
                self.face_count = 0
                self.catch_count = 0
                if self.miss_count == 0:
                    self.get_target = 1
                    self.miss_count = 1
            
            #get_target = 0
            
            for (x,y,w,h) in faces:
                self.face_count += 1
                if self.face_count == 50 and not self.finder == 0 and self.stop_start_status == 0:
                    get_second = play_time/1000
                    getmsg = 'Catch_time\n' + '{}:{}:{}'.format(hours, minutes, seconds)
                    #getmsg1 = 'Elapsed_time\n' + str(now - datetime.datetime.fromtimestamp(os.path.getctime(path[0]) - (self.run_time) + get_second))
                    self.finder.append_text(getmsg)
                    #self.finder.append_text(getmsg1)
                    self.missing_count = 0
                    #get_target = 1

                if self.face_count > 50:
                    self.catch_count += 1
                    if self.catch_count == 50:
                        getmsg = 'Catching...'
                        self.finder.append_text(getmsg)
                        self.catch_count = 0
                        self.miss_count = 0
                        self.now1 = datetime.datetime.now() 
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),1)
                
            ################################################################ server 전송 부 ################################################################
            if self.get_target == 1:
                self.missing_count += 1
                if not self.people_select == 0:     
                    if self.missing_count%50 == 0:
                        getmsg = 'People_Num : ' + '%d' % self.people_select
                        self.finder.append_text(getmsg)
                        getmsg ='Missing_Time : ' + '{}:{}:{}'.format(hours, minutes, seconds)
                        self.finder.append_text(getmsg)
                        getmsg = 'Elapsed time\n' + str(now - datetime.datetime.fromtimestamp(os.path.getctime(path[0]) - (self.run_time) + get_second))
                        self.finder.append_text(getmsg)
                elif self.people_select == 0: 
                    if self.missing_count%50 == 0:
                        getmsg ='Missing_Time : ' + '{}:{}:{}'.format(hours, minutes, seconds)
                        self.finder.append_text(getmsg)
                        getmsg = 'Elapsed time\n' + str(now - datetime.datetime.fromtimestamp(os.path.getctime(path[0]) - (self.run_time) + get_second))
                        self.finder.append_text(getmsg)
            ################################################################ server 전송 부 ################################################################

            self.label.resize(640, 480)
            img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            pixmap = pixmap.scaledToWidth(640)
            self.label.setPixmap(pixmap)
            sleep(self.video_speed)

            if self.record == True:
                self.video.write(self.frame)

            if self.pause == True:
                self.cap.set(1, self.total_frame/self.run_time*count)

            cv2.waitKey(1)
        
        self.cap.release()
    
    def slider_change(self, v):
        self.cap.set(1, v);

    def moveEvent(self, event):                         # 화면 이동시 관련 창 동시 이동
        super(Tracking_Video, self).moveEvent(event)
        self.Video_window = self.pos()
        global Video_window_x
        global Video_window_y
        Video_window_x = self.Video_window.x()
        Video_window_y = self.Video_window.y()
        if not self.finder == 0:
            geo1 = self.geometry()
            geo1.moveTo(Video_window_x + 650, Video_window_y + 200)
            self.finder.setGeometry(geo1)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
           
            if self.record == True and self.finder_status == 0:
                print('Recording Stop!')
                self.record = False
                self.video.release()
                self.cap.release()
                self.finder.close()
                #people_select = 0
                self.close()
            elif self.record == True:
                print('Recording Stop!')
                self.record = False
                self.video.release()
                self.cap.release()
                #people_select = 0
                self.close()
            elif self.finder_status == 0:
                self.cap.release()
                self.finder.close()
                people_select = 0
                self.close()
            else:
                self.cap.release()
                #people_select = 0
                self.close()
    
    def __del__(self):
        print('Video_sys_init...')

class Normal_Camera(QtWidgets.QDialog, Cam_Btn_Set, Background_Set):    # Only Cam 조작 화면
    def __init__(self, camera):                         # Only Cam 화면 셋팅 및 Cam데이터 Subs
        super(Normal_Camera, self).__init__()
        self.background_set()
        
        self.camera = camera  
        rospy.init_node('cam_sub%s' % camera, anonymous = False)
        self._sub = rospy.Subscriber('/cam_num%s' % camera, Image, self.callback, queue_size=1)
        
        self.bridge = CvBridge()

        width = 640
        height = 480
        self.setFixedSize(width, height)
        self.setGeometry(Position.x()-width-10, Position.y(), width, height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)
        global normal_check
        normal_check = 1

        self.cam_btn_set(camera)
        self.button_Finder.setEnabled(False)
        self.button_Finder.setStyleSheet("background-image: url('/home/jin/mst/jin/The_latest_package/Data/Image/controller_btn/finder_none.png'); border: none;")
        self.show()    

    def callback(self, data):                           # Cam 데이터 Qt 데이터로 변환
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

    def moveEvent(self, event):                         # 화면 이동시 관련 창 동시 이동
        super(Normal_Camera, self).moveEvent(event)
        self.cam_window = self.pos()
        global cam_window_x
        global cam_window_y
        cam_window_x = self.cam_window.x()
        cam_window_y = self.cam_window.y() 
        if not self.control == 0: 
            geo = self.geometry()
            geo.moveTo(cam_window_x + 650, cam_window_y + 425)
            self.control.setGeometry(geo)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cam_init = Cam_init(self.camera)
            self._sub.unregister()
            if self.manual == 0 and self.record == True:
                print('Recording Stop!')
                self.record = False
                self.control.close()
                global normal_check
                normal_check = 0
                self.close() 
            elif self.record == True:
                print('Recording Stop!')
                self.record = False
                normal_check = 0
                self.close() 
            elif self.manual == 0:
                self.control.close()
                normal_check = 0
                self.close()                
            else:
                normal_check = 0
                self.close()

    def __del__(self):
        print('Camera_sys_init...')

class Tracking_Camera(QtWidgets.QDialog, Cam_Btn_Set, Background_Set):  # Train & Video 조작 화면
    def __init__(self, camera, people):                         # Train & Video 화면 셋팅 및 Cam데이터 Subs
        super(Tracking_Camera, self).__init__()
        self.background_set()
        
        # self.db = pymysql.Connect(host='3.34.190.68', user='mstpjt', password='1111', port = 52481, database='mstDB')
        # self.cursor = self.db.cursor()


        # self.query = "INSERT INTO mstDB (CAMERA_NUM, SORTATION, TIME) VALUES (%s,%s,%s)"

        self.camera = camera
        self.people_select = people
        rospy.init_node('cam_sub%s' % camera, anonymous = False)
        self._sub = rospy.Subscriber('/cam_num%s' % camera, Image, self.callback, queue_size=1)

        self.bridge = CvBridge()

        width = 640
        height = 480
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
        
        self.get_target = 0
        self.face_count = 0
        self.missing_count = 0
        self.miss_count = 1
        self.catch_count = 0
    
    def callback(self, data):                           # Cam 데이터 Qt 데이터로 변환 및 객체 인식에 따른 모터 구동 Pub
        midScreenX = 320/2    # 화면 x축 중앙
        midScreenY = 240/2    # 화면 y축 중앙
        midScreenWindow = 17  # 객체를 인식한 사각형이 중앙에서 벗어날 수 있는 여유 값

        self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.cv_image = np.uint8(self.cv_image)                 ########################## 비디오 입력 방법 확인 해서 인자 'self.cv_image'   ex) cam = video 0 -> self.cv_image  한태민
        faceCascade = cv2.CascadeClassifier(path1[0])       ################################################    학습파일 경로   한태민
        faces = faceCascade.detectMultiScale(self.cv_image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))      ################################################학습파일 한태민
        





        #yolo src









        if faces == ():
            self.face_count = 0    
            self.catch_count = 0
            if self.miss_count == 0:
                self.get_target = 1
                self.miss_count = 1

        for (x,y,w,h) in faces:
            self.face_count += 1
            if self.face_count == 50 and not self.finder == 0:
                self.get_target = 0
                now = datetime.datetime.now().strftime("%m-%d-%H:%M:%S")
                getmsg = 'Catch_time\n' + now
                self.finder.append_text(getmsg)
                self.missing_count = 0

            if self.face_count > 50:
                self.catch_count += 1
                if self.catch_count == 50:
                    getmsg = 'Catching...'
                    self.finder.append_text(getmsg)
                    self.catch_count = 0
                    self.miss_count = 0
                    self.now1 = datetime.datetime.now()
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

        ################################################################ server 전송 부 ################################################################
        if self.get_target == 1:
            self.missing_count += 1
            now2 = datetime.datetime.now()
            if not self.people_select == 0:     
                if self.missing_count%50 == 0:
                        getmsg = 'Cam_num : ' + '%s' % self.camera
                        self.finder.append_text(getmsg)
                        getmsg = 'People_num : ' + '%d' % self.people_select
                        self.finder.append_text(getmsg)
                        getmsg = 'Missing_time\n' + str(now2 - self.now1)
                        self.finder.append_text(getmsg)

                        # self.data = (self.camera,self.people_select, str(now2 - self.now1))
                        # self.cursor.execute(self.query, self.data)
                        # self.db.commit()
            elif self.people_select == 0: 
                if self.missing_count%50 == 0:
                    getmsg = 'Cam_Num : ' + '%s' % self.camera
                    self.finder.append_text(getmsg)
                    getmsg = 'Missing...\n' + str(now2 - self.now1)
                    self.finder.append_text(getmsg)
        ################################################################ server 전송 부 ################################################################        

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

    def callback_manual(self, manual_msg):              # Cam 데이터 Qt 데이터로 변환 및 객체 추적 정보 Publish
                    self.servo_x = manual_msg.data[0]
                    self.servo_y = manual_msg.data[1]

    def moveEvent(self, event):                         # 화면 이동시 관련 창 동시 이동
        super(Tracking_Camera, self).moveEvent(event)
        self.cam_window = self.pos()
        global cam_window_x
        global cam_window_y
        cam_window_x = self.cam_window.x()
        cam_window_y = self.cam_window.y()
        if not self.control == 0: 
            geo = self.geometry()
            geo.moveTo(cam_window_x + 650, cam_window_y + 425)
            self.control.setGeometry(geo)
        
        if not self.finder == 0:
            geo1 = self.geometry()
            geo1.moveTo(cam_window_x + 650, cam_window_y + 200)
            self.finder.setGeometry(geo1)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cam_init = Cam_init(self.camera)
            self._sub.unregister()
            if self.manual == 0 and self.record == True and self.finder_status == 0:
                print('Recording Stop!')
                self.record = False
                self.tracking_on_off = 0
                self.control.close()
                self.finder.close()
                self.close()
            elif self.manual == 0 and self.record == True:
                print('Recording Stop!')
                self.record = False
                self.tracking_on_off = 0
                self.control.close()
                self.close()
            elif self.record == True and self.finder_status == 0:
                print('Recording Stop!')
                self.record = False
                self.finder.close()
                self.close()
            elif self.manual == 0 and self.finder_status == 0:
                self.tracking_on_off = 0
                self.control.close()
                self.finder.close()
                self.close()
            elif self.finder_status == 0:
                self.finder.close()
                self.close()
            elif self.record == True:
                print('Recording Stop!')
                self.record = False
                self.tracking_on_off = 0
                self.close()
            elif self.manual == 0:
                self.control.close()
                self.tracking_on_off = 0
                self.close()
            else:
                self.tracking_on_off = 0
                self.close()
    
    def __del__(self):
        print('Camera_sys_init...')

class Camera_Control(QtWidgets.QDialog, Background_Set):                # Cam 수동조작 & 방향키
    def __init__(self, camera):                         # Cam 수동조작 화면 셋팅
        super(Camera_Control, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.camera = camera
        print('Cam_Control_Num : %d' % self.camera)

        width = 130
        height = 85
        self.setFixedSize(width, height)
        self.setGeometry(cam_window_x + 650, cam_window_y + 480 - height, width, height)

        self.button_Up = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/up.png'),'', self)
        self.button_Up.resize(40, 40)
        self.button_Up.move(45, 0)
        self.button_Up.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Up.setFocusPolicy(Qt.NoFocus)
        self.button_Up.clicked.connect(lambda:self.Manual(1))

        self.button_Down = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/down.png'),'', self)
        self.button_Down.resize(40, 40)
        self.button_Down.move(45, 45)
        self.button_Down.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Down.setFocusPolicy(Qt.NoFocus)
        self.button_Down.clicked.connect(lambda:self.Manual(2))

        self.button_Right = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/right.png'),'', self)
        self.button_Right.resize(40, 40)
        self.button_Right.move(90, 45)
        self.button_Right.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Right.setFocusPolicy(Qt.NoFocus)
        self.button_Right.clicked.connect(lambda:self.Manual(3))

        self.button_Left = QtWidgets.QPushButton(QtGui.QIcon('/home/jin/mst/jin/The_latest_package/Data/Image/Controller/left.png'),'', self)
        self.button_Left.resize(40, 40)
        self.button_Left.move(0, 45)
        self.button_Left.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
        self.button_Left.setFocusPolicy(Qt.NoFocus)
        self.button_Left.clicked.connect(lambda:self.Manual(4))
        
        if normal_check == 1:
            self.servo_x = 320
            self.servo_y = 390
        else:
            pass
        self.show()

    def Manual(self, args):                             # Cam 수동조작 Publish
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