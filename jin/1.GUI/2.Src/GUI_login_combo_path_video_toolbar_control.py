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


class LoginForm(QtWidgets.QDialog):         # 로그인 화면
    def __init__(self):                     # 로그인 화면 셋팅
        super(LoginForm, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setWindowTitle('Login Window')
        
        width = 255
        height = 110
        
        self.setFixedSize(width, height)

        logo_label = QtWidgets.QLabel(self)
        logo_label.resize(100, 100)
        logo_label.move(155, 5)
        pixmap = QtGui.QPixmap('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/web.png')
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
        
        self.button_exit = QtWidgets.QPushButton('Exit', self)
        self.button_exit.clicked.connect(self.close)
        self.button_exit.resize(60, 30)
        self.button_exit.move(95, 75)

        self.center()
        global Position
        Position = self.qr.topLeft()

    def check_password(self):
        msg = QtWidgets.QMessageBox()

        if self.lineEdit_username.text() == 'choi3206' and self.lineEdit_password.text() == '0608':
            self.close()
            self.init = MainWindow()
        else :
            msg.setText('Check your ID, PW')
            msg.exec_()
            
    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())    

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
            QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/exit.png'),
             'Exit', self)                          # 툴바 아이콘 이미지 삽입
        exitAction.setShortcut('Ctrl+Q')            # 툴바 단축키 설정
        exitAction.setStatusTip('Exit')             # 상태창 메세지
        exitAction.setToolTip('Ctrl+Q')             # 툴팁 메세지
        exitAction.triggered.connect(self.close)    # 툴바 클릭시 발생 이벤트

        logoutAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/exit.png'), 'Logout', self)
        logoutAction.setShortcut('Ctrl+L')
        logoutAction.setStatusTip('Logout')
        logoutAction.setToolTip('Ctrl+L')
        logoutAction.triggered.connect(self.Logout)

        trainAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/open-file-button.png'), 'Train', self)
        trainAction.setShortcut('Ctrl+T')
        trainAction.setStatusTip('Train File Open')
        trainAction.setToolTip('Ctrl+T')
        trainAction.triggered.connect(self.Insert_Train)
        
        videoAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/open-file-button.png'), 'Video', self)
        videoAction.setShortcut('Ctrl+O')
        videoAction.setStatusTip('Video File Open')
        videoAction.setToolTip('Ctrl+O')
        videoAction.triggered.connect(self.Insert_Video)        
        
        stratAction = QtWidgets.QAction(QtGui.QIcon('/home/jin/mst/jin/1.GUI/2.Src/PyQt5_Tutorial/Data/exit.png'), 'Start', self)
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
        self.cam_num = 0                            # Camera 선택 초기화
        self.train = 0                              # Train 선택 초기화
        self.filePath.clear()                       # Train 파일 경로 초기화
        self.video = 0                              # Video 선택 초기화
        self.videoPath.clear()                      # Video 파일 경로 초기화

    def ComboBoxInit(self):                         # ComboBox 초기화
        self.cb.clear()                             # ComboBox 모두 지우기
        combo_num = 2                               # ComboBox 생성 갯수
        combo_init = 0                              
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
        if cam_num == 'Camera1':
            self.videoPath.clear()
            self.cam_num = 1
        elif cam_num == 'Camera2':
            self.videoPath.clear()
            self.cam_num = 2
        elif cam_num == 'Select Camera...':
            self.DataReset()

    def Start_btn(self):    
        if self.cam_num == 1 and self.train == 1:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Tracking_Camera(self.cam_num)
            self.DataReset()
            self.ComboBoxInit()
            print('cam1 & train')
        elif self.cam_num == 2 and self.train == 1:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Tracking_Camera(self.cam_num)
            self.DataReset()
            self.ComboBoxInit()
            print('cam2 & train')
        elif self.cam_num == 1:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Normal_Camera(self.cam_num)
            self.control = Camera_Control()
            self.DataReset()
            self.ComboBoxInit()
            print('cam1 & normal')
        elif self.cam_num == 2:
            rospy.init_node('Face_Tracking', anonymous=True)
            self.second = Normal_Camera(self.cam_num)
            self.DataReset()
            self.ComboBoxInit()
            print('cam2 & normal')   
        else:
            if self.train == 1 and self.video == 1:
                self.second = Tracking_Video()
                self.DataReset()
                self.ComboBoxInit()
                print('Train & video')
            elif self.train == 0 and self.video == 1:
                self.second = Normal_Video()
                self.DataReset()
                print('video only')                   

    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            self.logout_signal=1
            event.accept()
        else:
            self.logout_signal=2
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

class Normal_Video(QtWidgets.QDialog):
    def __init__(self):
        super(Normal_Video, self).__init__()
        self.setWindowTitle('Normal_Video')
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
    
    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:          
            event.accept()
        else:
            event.ignore()
            self.video = True
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cap.release()

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
    
    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:          
            event.accept()
        else:
            event.ignore()
            self.video = True
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cap.release()

class Camera_Control(QtWidgets.QDialog):
    def __init__(self):
        super(Camera_Control, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        height = 90
        self.setFixedSize(Main_width, height)
        self.setGeometry(Position.x(), Position.y()+Main_height+10, Main_width, height)

        self.button_REC = QtWidgets.QPushButton('REC', self)
        self.button_REC.resize(65,30)
        self.button_REC.move(5, 5)
        self.button_REC.clicked.connect(self.ChangeREC)
        
        self.button_Auto = QtWidgets.QPushButton('Auto', self)
        self.button_Auto.resize(65,30)
        self.button_Auto.move(10,50)
        self.button_Auto.clicked.connect(self.ChangeAuto)

        self.show()
    
    def ChangeREC(self):
        self.button_REC.setText("Stop")
        self.button_REC.clicked.connect(self.ReturnREC)

    def ReturnREC(self):
        self.button_REC.setText("REC")
        self.button_REC.clicked.connect(self.ChangeREC)

    def ChangeAuto(self):
        self.button_Auto.setText("Manual")
        self.button_Auto.clicked.connect(self.ReturnAuto)

    def ReturnAuto(self):
        self.button_Auto.setText("Auto")
        self.button_Auto.clicked.connect(self.ChangeAuto)


        # self.button_Manual = QtWidgets.QPushButton('Manual', self)
        # self.button_Manual.resize(65,30)
        # self.button_Manual.move(85,50)
        #self.button_Manual.clicked.connect()

        # self.button_UP = QtWidgets.QPushButton('UP')
        # self.button_UP.resize(65,30)
        # self.button_UP.move(10,130)
        #self.button_UP.clicked.connect()

        # self.button_Down = QtWidgets.QPushButton('Down')
        # self.button_Down.resize(65,30)
        # self.button_Down.move(10,130)
        #self.button_Down.clicked.connect()
 
        # self.button_Left = QtWidgets.QPushButton('Left')
        # self.button_Left.resize(65,30)
        # self.button_Left.move(10,130)
        #self.button_Left.clicked.connect()

        # self.button_Right = QtWidgets.QPushButton('Right')
        # self.button_Right.resize(65,30)
        # self.button_Right.move(10,130)
        #self.button_Right.clicked.connect()

        #self.center()

class Normal_Camera(QtWidgets.QDialog):
    def __init__(self, camera):
        super(Normal_Camera, self).__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self.camera=camera  
        
        if camera == 1 :
            self._sub = rospy.Subscriber('/camera1/usb_cam1/image_raw', Image, self.callback, queue_size=10)
        elif camera == 2 :
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=10)
        
        self.bridge = CvBridge()
                 
        Normal_cam_width = 640
        Normal_cam_height = 480
        self.setFixedSize(Normal_cam_width, Normal_cam_height)
        self.setGeometry(Position.x()+Main_width+10, Position.y(), Normal_cam_width, Normal_cam_height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.move(0,0)
         
        self.show()    

    def callback(self, data):  
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
           
        if self.camera == 1:
            self.width = 640
            self.height = 480
        elif self.camera == 2:
            self.width = 320
            self.height = 240
    
        self.label.resize(self.width, self.height)
        img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB) 
        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.cv_image = False
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cv_image = False
            self.close()

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
        faces = faceCascade.detectMultiScale(cv_image, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
        
        #얼굴인식 후 사각형 그리기
        for (x,y,w,h) in faces:
            cv2.rectangle(cv_image,(x,y),(x+w,y+h),(0,255,0),1)

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

    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QtWidgets.QMessageBox.question(self, 'Exit', quit_msg, QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.cv_image = False
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cv_image = False
            self.close()       

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    init = LoginForm()
    init.show()
    sys.exit(app.exec_())