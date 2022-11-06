'''
公共方法
'''

import logging
import hashlib
from conf import setting
from core import main_plus

def login_auth(func):
    '''函数装饰器：增加用户登录认证'''
    def inner(*args,**kwargs):
        if main_plus.login_user:
            res = func(*args,**kwargs)
            return res
        else:
            print("客户未登录！")
            main_plus.login()
    return inner

def get_pwd_md5(passwd):
    '''密码加密'''
    md = hashlib.md5()
    md.update(passwd.encode("utf-8"))
    salt = "any"
    md.update(salt.encode("utf-8"))
    return md.hexdigest()

def log_write(log_data):
    '''日志记录'''
    log_file = setting.LOG_PATH + '/logs.log'
    curr_date = setting.DATE
    log = curr_date + '   ' + log_data
    with open(log_file,'a+') as fp:
        fp.write("%s\n" %log)

    #感兴趣的同学可以尝试使用logging模块来实现
    '''
    # 设置一个basicConfig只能输出到一个Handler
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='w')
    logging.info(log_data)
    '''