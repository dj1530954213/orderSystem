import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow
from PyQt5 import uic


class main_windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("RecodeInput.ui")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = main_windows()
    mywindow.ui.show()
    app.exec_()
