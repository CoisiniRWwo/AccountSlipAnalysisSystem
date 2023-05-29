from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QInputDialog, QLineEdit
from PySide6.QtUiTools import QUiLoader
from lib.connectMySQL import insertByaccount
from lib.glob import getAccountValue


class win_InsertAccount:
    def __init__(self, main):
        self.main = main
        self.ui = QUiLoader().load('../ui/insertAccount.ui')
        # 监听提交按钮
        self.ui.commitInsert.clicked.connect(self.insertData)
        # 监听取消按钮
        self.ui.pushButton_2.clicked.connect(self.closWin)

    def insertData(self):
        # 获取下拉框值
        method = str(self.ui.typeBox.currentText())
        # 获取金额文本框
        price = str(self.ui.priceLine.text().strip())
        # print(method)
        # print(price)
        if method == '' or price == '':
            QMessageBox.critical(
                self.ui,
                '错误',
                '输入的值有空，请重新输入'
            )
            return

        result = insertByaccount(getAccountValue(), method, price)

        if result:
            QMessageBox.information(
                self.ui,
                '添加成功',
                '跳转回主界面'
            )
            self.closWin()
            self.main.resettingTable()
        else:
            QMessageBox.critical(
                self.ui,
                '失败',
                '遇到问题，添加失败'
            )

    def closWin(self):
        self.ui.close()
