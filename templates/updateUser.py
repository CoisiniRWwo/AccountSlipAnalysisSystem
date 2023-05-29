from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox
from lib.connectMySQL import authentication,updateUserData,updateUserDataBypwd
from lib.encryption import sha256
from lib.share import SI

class updateUser:
    def __init__(self):
        self.ui = QUiLoader().load('../ui/updateUser.ui')

        # 查询账号信息
        self.identity = authentication()

        # 给用户名和账号设值
        self.ui.rusername.setText(self.identity[3])

        # 监听调用修改按钮控件
        self.ui.registertoButton_2.clicked.connect(self.updateUser)
        # self.ui.registertoButton_2.clicked.connect(print(123))
        # 监听调用取消按钮控件
        self.ui.registertoButton_3.clicked.connect(self.cancellation)

    def updateUser(self):
        username = str(self.ui.rusername.text().strip())
        password = str(self.ui.rpassword.text().strip())
        if password == '' :
            result = updateUserData(username)
            if result:
                QMessageBox.information(
                    self.ui,
                    '成功',
                    '成功修改账号信息'
                )
            self.ui.close()
            return
        else:
            sha256_pwd = sha256(password)
            if sha256_pwd != self.identity[2]:
                QMessageBox.critical(
                    self.ui,
                    '失败',
                    '旧密码错误！'
                )
                return
            else:
                newpassword = str(self.ui.rpassword_2.text().strip())
                sha256_newpwd = sha256(newpassword)
                result = updateUserDataBypwd(username,sha256_newpwd)
                if result:
                    QMessageBox.information(
                        self.ui,
                        '提示',
                        '成功修改用户信息'
                    )
                SI.updateWin.ui.close()
                SI.mainWin.ui.hide()
                SI.loginWin.ui.show()
                return



    def cancellation(self):
        self.ui.close()