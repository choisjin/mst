## Ex 3-3. 창 닫기.
## https://codetorial.net/pyqt5/basics/closing.html

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('Quit', self) # 푸시버튼 생성. 이 버튼은 QPushButton 클래스의 인스턴스. 첫번째 파라미터는 버튼에 표시될 텍스트, 두번째 파라미터는 버튼이 위치할 부모 위젯
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('Quit Button')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())