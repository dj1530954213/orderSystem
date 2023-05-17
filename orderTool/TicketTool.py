import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow
from PyQt5 import uic
import toolUI

ticket_tool_application = QApplication(sys.argv)
ticket_tool = toolUI.ticket_toolui()
ticket_tool.ui.show()
ticket_tool_application.exec_()


