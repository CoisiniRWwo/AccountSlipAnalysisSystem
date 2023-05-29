def _init():  # 初始化账号
    global account
    account = [1]


def setAccountValue(fields):  # 为全局变量执行赋值
    account[0] = fields


def getAccountValue():  # 取出全局变量的值
    return account[0]


def page_init():
    global page_number
    page_number = [0]


def addPageValue():
    page_number[0] += 10


def subPageValue():
    if page_number[0] - 10 < 0:
        page_number[0] = 0
    else:
        page_number[0] -= 10


def setPageValue(value):
    page_number[0] = value


def getPageValue():
    return page_number[0]


def code_init():
    global code_number
    code_number = [0]


def setCodeValue(value):
    code_number[0] = value


def getCodeValue():
    return code_number[0]
