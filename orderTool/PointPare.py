from ConfigHandle import ConfigPare
class PointPare():
    def __init__(self, workName: str, diyWork: str, workTime: str, workResult: str, InformiationMod: {str: ConfigPare}):
        self.PworkName: str = workName
        self.PworkTime: str = workTime
        self.PworkResult: str = workResult
        self.PIsDIY: bool = not (diyWork == "")
        self.PdiyWork: str = diyWork
        self.PworkInformiation: {str: ConfigPare} = InformiationMod
        # 按照定额配置表来动态生成点位字典
        self.PworkContext: str = ""

    def CreatWorkContext(self):
        self.PworkContext: str = ""
        if self.PIsDIY:  # 是否为自定义工作量
            self.PworkContext += f"{self.PworkName}:"
            self.PworkContext += f"{self.PdiyWork}。"
            self.PworkContext += f"{self.PworkResult}。"
        else:
            self.PworkContext += f"{self.PworkName}:"
            for item in self.PworkInformiation.values():
                if item.quotaCount != 0:  # 定额条目中对应的点位是否为0
                    if item.quotaNumber == "SYAZ-5-317":  # 根据不同定额进行工作内容处理
                        self.PworkContext += f"{item.quotaDescribe}{round(item.quotaCount*5)}个、"
                    elif item.quotaNumber == "SYAZ-5-360":
                        self.PworkContext += f"可编程逻辑控制器PLC编程{round(item.quotaCount*24)}个点、SCADA系统数据库标签变量及报警变量测试共{round(item.quotaCount*24)}个、"
                    elif item.quotaNumber == "SYAZ-5-376":
                        self.PworkContext += f"{item.quotaDescribe}{round(item.quotaCount * 8)}个、"
                    else:
                        self.PworkContext += f"{item.quotaDescribe}{round(item.quotaCount)}个、"
            self.PworkContext += f"。{self.PworkResult}。"
            print(self.PworkContext)
    def CreatSqlStr(self):
        return f""
