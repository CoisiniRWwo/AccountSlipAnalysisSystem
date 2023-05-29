from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import ImageQt
from lib.share import SI
from lib.encryption import sha256
from templates.register import rsegisterWin
from templates.main import win_Main
from lib.connectMySQL import login
from lib.glob import _init, setAccountValue, code_init, setCodeValue, getCodeValue
from lib.verificationCode import generate_captcha


class win_Login:

    def __init__(self):
        self.ui = QUiLoader().load('../ui/login.ui')
        # 当登录按钮被点击调用onSignIn方法
        self.ui.login_button.clicked.connect(self.onSignIn)
        # 监听在password文本框回车时直接调用onSignIn方法
        self.ui.edt_password.returnPressed.connect(self.onSignIn)
        # 监听注册按钮控件
        self.ui.registerbutton.clicked.connect(self.onSegister)
        # 监听验证码按钮
        self.ui.vCodebutton.clicked.connect(self.verCode)

        code_init()
        # 启动界面默认调用验证码方法
        self.verCode()

    # 调用注册界面
    def onSegister(self):
        SI.rsegisterWin = rsegisterWin()
        SI.rsegisterWin.ui.show()
        self.ui.hide()

    # 登录判断
    def onSignIn(self):
        # 对全局变量初始化
        _init()
        # 获取username和password两个文本框
        account = str(self.ui.edt_username.text().strip())
        password = str(self.ui.edt_password.text().strip())
        code = str(self.ui.edt_password_2.text().strip())
        sha256_pwd = sha256(password)

        if str(code).lower() != str(getCodeValue()).lower():
            QMessageBox.critical(
                self.ui,
                '失败',
                '验证码错误'
            )
            return

        result = login(account, sha256_pwd)
        if result == False:
            QMessageBox.critical(
                self.ui,
                '失败',
                '账号密码错误'
            )
            return

        # 对全局变量赋值
        setAccountValue(account)

        # 调用主界面
        SI.mainWin = win_Main()
        SI.mainWin.ui.show()
        # 清空密码
        self.ui.edt_password.setText('')
        self.ui.edt_password_2.setText('')
        self.verCode()
        # 隐藏此界面
        self.ui.hide()

    def verCode(self):
        # 生成验证码
        captcha, image = generate_captcha()
        # 将Image对象转换为QPixmap对象
        pixmap = QPixmap.fromImage(ImageQt.ImageQt(image)).scaled(100, 100, Qt.KeepAspectRatio)
        # 设置按钮图标
        # self.ui.vCodebutton.setIcon(pixmap)
        self.ui.label_5.setPixmap(pixmap)
        setCodeValue(captcha)


app = QApplication([])
SI.loginWin = win_Login()
SI.loginWin.ui.show()
app.exec()
