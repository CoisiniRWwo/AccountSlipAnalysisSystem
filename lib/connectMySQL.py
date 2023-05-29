import pymysql, uuid, datetime
from lib.glob import getAccountValue, getPageValue

conn = pymysql.connect(host="localhost", user="root", password="010111", database="account_system")

cursor = conn.cursor()


def login(account, password):
    sql = 'select * from userinfo where account = %s and password = %s'
    value = (account, password)
    cursor.execute(sql, value)
    result = cursor.fetchone()
    if result != None:
        print('登录查询：id:%s,account:%s,pawssword:%s,username:%s' % (
            result[0], result[1], result[2], result[3]))
        return True
    else:
        print("账号密码错误")
        return False


def rsegister(raccount, rusername, rpassword):
    try:
        sql = 'insert into userinfo (id,account,password,username) values (null ,%s,%s,%s)'
        value = (raccount, rpassword, rusername)
        cursor.execute(sql, value)
        conn.commit()
        print("注册成功")
        return True
    except pymysql.Error as e:
        print("注册失败")
        # connect().rollback()
        # connect().close()
        return False


def consumption(account):
    sql = 'select uuid,date,type,price from consumption where account = %s order by date desc limit %s,10'
    value = (account, getPageValue())
    cursor.execute(sql, value)
    result = cursor.fetchall()
    # cursor.close()
    return result


def searchDataSQL(startDateTime, endDateTime, method):
    if method is None:
        sql = 'select * from consumption where date between %s and %s'
        value = (startDateTime, endDateTime)
        cursor.execute(sql, value)
        print("查询成功")
    else:
        sql = 'select * from consumption where date between %s and %s and type = %s'
        value = (startDateTime, endDateTime, method)
        cursor.execute(sql, value)
        print("查询成功")
    result = cursor.fetchall()
    return result


def selectNameByAccount(account):
    sql = 'select username from userinfo where account = %s'
    cursor.execute(sql, account)
    return cursor.fetchone()


def insertByaccount(account, type, price):
    try:
        sql = 'insert into consumption value (%s,%s,%s,%s,%s)'
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        value = (suid, account, type, price, now)
        cursor.execute(sql, value)
        conn.commit()
        print("添加账单成功")
        return True
    except pymysql.Error as e:
        print("添加账单失败")
        # connect().rollback()
        # connect().close()
        return False


def updateDataByuuid(uuid, column, fields):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        if column == 3:
            sql = 'update consumption set type = %s , date = %s where account = %s and uuid = %s '
            value = (str(fields), now, getAccountValue(), uuid)
            cursor.execute(sql, value)
            conn.commit()
            print("修改账单成功")
            return True
        elif column == 4:
            sql = 'update consumption set price = %s , date = %s where account = %s and uuid = %s '
            value = (fields, now, getAccountValue(), uuid)
            cursor.execute(sql, value)
            conn.commit()
            print("修改账单成功")
            return True
    except pymysql.Error as e:
        print('修改失败')
        return False


def countData():
    sql = 'select count(*) from consumption where account = %s'
    cursor.execute(sql, getAccountValue())
    return cursor.fetchone()


def everyDayCountPrice(year, month):
    if month == '':
        sql = 'select MONTH(date) as month, sum(price) as sumprice from consumption where year(date) = %s and account = %s group by month'
        value = (year, getAccountValue())
        cursor.execute(sql, value)
    else:
        sql = 'select Day(date) as day, sum(price) as sumprice from consumption where year(date) = %s and MONTH(date) = %s and account = %s group by day '
        value = (year, month, getAccountValue())
        cursor.execute(sql, value)
    return cursor.fetchall()


def everyDayCountType(year, month):
    if month == '':
        sql = 'SELECT type, sum( price ) AS sumprice FROM consumption WHERE  YEAR( DATE ) = %s  AND account = %s GROUP BY type ORDER BY type'
        value = (year, getAccountValue())
        cursor.execute(sql, value)
    else:
        sql = 'SELECT type, sum( price ) AS sumprice FROM consumption WHERE  YEAR( DATE ) = %s AND MONTH(date) = %s  AND account = %s GROUP BY type ORDER BY type'
        value = (year, month, getAccountValue())
        cursor.execute(sql, value)
    return cursor.fetchall()


def insertExecl(datetime, type, price):
    try:
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        sql = 'insert into consumption values (%s,%s,%s,%s,%s)'
        value = (suid, getAccountValue(), type, price, datetime)
        cursor.execute(sql, value)
        conn.commit()
        print('添加成功')
        return True
    except pymysql.Error as e:
        print('添加失败')
        return False


def selectfileDownLoad(num):
    sql = 'select * from consumption where account = %s order by date desc limit %s'
    value = (getAccountValue(), num)
    cursor.execute(sql, value)
    return cursor.fetchall()


def deleteByAccount(suuid):
    try:
        sql = 'delete from consumption where account = %s and uuid = %s'
        value = (getAccountValue(), suuid)
        cursor.execute(sql, value)
        conn.commit()
        print('删除成功')
    except pymysql.Error as e:
        print("删除失败")


def selectMonthBudget():
    try:
        sql = 'select sum(price) from consumption where account = %s and year(date) = %s and month(date) = %s'
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        values = (getAccountValue(), current_year, current_month)
        cursor.execute(sql, values)
        return cursor.fetchone()
    except pymysql.Error as e:
        print('查询失败：', e)


def insertBudget(budget):
    try:
        sql = 'insert into budget values (null,%s,%s,%s)'
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        value = (getAccountValue(), now, budget)
        cursor.execute(sql, value)
        conn.commit()
        print('添加预算成功')
        return True
    except pymysql.Error as e:
        print("添加预算失败，错误信息：", e)
        return False


def selectBudget():
    sql = 'select budget from budget where account = %s and year(date) = %s and month(date) = %s'
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    values = (getAccountValue(), current_year, current_month)
    cursor.execute(sql, values)
    return cursor.fetchone()


def selectBudgetData(budget):
    try:
        sql = 'update budget set budget = %s where account = %s and year(date) = %s and month(date) = %s'
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        value = (budget, getAccountValue(), current_year, current_month)
        cursor.execute(sql, value)
        conn.commit()
        print('修改预算成功')
        return True
    except pymysql.Error as e:
        print("修改预算失败，错误信息：", e)
        return False

def authentication():
    sql = 'select * from userinfo where account = %s'
    cursor.execute(sql, getAccountValue())
    return cursor.fetchone()

def updateUserData(username):
    try:
        sql = 'update userinfo set username = %s where account = %s'
        values = (username,getAccountValue())
        cursor.execute(sql, values)
        conn.commit()
        print('修改账号成功')
        return True
    except pymysql.Error as e:
        print("修改账号失败，错误信息：", e)
        return False

def updateUserDataBypwd(username,password):
    try:
        sql = 'update userinfo set username = %s,password = %s where account = %s'
        values = (username,password,getAccountValue())
        cursor.execute(sql, values)
        conn.commit()
        print('修改账号成功')
        return True
    except pymysql.Error as e:
        print("修改账号失败，错误信息：", e)
        return False