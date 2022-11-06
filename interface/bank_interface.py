'''
逻辑处理层：有关银行的数据处理
'''

import os
import time
from lib import common
from db import db_handler
from conf import setting

date = setting.DATE
def show_balance_interface(username):
    '''查询余额接口'''
    user_data = db_handler.select(username)
    return user_data.get("balance")

def withdraw_interface(username,money):
    '''提现接口'''
    fare = 0.05 #利率
    user_data = db_handler.select(username)
    if user_data.get("status") == "True":
        money2 = money*(fare+1)
        user_data['balance'] -= money2
        user_data['flow'].append(f"{date} 提现：{money},利率：{money*fare}")
        db_handler.save(user_data)
        return user_data['balance'] ,f"成功提现：{money},利率为：{money*fare},余额为：{user_data['balance']}"
    else:return 0,"账户被冻结，请联系管理员进行解冻！"

def repay_interface(username,money):
    '''还款接口'''
    user_data = db_handler.select(username)
    if user_data.get("status") == "True":
        user_data["balance"] += money
        user_data['flow'].append(f"{date} 还款：{money}")
        db_handler.save(user_data)
        return True ,f"还款成功，余额为：{user_data['balance']}"
    else:
        return False,"账户被冻结，请联系管理员进行解冻！"

def transfer_interface(username,to_username,money):
    '''转账接口'''
    money = float(money)
    user_data = db_handler.select(username)
    to_user_data = db_handler.select(to_username)
    if user_data.get("status") == "True":
        if to_user_data:
            fare = 0.05
            money2 = money*(1+0.05)
            user_data['balance'] -= money2
            to_user_data['balance'] += money
            user_data['flow'].append(f"{date} 转账：{money},利率：{money * fare}")
            to_user_data['flow'].append(f"{username}转账：{money}")
            db_handler.save(user_data)
            db_handler.save(to_user_data)
            return True,f"转账成功！"
        else:
            return False,f"还款失败，{to_username}用户不存在，请确认！"
    else:return False,"账户被冻结，请联系管理员进行解冻！"

def show_flow_interface(username):
    '''查询流水接口'''
    user_data = db_handler.select(username)
    return True, user_data["flow"]

def manage_interface(username,commond,value):
    '''管理员操作接口'''
    user_data = db_handler.select(username)
    if user_data:
        if commond == "a":
            old_file_path = os.path.join(setting.DB_PATH, f"{user_data.get('username')}.json")
            new_file_path = os.path.join(setting.DB_PATH, f"{value}.json")
            user_data["username"] = value
            os.rename(old_file_path,new_file_path)
        elif commond == "b":
            value = common.get_pwd_md5(value)
            user_data["passwd"] = value
        elif commond == "c":
            user_data["balance"] = value
        elif commond =="d":
            user_data["status"] = value
        db_handler.save(user_data)

        return True, "修改成功！"
    else:
        return False,"该用户不存在，从新输入！"