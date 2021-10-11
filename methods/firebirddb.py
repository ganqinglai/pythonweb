import asyncio
import base64
import os
from io import StringIO
from config import PYFDB_POOL
from config import curpath


class FdbObj():
    def fdbOpen():
        POOL = PYFDB_POOL
        conn = POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    def fdbClose(conn, cursor):
        cursor.close()
        conn.close()

    @classmethod
    async def sp_ExecSql(cls, sql):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            cursor.execute(sql)
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_ExecSqlArrs(cls, sql, dataList):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            for data in dataList:
                execsql = ""
                execsql = sql.format(**data)
                cursor.execute(execsql)
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_GetTableBase(cls, sql):
        conn, cursor = cls.fdbOpen()
        try:
            cursor.execute(sql)
            await asyncio.sleep(1)
            rData = cursor.fetchall()
            rField = cursor.description
            rDataDict = [
                dict(zip([col[0] for col in rField], row)) for row in rData
            ]
            # rDataDict 返回json [{"field1":"value1","field2":"value2"},{"field1":"value3","field2":"value4"}]
        except Exception as e:
            e
        finally:
            cls.fdbClose(conn, cursor)

        return rDataDict

    @classmethod
    async def sp_ExecSql_JhInsert(cls, addList, jsonbody):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            dataDict_A = dict(jsonbody.get("master"))
            dataList_B = list(jsonbody.get("detail"))

            sqldictA = dict(list(addList)[0])
            sqldictB = dict(list(addList)[1])
            tableA = sqldictA.get("table")
            fieldA = sqldictA.get("field")
            valueA = sqldictA.get("value")
            sqlA = ""
            sqlA = "INSERT INTO {table}({field}) VALUES ({value})".format(
                table=tableA, field=fieldA, value=valueA)
            sqlA = sqlA.format(**dataDict_A)
            cursor.execute(sqlA)
            await asyncio.sleep(1)

            tableB = sqldictB.get("table")
            fieldB = sqldictB.get("field")
            valueB = sqldictB.get("value")
            sqlB = ""
            sqlB = "INSERT INTO {table}({field}) VALUES ({value})".format(
                table=tableB, field=fieldB, value=valueB)

            for data in dataList_B:
                execsql = ""
                execsql = sqlB.format(**data)
                cursor.execute(execsql)
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_ExecSql_JhModify(cls, modifyList, jsonbody):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            dataDict_A = dict(jsonbody.get("master"))
            dataList_B = list(jsonbody.get("detail"))

            sqldictA = dict(list(modifyList)[0])
            sqldictB = dict(list(modifyList)[1])
            tableA = sqldictA.get("table")
            fieldA = sqldictA.get("field")
            whereA = sqldictA.get("where")
            sqlA = ""
            sqlA = "UPDATE {table} SET {field} WHERE {where}".format(
                table=tableA, field=fieldA, where=whereA)
            sqlA = sqlA.format(**dataDict_A)
            cursor.execute(sqlA)
            await asyncio.sleep(1)

            tableB = sqldictB.get("table")
            fieldB = sqldictB.get("field")
            whereB = sqldictB.get("where")
            sqlB = ""
            sqlB = "UPDATE {table} SET {field} WHERE {where}".format(
                table=tableB, field=fieldB, where=whereB)

            for data in dataList_B:
                execsql = ""
                execsql = sqlB.format(**data)
                cursor.execute(execsql)
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_ExecSql_JhDelete(cls, deleteList, jsonbody):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            dataDict_A = dict(jsonbody.get("master"))
            dataList_B = list(jsonbody.get("detail"))

            sqldictA = dict(list(deleteList)[0])
            print()
            sqldictB = dict(list(deleteList)[1])
            tableA = sqldictA.get("table")
            whereA = sqldictA.get("where")
            sqlA = ""
            sqlA = "DELETE FROM  {table} WHERE {where}".format(table=tableA,
                                                               where=whereA)
            sqlA = sqlA.format(**dataDict_A)
            cursor.execute(sqlA)
            await asyncio.sleep(1)

            tableB = sqldictB.get("table")
            whereB = sqldictB.get("where")
            sqlB = ""
            sqlB = "DELETE FROM  {table} WHERE {where}".format(table=tableB,
                                                               where=whereB)

            for data in dataList_B:
                execsql = ""
                execsql = sqlB.format(**data)
                cursor.execute(execsql)
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_JhQuery(cls, queryList, jsonbody):
        conn, cursor = cls.fdbOpen()
        try:
            dataDict_A = dict(jsonbody.get("query"))

            sqldictA = dict(list(queryList)[0])
            sqldictB = dict(list(queryList)[1])

            tableA = sqldictA.get("table")
            fieldA = sqldictA.get("field")
            whereA = sqldictA.get("where")
            sqlA = ""
            sqlA = "SELECT {field} FROM {table} WHERE {where}".format(
                field=fieldA, table=tableA, where=whereA)
            sqlA = sqlA.format(**dataDict_A)
            cursor.execute(sqlA)
            await asyncio.sleep(1)
            rDataA = cursor.fetchall()
            rFieldA = cursor.description
            rDataDictA = [
                dict(zip([colA[0] for colA in rFieldA], rowA))
                for rowA in rDataA
            ]

            tableB = sqldictB.get("table")
            fieldB = sqldictB.get("field")
            whereB = sqldictB.get("where")
            sqlB = ""
            sqlB = "SELECT {field} FROM {table} WHERE {where}".format(
                field=fieldB, table=tableB, where=whereB)
            sqlB = sqlB.format(**dataDict_A)
            cursor.execute(sqlB)
            await asyncio.sleep(1)
            rDataB = cursor.fetchall()
            rFieldB = cursor.description
            rDataDictB = [
                dict(zip([colB[0] for colB in rFieldB], rowB))
                for rowB in rDataB
            ]
            rDataDict = dict()
            rDataDict = {tableA: rDataDictA, tableB: rDataDictB}
            # rDataDict 返回json [{"field1":"value1","field2":"value2"},{"field1":"value3","field2":"value4"}]
        except Exception as e:
            e
        finally:
            cls.fdbClose(conn, cursor)

        return rDataDict

    @classmethod
    async def sp_ExecSql_ImgInsert(cls, addList, jsonbody):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            '''
            sqldictA = dict(list(addList)[0])
            tableA = sqldictA.get("table")
            fieldA = sqldictA.get("field")
            valueA = sqldictA.get("value")

            dataDict = dict()
            dataDict["guid"] = jsonbody.get("guid")
            dataDict["imga"] = StringIO(jsonbody.get("imga"))
            dataDict["imgb"] = StringIO(jsonbody.get("imgb"))
            # https://www.cnblogs.com/wudeng/p/9559469.html
            sqlA = ""
            sqlA = "INSERT INTO {table}({field}) VALUES ({value})".format(
                table=tableA, field=fieldA, value=valueA)
            sqlA = sqlA.format(**dataDict)
            print(sqlA)

            cursor.execute(sqlA)
            '''
            '''
            def writeTofile(data, filename):
                # Convert binary data to proper format and write it on Hard Disk
                with open(filename, 'wb') as file:
                    file.write(data)
                print("Stored blob data into: ", filename, "\n")

            photo = StringIO(jsonbody.get("imga"))
            photoPath = "D:\\python\\python20201102\\statics\\uploads\\BBBB\\xxx.jpg"
            writeTofile(photo, photoPath)
            '''
            src = jsonbody.get("imga")
            data = src.split(',')[1]
            image_data = base64.b64decode(data)
            jsonpath = os.path.join(curpath,
                                    r"statics\\uploads\\BBBB\\zzz.jpg")
            with open(jsonpath, 'wb') as f:
                f.write(image_data)

            cursor.execute("insert into IMG values (?,?,?)", (
                jsonbody.get("guid"),
                StringIO(jsonbody.get("imga")),
                StringIO(jsonbody.get("imgb")),
            ))
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_ImgQuery(cls, queryList, jsonbody):
        conn, cursor = cls.fdbOpen()
        try:
            '''
            sqldictA = dict(list(queryList)[0])
            tableA = sqldictA.get("table")
            fieldA = sqldictA.get("field")
            whereA = sqldictA.get("where")
            dataDict = dict()
            dataDict["guid"] = jsonbody.get("guid")
            sqlA = ""
            sqlA = "SELECT {field} FROM {table} WHERE {where}".format(
                field=fieldA, table=tableA, where=whereA)
            sqlA = sqlA.format(**dataDict)
            print(sqlA)
            cursor.execute(sqlA)

            cursor.execute("select IMGA from IMG where guid='c09072c751fd412783c2caa7c5cbbf6d'")
            readerA = cursor.fetchone()[0]
            cursor.execute("select IMGB from IMG where guid='c09072c751fd412783c2caa7c5cbbf6d'")
            readerB = cursor.fetchone()[0]
            '''
            sql_fetch_blob_query = "SELECT IMGA, IMGB from IMG where guid = ?"
            cursor.execute(sql_fetch_blob_query, (jsonbody.get("guid"), ))
            record = cursor.fetchall()
            for row in record:
                readerA = row[0]
                readerB = row[1]

            await asyncio.sleep(1)
            rDataDict = dict()
            rDataDict = {
                "imgA": str(readerA)[2:-1],
                "imgB": str(readerB)[2:-1]
            }
            # rDataDict 返回json [{"field1":"value1","field2":"value2"},{"field1":"value3","field2":"value4"}]
        except Exception as e:
            print(e)
        finally:
            cls.fdbClose(conn, cursor)

        return rDataDict

    @classmethod
    async def sp_ExecSql_ImgModify(cls, modifyList, jsonbody):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            dataDict_A = dict(jsonbody.get("master"))
            dataList_B = list(jsonbody.get("detail"))

            sqldictA = dict(list(modifyList)[0])
            sqldictB = dict(list(modifyList)[1])
            tableA = sqldictA.get("table")
            fieldA = sqldictA.get("field")
            whereA = sqldictA.get("where")
            sqlA = ""
            sqlA = "UPDATE {table} SET {field} WHERE {where}".format(
                table=tableA, field=fieldA, where=whereA)
            sqlA = sqlA.format(**dataDict_A)
            cursor.execute(sqlA)
            await asyncio.sleep(1)

            tableB = sqldictB.get("table")
            fieldB = sqldictB.get("field")
            whereB = sqldictB.get("where")
            sqlB = ""
            sqlB = "UPDATE {table} SET {field} WHERE {where}".format(
                table=tableB, field=fieldB, where=whereB)

            for data in dataList_B:
                execsql = ""
                execsql = sqlB.format(**data)
                cursor.execute(execsql)
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    @classmethod
    async def sp_ExecSql_ImgDelete(cls, deleteList, jsonbody):
        flag = True
        conn, cursor = cls.fdbOpen()
        try:
            dataDict_A = dict(jsonbody.get("master"))
            dataList_B = list(jsonbody.get("detail"))

            sqldictA = dict(list(deleteList)[0])
            print()
            sqldictB = dict(list(deleteList)[1])
            tableA = sqldictA.get("table")
            whereA = sqldictA.get("where")
            sqlA = ""
            sqlA = "DELETE FROM  {table} WHERE {where}".format(table=tableA,
                                                               where=whereA)
            sqlA = sqlA.format(**dataDict_A)
            cursor.execute(sqlA)
            await asyncio.sleep(1)

            tableB = sqldictB.get("table")
            whereB = sqldictB.get("where")
            sqlB = ""
            sqlB = "DELETE FROM  {table} WHERE {where}".format(table=tableB,
                                                               where=whereB)

            for data in dataList_B:
                execsql = ""
                execsql = sqlB.format(**data)
                cursor.execute(execsql)
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            conn.rollback()
            flag = False
        else:
            conn.commit()

        cls.fdbClose(conn, cursor)
        return flag

    '''
    @classmethod
    def sf_FetchOneRecord(cls, sql):
        conn, cursor = cls.fdbOpen()
        cursor.execute(sql)
        dataArrs = cursor.fetchone()
        cls.fdbClose(conn, cursor)
        return dataArrs

    @classmethod
    def sf_FetchRowRecord(cls, sql):
        conn, cursor = cls.fdbOpen()
        cursor.execute(sql)
        dataArrs = cursor.fetchall()
        cls.fdbClose(conn, cursor)
        return dataArrs
    '''


'''
# cs.executemany('insert into '表名'(字段名) values(%s,%s,%s,%s)', usersvalues)
# 装饰器，计算插入50000条数据需要的时间
def timer(func):
    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)

    return decor

def add_test_users():

    usersvalues = []
    for num in range(1, 50000):

    conn = connect(host='主机名', port='端口号', user='用户名', password='密码', database='数据库名', charset='utf8')
    cs = conn.cursor()  # 获取光标
    # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
    cs.executemany('insert into '表名'(字段名) values(%s,%s,%s,%s)', usersvalues)

    conn.commit()
    cs.close()
    conn.close()
    print('OK')

调用存储过程
cursor = cnx.cursor()

try:
    args = (1,'op')
    cursor.callproc("get_product_info", args)
    #stored_results() 返回所有查询
    #result 获取一次查询
    for result in cursor.stored_results():
        #rs返回一次查询结果
        rs =result.fetchall()
except Exception as e:
    print(e)

# -*- coding: utf-8 -*-
"""
tornado websocket
author: cjh
"""
import json
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler


class WebsocketBase(WebSocketHandler):
    """继承WebSocketHandler基类，重写所需实例方法"""
    def on_message(self, message):
        """接收消息"""

    def data_received(self, chunk):
        """接收消息"""

    def open(self):
        """新的websocket连接后被调动"""
        print 'new_connect', self

    def on_close(self):
        """websocket连接关闭后被调用"""
        print 'lost_connect', self

    def check_origin(self, origin):
        """重写同源检查 解决跨域问题"""
        return True


class RealData(WebsocketBase):
    """实时数据"""
    def on_message(self, args):
        """args 是请求参数"""
        # TODO实际的业务操作,只需在此处写自己的业务逻辑即可。
        self.write_message('啦啦啦')		# 向客户端返回数据，如果是字典、列表这些数据类型，需要json.dumps()


class WebSocketApplication(Application):
    def __init__(self):
        handlers = [
            (r'/real_data', RealData),        # websocket路由
        ]
        Application.__init__(self, handlers)


def run():
    app = WebSocketApplication()
    app.listen(port=4053, address='0.0.0.0')
    IOLoop.current().start()


if __name__ == "__main__":
    run()


<html>
   <head>
      <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
      <script type="text/javascript">
         window.onload = function() {
            var ws = new WebSocket("ws://127.0.0.1:4053");
            ws.onopen = function() {
              console.log("client：打开连接");
              ws.send("{'unit_id':'38', 'db_code': 'sx'}");
            };
            ws.onmessage = function(e) {
              console.log("client：接收到服务端的消息 " + e.data);
              setTimeout(() => {
                /*ws.close(); */
              }, 5000);
            };
            ws.onclose = function(params) {
                console.log("client：关闭连接");
            };
         }
      </script>
   </head>
   <body>
      <h1>Ping output:</h1>
      <pre id="output">

      </pre>
   </body>
</html>



import sqlite3

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def readBlobData(empId):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            photo = row[2]
            resumeFile = row[3]

            print("Storing employee image and resume on disk \n")
            photoPath = "E:\\pynative\\Python\\photos\\db_data\\" + name + ".jpg"
            resumePath = "E:\\pynative\\Python\\photos\\db_data\\" + name + "_resume.txt"
            writeTofile(photo, photoPath)
            writeTofile(resumeFile, resumePath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

readBlobData(1)
readBlobData(2)



import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(empId, name, photo, resumeFile):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO new_employee
                                  (id, name, photo, resume) VALUES (?, ?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        resume = convertToBinaryData(resumeFile)
        # Convert data into tuple format
        data_tuple = (empId, name, empPhoto, resume)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

insertBLOB(1, "Smith", "E:\\pynative\\Python\\photos\\smith.jpg", "E:\\pynative\\Python\\photos\\smith_resume.txt")
insertBLOB(2, "David", "E:\\pynative\\Python\\photos\\david.jpg", "E:\\pynative\\Python\\photos\\david_resume.txt")

import fdb
import io

con = fdb.connect(dsn='localhost:testdatabase', user='sysdba', password='masterkey')

cur = con.cursor()
statement = "insert into blob_test2 (text_blob) values (?)"
cur.execute(statement, ("test blob as string",))
cur.execute(statement, (io.StringIO("test blob as StringIO"),))
streamwrites = io.StringIO()
streamwrites.write("streamed write1,")
streamwrites.write("streamed write2,")
streamwrites.seek(0)
cur.execute(statement, (streamwrites,))

con.commit()

con.close()


#-*-coding:utf-8-*- python 数据类型互相转换

#1、字典
dict = {'name': 'Zara', 'age': 7, 'class': 'First'}

#字典转为字符串，返回：<type 'str'> {'age': 7, 'name': 'Zara', 'class': 'First'}
print type(str(dict)), str(dict)

#字典可以转为元组，返回：('age', 'name', 'class')
print tuple(dict)
#字典可以转为元组，返回：(7, 'Zara', 'First')
print tuple(dict.values())

#字典转为列表，返回：['age', 'name', 'class']
print list(dict)
#字典转为列表
print dict.values

#2、元组
tup=(1, 2, 3, 4, 5)

#元组转为字符串，返回：(1, 2, 3, 4, 5)
print tup.__str__()

#元组转为列表，返回：[1, 2, 3, 4, 5]
print list(tup)

#元组不可以转为字典

#3、列表
nums=[1, 3, 5, 7, 8, 13, 20];

#列表转为字符串，返回：[1, 3, 5, 7, 8, 13, 20]
print str(nums)

#列表转为元组，返回：(1, 3, 5, 7, 8, 13, 20)
print tuple(nums)

#列表不可以转为字典

#4、字符串

#字符串转为元组，返回：(1, 2, 3)
print tuple(eval("(1,2,3)"))
#字符串转为列表，返回：[1, 2, 3]
print list(eval("(1,2,3)"))
#字符串转为字典，返回：<type 'dict'>
print type(eval("{'name':'ljq', 'age':24}"))

'''
