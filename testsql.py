# import pymysql,datetime
from lib.connectMySQL import login, consumption, everyDayCountPrice
#
# DBHost = "localhost"
# DBUser = "root"
# DBPassword = "010111"
# DBName = "userinfo"
#
# # cur = connect().cursor()
# # sql = 'insert into userinfo values (%s,%s,%s,%s,%s)'
# # value = (None,'test','test','test',10.1)
# # cur.execute(sql,value)
# # db.commit()
# # print('数据插入成功')
# # sql = 'select * from userinfo'
# # cur.execute(sql)
# # result = cur.fetchall()
# # for row in result:
# #     id = row[0]
# #     username = row[1]
# #     pawssword = row[2]
# #     type = row[3]
# #     price = row[4]
# #     print('id:%s,username:%s,pawssword:%s,type:%s,price:%s'%(id,username,pawssword,type,price))
# # connect().close()
#
# # login("test","test1")
#
# # result = consumption("123")
# # for row,num in zip(result, range(0,len(result))):
# #     date = row[0]
# #     type = row[1]
# #     price = row[2]
# #     print(num)
# #     print('date=%s,type:%s,price:%s'%(date,type,price))
# # print(len(result))
#
# now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(now)


# list1 = list(range(1, 32))
# list2 = []
# for i in range(1,32):
#     list2.append(0)
# print(list1)
# print(list2)
# result = everyDayCountPrice()
# for row in result:
#     list2[row[0]] = row[1]
# print(list2)

# print(22//10+1)

# from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QPushButton
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('文件上传')
#         self.setGeometry(100, 100, 400, 300)
#
#         # 创建上传按钮
#         uploadBtn = QPushButton('上传文件', self)
#         uploadBtn.move(150, 100)
#         uploadBtn.clicked.connect(self.uploadFile)
#
#     def uploadFile(self):
#         # 打开文件对话框
#         fileName, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'All Files (*);;Text Files (*.txt)')
#
#         # 如果选择了文件，将文件名显示在标签中
#         if fileName:
#             self.label.setText(fileName)
#
# if __name__ == '__main__':
#     app = QApplication([])
#     mainWindow = MainWindow()
#     mainWindow.show()
#     app.exec()

from PIL import Image, ImageDraw, ImageFont
import random


def generate_captcha(length=4, size=(120, 40), font_size=25):
    # 生成随机字符
    chars = "0123456789abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha = ''.join(random.sample(chars, length))

    # 创建图片
    image = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 绘制字符
    font = ImageFont.truetype('arial.ttf', font_size)
    for i in range(length):
        draw.text((i * font_size + 10, 10), captcha[i], font=font, fill=get_random_color())

    # 绘制干扰点
    for i in range(200):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        draw.point((x, y), fill=get_random_color())

    return captcha, image


def get_random_color():
    return (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220))


# 生成验证码
captcha, image = generate_captcha()

# 输出验证码字符
print(captcha)

# 输出验证码图片
image.show()
