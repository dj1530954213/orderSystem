from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtCore

# https://www.cnblogs.com/ygzhaof/p/9732703.html具体表格的使用参考此博客
class ConfigHandle():
    def __init__(self, tableWidget: QTabWidget):

        self.tableWidget = tableWidget
        self.config_pares:{str: ConfigPare} = {}
        self.configList = []
        self.configobject = open("Config.csv", 'r', encoding="gbk")
        self.LoadConfig()
        self.configobject.close()
        # 设置第二列自适应
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        # 显示网格线
        self.tableWidget.setShowGrid(True)


    def LoadConfig(self):
        while True:
            # 接收读取的字符串并去除换行符
            line = self.configobject.readline().replace("\n", "")
            if not line:
                break
            # 将所有CSV数据读取至数据列表中
            items = line.split(',')
            self.configList.append(items)
            # 根据配置表生成定额参数对象，将在PointPare中作为模板使用
            if items[0] != "定额编号":  # 跳过标题行
                self.config_pares[f"{items[0]}"] = ConfigPare(items[0], items[1], items[2], float(items[3]), float(items[4]), float(items[5]))
        # 将记录填充入列表中
        self.tableWidget.setRowCount(len(self.configList)+1)
        self.tableWidget.setColumnCount(6)
        indexItemy = 0
        indexItemx = 0
        for itemy in self.configList:
            indexItemx = 0
            for itemx in itemy:
                # 添加记录
                self.tableWidget.setItem(indexItemy,indexItemx,QTableWidgetItem(str(self.configList[indexItemy][indexItemx])))
                indexItemx += 1
            indexItemy += 1
class ConfigPare():
    def __init__(self,quotaNumber,quotaDescribe,quotaUnit,quotaCount,quotaPrice,quotaTotalPrice):
        self.quotaNumber:str = quotaNumber
        self.quotaDescribe:str = quotaDescribe
        self.quotaUnit:str = quotaUnit
        self.quotaCount:float = quotaCount
        self.quotaPrice:float = quotaPrice
        self.quotaTotalPrice:float = quotaTotalPrice
    def __str__(self):
        return f"{self.quotaNumber}   {self.quotaDescribe}   {self.quotaUnit}   {self.quotaCount}   {self.quotaPrice}   {self.quotaTotalPrice}"