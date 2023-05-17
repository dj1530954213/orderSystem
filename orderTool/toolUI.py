from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5 import uic
from ConfigHandle import ConfigHandle,ConfigPare
from PointPare import PointPare
from SqlHandle import sqlHabdle
import enum


class ticket_toolui(QMainWindow):
    def __init__(self):
        # 执行父类的构造函数
        super().__init__()
        # 加载实例化插入记录界面的类
        self.ui = uic.loadUi("RecodeInput.ui")
        self.inputpage = InputPage(self.ui)
        self.sql = sqlHabdle('orderDB.db')
        # 实例化点位对象PointPare
        self.currentPointPare = PointPare(workName=self.inputpage.tbx_WorkName.toPlainText(),
                                          workTime=self.inputpage.calendarWidget.selectedDate().toString('yyyy-MM-dd'),
                                          diyWork=self.inputpage.tbx_DIYWork.toPlainText(),
                                          workResult=self.inputpage.tbx_WorkResult.toPlainText(),
                                          InformiationMod=self.inputpage.configHandler.config_pares)
        # 按钮事件注册
        self.inputpage.btn_CreatWork.clicked.connect(self.btn_CreatWork_click)
        self.inputpage.btn_SaveWork.clicked.connect(self.btn_SaveWork_click)
        self.inputpage.btn_CountMoney.clicked.connect(self.btn_CountMoney_click)
        self.inputpage.btn_ChangeConfig.clicked.connect(self.btn_ChangeConfig_click)
        self.inputpage.btn_EnbaleModul.clicked.connect(self.btn_EnbaleModul_click)
        self.inputpage.btn_ResetTable.clicked.connect(self.btn_ResetTable_click)
    # 按钮信号处理
    def btn_CreatWork_click(self):
        self.currentPointPare.PworkName = self.inputpage.tbx_WorkName.toPlainText()
        self.currentPointPare.PworkTime = self.inputpage.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        self.currentPointPare.PworkResult = self.inputpage.tbx_WorkResult.toPlainText()
        self.currentPointPare.PdiyWork = self.inputpage.tbx_DIYWork.toPlainText()
        self.currentPointPare.PIsDIY = not(self.inputpage.tbx_DIYWork.toPlainText() == "")
        self.currentPointPare.CreatWorkContext()
        self.inputpage.ContextResult.setText(self.currentPointPare.PworkContext)

    def btn_ResetTable_click(self):
        for itemy in self.currentPointPare.PworkInformiation.values():
            singleConfigPare:ConfigPare = itemy
            singleConfigPare.quotaCount = 0
        self.RefreshTable()
    def btn_SaveWork_click(self):
        if self.inputpage.ContextResult.toPlainText() == "":
            QMessageBox.information(self, "提示", "请先生成工作量")
            return



    def btn_CountMoney_click(self):
        money = 0
        for itemy in self.currentPointPare.PworkInformiation.values():
            singleConfigPare: ConfigPare = itemy
            money += singleConfigPare.quotaTotalPrice
        QMessageBox.information(self,"提示",str(round(money,4)))

    def btn_ChangeConfig_click(self):
        table_wigth:QTableWidget = self.inputpage.configHandler.tableWidget
        table_wigth.setRowCount(table_wigth.rowCount()+1)
        try:
            csvFile = open("Config.csv", 'w', encoding="gbk")
            titlestr = "定额编号,定额描述,单位,数量,单价,合价\n"
            csvFile.write(titlestr)
            for index in range(1,table_wigth.rowCount()-1):
                writeLine = ""
                writeLine += f"{table_wigth.item(index,0).text()},"
                writeLine += f"{table_wigth.item(index, 1).text()},"
                writeLine += f"{table_wigth.item(index, 2).text()},"
                writeLine += f"{0},"
                writeLine += f"{table_wigth.item(index, 4).text()},"
                writeLine += f"{0}"
                writeLine += "\n"
                csvFile.write(writeLine)
            # 如果下面的任意一个单元格为空则跳入异常检查
            table_wigth.item(table_wigth.rowCount() - 2, 0).text()
            table_wigth.item(table_wigth.rowCount() - 2, 1).text()
            table_wigth.item(table_wigth.rowCount() - 2, 2).text()
            table_wigth.item(table_wigth.rowCount() - 2, 3).text()
            table_wigth.item(table_wigth.rowCount() - 2, 4).text()
            table_wigth.item(table_wigth.rowCount() - 2, 5).text()
            # 写入新增行
            csvFile.write(f"{table_wigth.item(table_wigth.rowCount(),0).text()},{table_wigth.item(table_wigth.rowCount(),1).text()},{table_wigth.item(table_wigth.rowCount(),2).text()},0,{table_wigth.item(table_wigth.rowCount(),4).text()},0")
            QMessageBox.information(self,"提示","新增及修改操作成功成功")
        except Exception as ex:
            csvFile.flush()
            csvFile.close()
            table_wigth.setRowCount(table_wigth.rowCount()-1)
            QMessageBox.information(self,"提示","未发现新增，已完成修改操作")
            return
    def btn_EnbaleModul_click(self):
        # 复选框状态
        analogChecked = bool(self.inputpage.APointCheck.checkState())
        otherChecked = bool(self.inputpage.OtherPointCheck.checkState())
        dPointChecked = bool(self.inputpage.DPointCheck.checkState())
        computerChecked = bool(self.inputpage.ComputerCheck.checkState())
        # 如果没有选择任何模板
        if analogChecked != True and otherChecked != True and dPointChecked != True and computerChecked != True:
            QMessageBox.information(self, "提示", "未选择任何模板")
            return
        # 如果选择了模拟量模板
        if analogChecked == True:  # SYAZ-5-360  SYAZ-5-202  SYAZ-5-375  SYAZ-5-213
            if self.inputpage.tbx_APointNumber.toPlainText() != "":
                apointNumber: float = float(self.inputpage.tbx_APointNumber.toPlainText())
                self.currentPointPare.PworkInformiation["SYAZ-5-360"].quotaCount += apointNumber/24*2
                self.currentPointPare.PworkInformiation["SYAZ-5-202"].quotaCount += apointNumber
                self.currentPointPare.PworkInformiation["SYAZ-5-375"].quotaCount += apointNumber
                self.currentPointPare.PworkInformiation["SYAZ-5-213"].quotaCount += apointNumber
            else:
                QMessageBox.information(self,"警告","未写入数量请重新出入")
        #  如果选择了状态量模板
        if dPointChecked == True:  # SYAZ-5-360   SYAZ-5-202   SYAZ-5-376   SYAZ-5-215
            if self.inputpage.tbx_DPointNumber.toPlainText()!= "":
                dPointNumber: float = float(self.inputpage.tbx_DPointNumber.toPlainText())
                self.currentPointPare.PworkInformiation["SYAZ-5-360"].quotaCount += dPointNumber/24*2
                self.currentPointPare.PworkInformiation["SYAZ-5-202"].quotaCount += dPointNumber
                self.currentPointPare.PworkInformiation["SYAZ-5-376"].quotaCount += dPointNumber/8
                self.currentPointPare.PworkInformiation["SYAZ-5-215"].quotaCount += dPointNumber
            else:
                QMessageBox.information(self,"警告","未写入数量请重新出入")
        #  如果选择了与第三方设备接口调试
        if otherChecked == True:  # SYAZ-5-378
            if self.inputpage.tbx_threeComNumber.toPlainText()!= "":
                threeComNumber: float = float(self.inputpage.tbx_threeComNumber.toPlainText())
                self.currentPointPare.PworkInformiation["SYAZ-5-378"].quotaCount += threeComNumber
            else:
                QMessageBox.information(self,"警告","未写入数量请重新出入")
        #  如果选择了生产管理计算机
        if computerChecked == True:  # SYAZ-5-317
            if self.inputpage.tbx_computerNumber.toPlainText()!= "":
                computerNumber: float = float(self.inputpage.tbx_computerNumber.toPlainText())/5
                self.currentPointPare.PworkInformiation["SYAZ-5-317"].quotaCount += computerNumber
            else:
                QMessageBox.information(self,"警告","未写入数量请重新输入")
        #  生成总价
        for item in self.currentPointPare.PworkInformiation.values():
            singleConfigPare: ConfigPare = item
            singleConfigPare.quotaTotalPrice = round(singleConfigPare.quotaCount*singleConfigPare.quotaPrice,4)
        #  刷新表格
        self.RefreshTable()
        #  复选框和文本框初始化
        self.inputpage.APointCheck.setCheckState(Qt.Unchecked)
        self.inputpage.OtherPointCheck.setCheckState(Qt.Unchecked)
        self.inputpage.DPointCheck.setCheckState(Qt.Unchecked)
        self.inputpage.ComputerCheck.setCheckState(Qt.Unchecked)
        self.inputpage.tbx_APointNumber.clear()
        self.inputpage.tbx_DPointNumber.clear()
        self.inputpage.tbx_threeComNumber.clear()
        self.inputpage.tbx_computerNumber.clear()

    def RefreshTable(self):
        indexItemy = 1
        for itemy in self.currentPointPare.PworkInformiation.values():
            singleConfigPare:ConfigPare = itemy
            self.inputpage.configHandler.tableWidget.setItem(indexItemy,0,QTableWidgetItem(str(singleConfigPare.quotaNumber)))
            self.inputpage.configHandler.tableWidget.setItem(indexItemy, 1, QTableWidgetItem(str(singleConfigPare.quotaDescribe)))
            self.inputpage.configHandler.tableWidget.setItem(indexItemy, 2, QTableWidgetItem(str(singleConfigPare.quotaUnit)))
            self.inputpage.configHandler.tableWidget.setItem(indexItemy, 3, QTableWidgetItem(str(round(singleConfigPare.quotaCount,3))))
            self.inputpage.configHandler.tableWidget.setItem(indexItemy, 4, QTableWidgetItem(str(round(singleConfigPare.quotaPrice,3))))
            self.inputpage.configHandler.tableWidget.setItem(indexItemy, 5, QTableWidgetItem(str(singleConfigPare.quotaTotalPrice)))
            indexItemy += 1


class InputPage():
    def __init__(self, ui):
        self.calendarWidget: QCalendarWidget = ui.calendarWidget
        self.tbx_WorkName: QTextEdit = ui.tbx_WorkName
        self.tbx_WorkResult: QTextEdit = ui.tbx_WorkResult
        self.tbx_DIYWork: QTextEdit = ui.tbx_DIYWork
        self.APointCheck: QCheckBox = ui.APointCheck
        self.OtherPointCheck: QCheckBox = ui.OtherPointCheck
        self.DPointCheck: QCheckBox = ui.DPointCheck
        self.ComputerCheck: QCheckBox = ui.ComputerCheck
        self.tbx_APointNumber: QTextEdit = ui.tbx_APointNumber
        self.tbx_computerNumber: QTextEdit = ui.tbx_computerNumber
        self.tbx_threeComNumber: QTextEdit = ui.tbx_threeComNumber
        self.tbx_DPointNumber: QTextEdit = ui.tbx_DPointNumber
        self.btn_CreatWork: QPushButton = ui.btn_CreatWork
        self.btn_SaveWork: QPushButton = ui.btn_SaveWork
        self.btn_CountMoney: QPushButton = ui.btn_CountMoney
        self.btn_ChangeConfig: QPushButton = ui.btn_ChangeConfig
        self.btn_EnbaleModul: QPushButton = ui.btn_EnbaleModul
        self.btn_ResetTable:QPushButton = ui.btn_ResetTable
        self.ContextResult: QTextEdit = ui.ContextResult
        # 表格控件类的实例化
        self.configHandler: ConfigHandle = ConfigHandle(ui.tableWidget)
