
import traceback
import shutil
from multiprocessing import cpu_count
import os
import time
import sqlite3
import requests
import json
import random

def get_now():
    return time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))

'''

参数有：
src_pdf_path 原PDF文件位置
save_pic_path 生成隔页保存位置
processors 要使用的进程数
COLOR_THRESHHOLD 为亮度阈值
LoginToken 为上传服务器记录的Token
urldb 为保存连接信息的数据库
PdfExePath 为切分PDF文件的exe路径
'''
class cutPdfClass:

    def __init__(self, src_pdf_path, save_pic_path, processors, COLOR_THRESHHOLD, LoginToken, urldb, PdfExePath, communication = None):
        self.user = ""
        self.src_pdf_path = src_pdf_path
        self.save_pic_path = save_pic_path
        self.processors = processors
        self.COLOR_THRESHHOLD = COLOR_THRESHHOLD
        self.token = LoginToken
        self.run_code = 1
        self.urldb = urldb
        self.PdfExePath = PdfExePath
        self.communication = communication

    def run(self):
        if not os.path.isdir(self.src_pdf_path):
            if self.communication:
                self.communication.mainPrint("原PDF文件路径不存在")
            else:
                print("原PDF文件路径不存在")
            return
        if not os.path.isdir(self.save_pic_path):
            if self.communication:
                self.communication.mainPrint("保存文件隔页位置不存在")
            else:
                print("保存文件隔页位置不存在")
            return
        if '"' in self.src_pdf_path:
            if self.communication:
                self.communication.mainPrint("源文件路径包含英文的双引号")
            else:
                print("源文件路径包含英文的双引号")
            return
        else:
            if '"' in self.save_pic_path:
                if self.communication:
                    self.communication.mainPrint("保存文件路径包含英文的双引号")
                else:
                    print("保存文件路径包含英文的双引号")
                return

        if not self.checkSpace():
            return

        self.oldDir = set()
        # 获取所有保存PDF文件位置中的所有文件夹列表。
        ALlFileList = os.listdir(self.save_pic_path)
        for i in ALlFileList:
            dir = os.path.join(self.save_pic_path, i)
            if os.path.isdir(dir):
                self.oldDir.add(dir)

        #检查token
        self.checkToken(3, "获取隔页")
        if self.run_code:
            self.true_run()
        else:
            if self.communication:
                self.communication.mainPrint("程序执行报错")
            else:
                print("程序执行报错")
            # self.communication.reload_signal.emit()

    #获取URL文件位置
    def get_url(self,urlName):
        conn = sqlite3.connect(self.urldb)
        cursor = conn.cursor()
        sql = "select * from urldb where url_name = '{}'".format(urlName)
        cursor.execute(sql)
        g = cursor.fetchall()
        return g

    #开始执行时传递的id，和所需要记录的文本
    def checkToken(self,id,comments):
        try:
            if not os.path.exists(self.urldb):
                if self.communication:
                    self.communication.mainPrint("保存URl表不存在")
                else:
                    print("保存URl表不存在")
                self.run_code = 0
                return False
            if self.communication:
                self.communication.mainPrint(self.token)
            else:
                print(self.token)
            headers = {
                "token": self.token
            }
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": id,
                    "comments": "【开始执行：】  {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                if self.communication:
                    self.communication.mainPrint(response.text)
                else:
                    print(response.text)
                if response.status_code != 200:

                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break

                        if num == 2:
                            # self.communication.child_token_signal.emit()
                            if self.communication:
                                self.communication.mainPrint("登录信息的Token过期")
                            else:
                                print("登录信息的Token过期")
                            self.run_code = 0
                        num += 1
                else:
                    if self.communication:
                        self.communication.mainPrint("更新成功")
                    else:
                        print("更新成功")
        except Exception as e:
            if self.communication:
                self.communication.mainPrint("请求网页失败")
                self.communication.mainPrint(e)
            else:
                print("请求网页失败")
                print(e)
            self.run_code = 0

    # 完成执行时传递的id，和所需要记录的文本
    def checkToken1(self,id,comments):
        try:
            if not os.path.exists(self.urldb):
                if self.communication:
                    self.communication.mainPrint( "保存URl表不存在")
                else:
                    print("保存URl表不存在")
                self.run_code = 0
                return False
            headers = {
                "token": self.token
            }
            if self.communication:
                self.communication.mainPrint(self.token)
            else:
                print(self.token)
            dbText = self.get_url("commit")
            if dbText:
                url = dbText[0][1]
                body = {
                    "id": id,
                    "comments": "【执行完成：】 {}".format(comments),
                    "pid": 0
                }
                response = requests.post(url=url, data=json.dumps(body), headers=headers)
                #判断响应的状态码是否为200， 不为200会进行三次尝试
                if response.status_code != 200:
                    num = 0
                    while num < 3:
                        time.sleep(random.uniform(0.5, 1))
                        response = requests.post(url=url, data=json.dumps(body), headers=headers)
                        if response.status_code == 200:
                            break
                        if num == 2:
                            if self.communication:
                                self.communication.mainPrint("登录信息的Token过期")
                            else:
                                print("登录信息的Token过期")
                            self.run_code = 0
                        num+=1
                else:
                    if self.communication:
                        self.communication.mainPrint("更新成功")
                    else:
                        print("更新成功")

        except Exception as e:
            if self.communication:
                self.communication.mainPrint("请求网页失败")
                self.communication.mainPrint(str(e))
            else:
                print("请求网页失败")
                print(str(e))
            self.run_code = 0

    #检查空格
    def checkSpace(self):

        file_path = self.src_pdf_path
        filename = ""
        for parent, dir, files in os.walk(file_path):
            for i in files:
                if " .pdf" in i:
                    filename += i + "   "
                    if self.communication:
                        self.communication.mainPrint("pdf文件："+ i + "。包含空格\n")
                    else:
                        print("pdf文件："+ i + "。包含空格\n")
                    self.run_code = 0
        if filename:
            if self.communication:
                self.communication.mainPrint("存在PDF文件包含空格，请修改后再次输入")
            else:
                print("存在PDF文件包含空格，请修改后再次输入")
            return False
        else:
            return True

    def true_run(self):
        if self.communication:
            self.communication.mainPrint(self.src_pdf_path)
            self.communication.mainPrint(self.save_pic_path)
        else:
            print(self.src_pdf_path)
            print(self.save_pic_path)
        # 判断路径是否过长
        len_number = 0
        # 判断路劲是否存在
        if os.path.exists(self.src_pdf_path):
            if os.path.exists(self.save_pic_path):
                for parent, dirnames, filenames in os.walk(self.src_pdf_path):
                    for filename in filenames:
                        file_path = os.path.join(parent, filename)
                        pathLen = len(file_path) + len(self.save_pic_path) - len(self.src_pdf_path)
                        if pathLen >= 259:
                            len_number = 1
                            if self.communication:
                                self.communication.mainPrint(file_path + " \n路径过长")
                            else:
                                print(file_path + " \n路径过长")
            else:
                self.run_code = 0
                if self.communication:
                    self.communication.mainPrint("保存文件不存在，请重新输入\n")
                else:
                    print("保存文件不存在，请重新输入\n")
        else:
            self.run_code = 0
            if self.communication:
                self.communication.mainPrint("原路径不存在，请重新输入\n")
            else:
                print("原路径不存在，请重新输入\n")

        # 判断路径长度是否大于259
        if len_number and self.run_code:
            # 线程结束
            if self.communication:
                self.communication.mainPrint("这里是要结束的进程， 这里是待写入的文件路径")
            else:
                print("这里是要结束的进程， 这里是待写入的文件路径")

        if not self.COLOR_THRESHHOLD and self.run_code:
            self.COLOR_THRESHHOLD = 19

        # 设置默认的进程数为cpu的核数-1
        if not self.processors :
            self.processors = int(cpu_count() - 1)

        else:
            #判断输入的线程内容为整数，还是分数
            try:

                if int(self.processors) > int(cpu_count()) or int(self.processors) < 1:
                    if self.communication:
                        self.communication.mainPrint("请输入1-{}的整数".format(cpu_count() ))
                    else:
                        print("请输入1-{}的整数".format(cpu_count() ))
                    return "请输入1-{}的整数".format(cpu_count() )

                self.processors = int(self.processors)

            except:
                try:
                    self.run_code = 0
                    self.processors = ""
                    if self.communication:
                        self.communication.mainPrint("请输入1-{}的整数".format(cpu_count() ))
                    else:
                        print("请输入1-{}的整数".format(cpu_count() ))
                    return "请输入1-{}的整数".format(cpu_count() )

                except:
                    traceback.print_exc()

        # 检测用于保存表的路径是否存在
        Db_path = r'database'
        if not os.path.exists(Db_path):
            os.makedirs(Db_path)

        #通过执行exe来运行
        if self.run_code:
            main = self.PdfExePath
            if not os.path.isfile(main):
                if self.communication:
                    self.communication.mainPrint("warning", "切分隔页的exe不存在")
                else:
                    print("warning", "切分隔页的exe不存在")
                return
            else:
                if self.communication:
                    self.communication.mainPrint("执行隔页exe\n")
                else:
                    print("执行隔页exe\n")
                try:
                    if self.communication:
                        self.communication.mainPrint('执行exe信息')
                        self.communication.mainPrint((self.src_pdf_path, self.save_pic_path, self.processors, int(self.COLOR_THRESHHOLD)))
                    else:
                        print('执行exe信息')
                        print((self.src_pdf_path, self.save_pic_path, self.processors, int(self.COLOR_THRESHHOLD)))
                    f = os.popen('"{main}" "{oldPath}" "{savePath}" "{process}" "{num}"'.format(main = main,oldPath = self.src_pdf_path, savePath =self.save_pic_path, process= self.processors, num= int(self.COLOR_THRESHHOLD)))
                    data = f.readlines()
                    f.close()
                    for i in data:
                        if self.communication:
                            self.communication.mainPrint(i)
                        else:
                            print(i)
                except Exception as e:
                    if self.communication:
                        self.communication.mainPrint("执行exe文件报错")
                    else:
                        print("执行exe文件报错")
                    start_time = get_now()
                    index_check_log_name = './logging/底稿切分隔页UI报错日志_' + str(start_time)
                    log_path = os.path.join(os.getcwd(),index_check_log_name.replace("./", "") + ".txt").replace("\\","/")
                    if self.communication:
                        self.communication.mainPrint("保存运行日志的文件夹为：" + log_path.split('logging/')[0] + "logging。运行日志文件名为：" +log_path.split('logging/')[1] + "\n")
                    else:
                        print("保存运行日志的文件夹为：" + log_path.split('logging/')[0] + "logging。运行日志文件名为：" +log_path.split('logging/')[1] + "\n")
                    with open(index_check_log_name + '.txt', "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                        file.write('[Error]' + str(get_now()) + "\n")
                        file.write('[报错内容]' + str(e) + "\n")
                        file.write('[报错源文件位置]' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + "\n")
                        file.write('[报错源码行数]' + str(e.__traceback__.tb_lineno) + "\n")
                if self.communication:
                    self.communication.mainPrint("执行完成")
                else:
                    print("执行完成")
        self.checkToken1(3, "获取隔页")


    #停止切分
    def stopCut(self):
        try:
            #停止所有正在切分的Exe
            os.system("taskkill -f -im cutPdfFun.exe")
            self.newDir = set()
            f = os.listdir(("源文件路径包含英文的双引号"))
            for i in f:
                dir = os.path.join(("源文件路径包含英文的双引号"), i)
                if os.path.isdir(dir):
                    self.newDir.add(dir)
            dir_names = self.newDir - self.oldDir
            if self.communication:
                self.communication.mainPrint("new"+ str(self.newDir))
                self.communication.mainPrint("old"+ str(self.oldDir))
                self.communication.mainPrint(dir_names)
            else:
                print("new"+ str(self.newDir))
                print("old"+ str(self.oldDir))
                print(dir_names)
            for i in dir_names:
                shutil.rmtree(i)
        except:
            traceback.print_exc()



if __name__ == "__main__":
    src_pdf_path = r'D:\0000代切分PDf'
    save_pic_path = r'D:\0000切分后保存位置'
    processors = 4
    COLOR_THRESHHOLD = 19
    LoginToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwibWFjIjoiMDAyYjY3ZTIyZDU4IiwiaXAiOiIxMjQuMjAyLjIxMi4xOCJ9.7msweo_W_V7cTM70kZv8bM0SJYBQ_pvBTlX9-HPcMkE"
    urldb = './url.db'
    # PdfExePath = "./cutPdfFun.exe"
    PdfExePath = r"D:\000PDF撕裂者\NewCutPdfFun\CutPdfFun\cutPdfFun.exe"
    cutfun = cutPdfClass(src_pdf_path, save_pic_path, processors, COLOR_THRESHHOLD, LoginToken, urldb, PdfExePath)
    cutfun.run()