import sqlite3


class sqlHabdle():
    def __init__(self,path:str):
        self.path:str = path
        self.conn:sqlite3.Connection = None
        self.sqlCursor = None
    def closeConnect(self):
        try:
            self.conn.close()
        except Exception as ex:
            print(ex)
    def connect(self):
        try:
            self.conn:sqlite3.Connection = sqlite3.connect(self.path)
        except Exception as ex:
            print(ex)
    def sqlRead(self,sqlStr):
        sql_cursor = self.conn.cursor()
        result = sql_cursor.execute(sqlStr).fetchall()
        sql_cursor.close()
        return result
    def sqlExecute(self,sqlStr):
        sql_cursor = self.conn.cursor()
        sql_cursor.execute(sqlStr)
        self.conn.commit()
        sql_cursor.close()




if __name__ == '__main__':
    sqlHabdlea = sqlHabdle('orderDB.db')
    sqlHabdlea.connect()
    sqlStr = "insert into orderSystem " \
             "(workName,workTime,workResult,workDIY,workInformiation,workContext) " \
             "values(1,'2023-03-06',3,4,5,6)"
    sqlHabdlea.sqlExecute(sqlStr)
    print(sqlHabdlea.sqlRead('select * from orderSystem'))
    sqlHabdlea.closeConnect()