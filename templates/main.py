from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QInputDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor
import pandas as pd
import time
import updateUser
from lib.share import SI
from lib.glob import getAccountValue, page_init, addPageValue, subPageValue, getPageValue, setPageValue
from templates.ConsumptionPrice import barType
from templates.ConsumptionType import showPieChart
from lib.connectMySQL import consumption, selectfileDownLoad, deleteByAccount, \
    searchDataSQL, selectNameByAccount, updateDataByuuid, countData, insertExecl, insertBudget, selectMonthBudget \
    , selectBudget, selectBudgetData


class win_Main:
    def __init__(self):
        self.ui = QUiLoader().load('../ui/main.ui')

        # 实例化TableOperations类
        # table_ops = TableOperations(self.ui)

        # 监听调用搜索按钮控件
        self.ui.searchbutton.clicked.connect(self.searchData)
        # 监听调用重置按钮控件
        self.ui.resetting.clicked.connect(self.resettingTable)
        # 监听调用添加账单按钮控件
        self.ui.insertAccount.clicked.connect(self.insertAccount)
        # 监听调用上一页按钮控件
        self.ui.previousPage.clicked.connect(self.lastPage)
        # 监听调用下一页按钮控件
        self.ui.nextPage.clicked.connect(self.nextToPage)
        # 监听调用删除按钮控件
        self.ui.deleteButton.clicked.connect(self.deleteData)

        # 获取点击退出动作
        self.ui.actionExit.triggered.connect(self.onSignOut)
        # 获取主页明细动作
        self.ui.actionsaccount.triggered.connect(self.account)
        # 获取消费类型分析动作
        self.ui.accounttype.triggered.connect(self.accounttype)
        # 获取消费金额分析动作
        self.ui.accountprice.triggered.connect(self.accountprice)
        # 获取上传动作
        self.ui.actionshangchuan.triggered.connect(self.fileshangchuan)
        # 获取下载动作
        self.ui.actionxiazai.triggered.connect(self.fileDownLoad)
        # 获取添加预算动作
        self.ui.actionbudget.triggered.connect(self.insertbudget)
        # 获取修改预算动作
        self.ui.actionxiugaibudget.triggered.connect(self.updateBudget)
        # 获取修改个人信息动作
        self.ui.actionupdateUser.triggered.connect(self.updateUser)

        # 设置主界面时间控件默认时间
        self.ui.startdate.setDateTime(QDateTime.currentDateTime())
        self.ui.enddate.setDateTime(QDateTime.currentDateTime())

        # 设置页码
        countPageRow = countData()
        if countPageRow[0] % 10 != 0:
            countPageRowResult = countPageRow[0] // 10 + 1
        else:
            countPageRowResult = countPageRow[0] // 10

        pagelabelResult = '/共' + str(countPageRowResult) + '页'
        self.ui.pagelabel.setText(pagelabelResult)
        # 监听调用跳转按钮控件
        self.ui.pagepushButton.clicked.connect(lambda: self.jumpPage(countPageRowResult))

        # 初始化分页参数全局变量
        page_init()

        # 调用全局变量获取account
        account = getAccountValue()

        # 显示用户名
        username = selectNameByAccount(account)
        username = '用户名：' + username[0]
        self.ui.usernameLabe.setText(username)

        # 本月预算查询
        self.selectBudget()

        # 数据明细查询显示
        result = consumption(account)
        # 取消表格自带序列
        self.ui.accounttableWidget.verticalHeader().setHidden(True)
        # 表格列宽分配
        self.ui.accounttableWidget.setColumnWidth(0, 50)
        self.ui.accounttableWidget.setColumnWidth(1, 250)
        self.ui.accounttableWidget.setColumnWidth(2, 150)
        self.ui.accounttableWidget.setColumnWidth(4, 108)

        for row, num in zip(result, range(0, len(result))):
            # 对要插入的行定义
            self.ui.accounttableWidget.insertRow(num)

            # 修改值类型为QTableWidgetItem
            uuidnum = QTableWidgetItem(str(row[0]))
            # 数据居中
            uuidnum.setTextAlignment(Qt.AlignCenter)
            uuidnum.setFlags(uuidnum.flags() ^ Qt.ItemIsEditable)
            uuidnum.setBackground(QColor(Qt.lightGray).lighter(125))
            datetime = QTableWidgetItem(str(row[1]))
            datetime.setTextAlignment(Qt.AlignCenter)
            datetime.setFlags(datetime.flags() ^ Qt.ItemIsEditable)
            datetime.setBackground(QColor(Qt.lightGray).lighter(125))
            type = QTableWidgetItem(row[2])
            type.setTextAlignment(Qt.AlignCenter)
            price = QTableWidgetItem(str(row[3]))
            price.setTextAlignment(Qt.AlignCenter)

            # 设置某列无法更改
            number = QTableWidgetItem(str(num + 1))
            number.setTextAlignment(Qt.AlignCenter)
            number.setBackground(QColor(Qt.lightGray).lighter(125))
            number.setFlags(number.flags() ^ Qt.ItemIsEditable)

            # 插入数据
            self.ui.accounttableWidget.setItem(num, 0, number)
            self.ui.accounttableWidget.setItem(num, 1, uuidnum)
            self.ui.accounttableWidget.setItem(num, 2, datetime)
            self.ui.accounttableWidget.setItem(num, 3, type)
            self.ui.accounttableWidget.setItem(num, 4, price)

        # 监听表格发生变化
        self.ui.accounttableWidget.itemChanged.connect(self.on_item_changed)

        # 将消费金额分析动作与搜索按钮绑定
        self.ui.yearmonthButton.clicked.connect(self.ui.accountprice.triggered)

        # 将消费类型分析动作与搜索按钮绑定
        self.ui.yearmonthButton_2.clicked.connect(self.ui.accounttype.triggered)

    def account(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def accounttype(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        showPieChart(self)
        # scrollAreaType

    def accountprice(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        barType(self)

    # 按条件查询数据
    def searchData(self):
        self.ui.accounttableWidget.itemChanged.disconnect(self.on_item_changed)
        # 清空表格
        self.ui.accounttableWidget.setRowCount(0)
        # 获取两个时间
        startdate = self.ui.startdate.date()
        startyear = startdate.year()
        startmonth = startdate.month()
        startday = startdate.day()
        starttime = self.ui.startdate.time()
        starthour = starttime.hour()
        startminute = starttime.minute()
        startsecond = starttime.second()
        startDateTime = str(startyear) + '-' + str(startmonth) + '-' + str(startday) + ' ' + str(starthour) + ':' + str(
            startminute) + ':' + str(startsecond)
        enddate = self.ui.enddate.date()
        endyear = enddate.year()
        endmonth = enddate.month()
        endday = enddate.day()
        endtime = self.ui.enddate.time()
        endhour = endtime.hour()
        endminute = endtime.minute()
        endsecond = endtime.second()
        endDateTime = str(endyear) + '-' + str(endmonth) + '-' + str(endday) + ' ' + str(endhour) + ':' + str(
            endminute) + ':' + str(endsecond)
        # print(startDateTime, ',', endDateTime)
        # 获取下拉框值
        method = self.ui.comboBox.currentText()
        # print('method:', method)
        result = searchDataSQL(startDateTime, endDateTime, method)
        for row, num in zip(result, range(0, len(result))):
            # 对要插入的行定义
            self.ui.accounttableWidget.insertRow(num)

            # 修改值类型为QTableWidgetItem
            uuidnum = QTableWidgetItem(str(row[0]))
            # 数据居中
            uuidnum.setTextAlignment(Qt.AlignCenter)
            uuidnum.setFlags(uuidnum.flags() ^ Qt.ItemIsEditable)
            uuidnum.setBackground(QColor(Qt.lightGray).lighter(125))
            datetime = QTableWidgetItem(str(row[1]))
            datetime.setTextAlignment(Qt.AlignCenter)
            datetime.setFlags(datetime.flags() ^ Qt.ItemIsEditable)
            datetime.setBackground(QColor(Qt.lightGray).lighter(125))
            type = QTableWidgetItem(row[2])
            type.setTextAlignment(Qt.AlignCenter)
            price = QTableWidgetItem(str(row[3]))
            price.setTextAlignment(Qt.AlignCenter)

            # 设置某列无法更改
            number = QTableWidgetItem(str(num + 1))
            number.setTextAlignment(Qt.AlignCenter)
            number.setBackground(QColor(Qt.lightGray).lighter(125))
            number.setFlags(number.flags() ^ Qt.ItemIsEditable)

            # 插入数据
            self.ui.accounttableWidget.setItem(num, 0, number)
            self.ui.accounttableWidget.setItem(num, 1, uuidnum)
            self.ui.accounttableWidget.setItem(num, 2, datetime)
            self.ui.accounttableWidget.setItem(num, 3, type)
            self.ui.accounttableWidget.setItem(num, 4, price)

        self.ui.accounttableWidget.itemChanged.connect(self.on_item_changed)

    # 刷新表格
    def resettingTable(self):
        self.ui.accounttableWidget.itemChanged.disconnect(self.on_item_changed)
        # 清空表格
        self.ui.accounttableWidget.setRowCount(0)
        # 数据明细查询显示
        result = consumption(getAccountValue())
        for row, num in zip(result, range(0, len(result))):
            # 对要插入的行定义
            self.ui.accounttableWidget.insertRow(num)

            # 修改值类型为QTableWidgetItem
            uuidnum = QTableWidgetItem(str(row[0]))
            # 数据居中
            uuidnum.setTextAlignment(Qt.AlignCenter)
            uuidnum.setFlags(uuidnum.flags() ^ Qt.ItemIsEditable)
            uuidnum.setBackground(QColor(Qt.lightGray).lighter(125))
            datetime = QTableWidgetItem(str(row[1]))
            datetime.setTextAlignment(Qt.AlignCenter)
            datetime.setFlags(datetime.flags() ^ Qt.ItemIsEditable)
            datetime.setBackground(QColor(Qt.lightGray).lighter(125))
            type = QTableWidgetItem(row[2])
            type.setTextAlignment(Qt.AlignCenter)
            price = QTableWidgetItem(str(row[3]))
            price.setTextAlignment(Qt.AlignCenter)

            # 设置某列无法更改
            number = QTableWidgetItem(str(num + 1))
            number.setTextAlignment(Qt.AlignCenter)
            number.setBackground(QColor(Qt.lightGray).lighter(125))
            number.setFlags(number.flags() ^ Qt.ItemIsEditable)

            # 插入数据
            self.ui.accounttableWidget.setItem(num, 0, number)
            self.ui.accounttableWidget.setItem(num, 1, uuidnum)
            self.ui.accounttableWidget.setItem(num, 2, datetime)
            self.ui.accounttableWidget.setItem(num, 3, type)
            self.ui.accounttableWidget.setItem(num, 4, price)
        self.ui.accounttableWidget.itemChanged.connect(self.on_item_changed)

    def insertAccount(self):
        from templates.insertAccount import win_InsertAccount
        SI.insertWin = win_InsertAccount(self)
        SI.insertWin.ui.show()

    def on_item_changed(self, item):
        # 获取修改的uuid
        uuid = self.ui.accounttableWidget.item(item.row(), 1)
        # if item.column()
        # print(item.column(),item.text())
        if item.column() == 4 and item.text() == '0':
            # updateDataByuuid(uuid.text(), item.column(), item.text())
            deleteByAccount(uuid.text())
        else:
            updateDataByuuid(uuid.text(), item.column(), item.text())
        self.resettingTable()

    def deleteData(self):
        uuid = self.ui.accounttableWidget.item(self.ui.accounttableWidget.currentRow(), 1).text()
        print(uuid)
        deleteByAccount(uuid)
        self.resettingTable()

    def lastPage(self):
        subPageValue()
        self.resettingTable()

    def nextToPage(self):
        countRow = countData()
        addPageValue()
        getPageValueNumber = int(getPageValue())
        if int(countRow[0]) - getPageValueNumber > 0:
            self.resettingTable()
        else:
            subPageValue()
            self.resettingTable()

    def jumpPage(self, countPageRowResult):
        page = int(self.ui.pagelineEdit.text().strip())
        if page > countPageRowResult:
            QMessageBox.critical(
                self.ui,
                '失败',
                '超出最大页码'
            )
            return
        else:
            setPageValue((page - 1) * 10)

        self.resettingTable()

    def insertbudget(self):
        result = selectBudget()
        if result is not None and len(result) > 0:
            QMessageBox.critical(
                self.ui,
                '错误',
                '已添加本月预算，请勿重复添加！'
            )
            return

        value, ok = QInputDialog.getDouble(
            None, '预算', '请输入本月的预算金额：', 0, 0, 999999, 1
        )
        # print(value)
        if ok:
            result = insertBudget(value)
            if result:
                QMessageBox.information(
                    self.ui,
                    '成功',
                    '成功添加本月预算'
                )
                return
            else:
                QMessageBox.critical(
                    self.ui,
                    '错误',
                    '添加预算失败'
                )
                return

    def selectBudget(self):
        monthBudget = selectMonthBudget()[0]  # 获取当前月份的总金额
        budgetprice = selectBudget()  # 获取当前月份的预算金额
        # time.sleep(3)
        # print(budgetprice)
        if budgetprice is not None and len(budgetprice) > 0:
            if monthBudget > budgetprice[0]:
                QMessageBox.information(
                    self.ui,
                    '注意',
                    '您的本月消费已超过您设置的本月预算！请注意！'
                )

    def updateBudget(self):
        result = selectBudget()[0]
        if result != '':
            value, ok = QInputDialog.getDouble(
                None, '预算', '请输入本月的预算金额：', 0, 0, 999999, 1
            )
            flag = selectBudgetData(value)
            if flag:
                QMessageBox.information(
                    self.ui,
                    '提示',
                    '成功修改本月预算金额！'
                )
                return
        else:
            self.insertbudget()

    def fileshangchuan(self):
        # self.ui.stackedWidget.setCurrentIndex(3)
        # # 监听上传文件按钮控件
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('选择文件')
        file_dialog.FilterIndex = 1
        file_dialog.setDirectory('C:\\Users\\Admin\\Desktop')
        file_name, file_filter = file_dialog.getOpenFileName()

        # 处理用户选择的文件
        print(file_name)
        if file_name:
            strfile_path = str(file_name).split('.')
            if strfile_path[1] != 'xlsx' and strfile_path[1] != 'xls':
                QMessageBox.critical(
                    self.ui,
                    '错误',
                    '文件类型只能是.xlsx或.xls'
                )
                return

            df = pd.read_excel(file_name)
            # print(df)
            if len(df.columns.values) != 3:
                QMessageBox.critical(
                    self.ui,
                    '错误',
                    '文件内容格式不匹配，格式为：时间，类型，金额'
                )
                return
            df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            rows = df.values
            result = False
            for fields in rows:
                result = insertExecl(fields[0], fields[1], fields[2])
                if result == False:
                    return
            if result:
                QMessageBox.information(
                    self.ui,
                    '成功',
                    '数据上传成功'
                )
                self.resettingTable()
                return
            else:
                QMessageBox.critical(
                    self.ui,
                    '错误',
                    '数据上传失败'
                )
                return

    def fileDownLoad(self):
        value, ok = QInputDialog.getInt(
            None, '输入框', '请输入需要的最新账单信息数：', 0, 0, 1000, 1
        )
        result = selectfileDownLoad(value)
        # print(result)
        # 将数据转换为 Pandas DataFrame
        data = pd.DataFrame(result, columns=['uuid', 'account', 'type', 'price', 'date'])

        # 将数据保存为 Excel 文件
        writer = pd.ExcelWriter('C:\\Users\\Admin\\Downloads\\data.xlsx')
        data.to_excel(writer, index=False)
        writer.save()

        if ok:
            QMessageBox.information(
                self.ui,
                '成功',
                '文件下载成功')

    def updateUser(self):
        SI.updateWin = updateUser.updateUser()
        SI.updateWin.ui.show()
        # self.ui.actionupdateUser.triggered.disconnect()

    def onSignOut(self):
        SI.mainWin.ui.hide()
        SI.loginWin.ui.show()
