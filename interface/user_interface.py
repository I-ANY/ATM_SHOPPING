'''
逻辑接口层：用户的数据处理
'''

import json
import os
import time
from lib import common
from conf import setting
from db import db_handler

def register_interface(username,passwd,balance):
    '''接口层用户注册'''
    date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    passwd = common.get_pwd_md5(passwd)
    user_dict = {
        "username": username,
        "passwd": passwd,
        "balance": balance,
        "flow":[],
        "shop_car":{},
        "status": True,
        "open_date": date,
    }
    file_path = os.path.join(setting.DB_PATH, f'{user_dict.get("username")}.json')
    with open(file_path,'w',encoding="utf-8") as fp:
        json.dump(user_dict,fp)
    return True

def login_interface(username,passwd):
    '''用户登录接口'''
    user_data = db_handler.select(username)
    if passwd == user_data["passwd"]:
        return user_data

def manage_login(manage_user,manage_pw):
    '''管理员登录接口'''
    if manage_user == setting.MANAGE_NAME:
        if manage_pw == setting.MANAGE_PASSWD:
            return True, "管理员认证成功！"
        else:
            return False, "密码错误！"
    else:
        return False, "管理员错误！"