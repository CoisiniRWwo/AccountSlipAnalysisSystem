from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from lib.share import SI
from lib.encryption import sha256

from lib.connectMySQL import rsegister


class rsegisterWin:
    def __init__(self):
        self.ui = QUiLoader().load('../ui/register.ui')
        # 监听返回按钮控件
        self.ui.retuenButton.clicked.connect(self.retuenButton)
        # 监听注册按钮控件
        self.ui.registertoButton.clicked.connect(self.onregister)

    def retuenButton(self):
        SI.rsegisterWin.ui.hide()
        SI.loginWin.ui.show()

    def onregister(self):
        # 获取account、username和password两个文本框
        r_account = str(self.ui.raccount.text().strip())
        r_username = str(self.ui.rusername.text().strip())
        r_password = str(self.ui.rpassword.text().strip())
        sha256_pwd = sha256(r_password)

        if r_account == '' and r_username == '' and r_password == '':
            QMessageBox.critical(
                self.ui,
                '错误',
                '信息有空，请重新输入'
            )
            return

        flag = rsegister(r_account, r_username, sha256_pwd)
        if flag:
            QMessageBox.information(
                self.ui,
                '提示',
                '注册成功,请去登录'
            )
            self.ui.hide()
            SI.loginWin.ui.show()
            return
