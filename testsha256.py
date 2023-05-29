import hashlib


def sha256(arg):
    sha256_pwd = hashlib.sha256()
    sha256_pwd.update(arg.encode('utf8'))
    return sha256_pwd.hexdigest()


def log(user, pwd):
    with open('db', 'r', encoding='utf-8') as f:
        for line in f:
            u, p = line.strip().split('|')
            if u == user and p == sha256(pwd):
                return True


def register(user, pwd):
    with open('db', 'a', encoding='utf-8') as f:
        temp = user + '|' + sha256(pwd)
        f.write(temp)


i = input('1表示登录，2表示注册：')
if i == '2':
    user = input('请输入用户名：')
    pwd = input('请输入密码：')
    register(user, pwd)
elif i == '1':
    user = input('请输入用户名：')
    pwd = input('请输入密码：')
    r = log(user, pwd)
    if r == True:
        print('登录成功！')
    else:
        print('登录失败!')
else:
    print('账号不存在')