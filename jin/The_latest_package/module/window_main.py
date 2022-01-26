#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

import window_background_set
import window_login

class MainWindow(QtWidgets.QMainWindow):                # 기능선택 화면
    def __init__(self, position):                                 
        super(MainWindow, self).__init__()
        self.position = position
        self.initUI()
        
    def initUI(self):                                   # 기능선택 화면 셋팅
        global Main_width
        global Main_height
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        window_background_set.background_set(self)

        Main_width = 175
        Main_height = 175
        self.setFixedSize(Main_width, Main_height)
        self.setGeometry(self.position.x(), self.position.y(), Main_width, Main_height)
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
        path1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Weights File(*.weights)')
        #path1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'mp4 File(*.xml)') #################################### 파일 확장자 변경 한태민
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
            window_login()
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
            #Tracking_Camera(self.cam_num, self.people_select)
        elif self.cam_select == 1:
            print('Normal_Cam')
            #Normal_Camera(self.cam_num)
        else:
            if self.train == 1 and self.video == 1:
                print('Train & video')
                self.train = 0
                self.peple_select_cb.clear()
                self.People_ComboBoxInit()
                #Tracking_Video(self.cam_num, self.people_select)
            elif self.train == 0 and self.video == 1:
                print('video only')
                #Normal_Video(self.cam_num, self.people_select)
    
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
