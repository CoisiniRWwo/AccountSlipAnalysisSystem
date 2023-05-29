import hashlib


def sha256(arg):
    sha256_pwd = hashlib.sha256()
    sha256_pwd.update(arg.encode('utf8'))
    return sha256_pwd.hexdigest()
