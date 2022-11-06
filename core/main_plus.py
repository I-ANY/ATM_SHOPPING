'''
用户层视图层：
主要是展示界面信息（系统运行之后用户所能看到的），所有的数据处理都通过函数传到逻辑接口层进处理然后返回。
'''

import os
from lib import common
from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from conf import setting

login_user = None

def run():
    '''执行函数：分别调用其他函数'''
    mean1='''
======= Wellcome to ANY’s world =======
            1:用户注册
            2:用户登录
            3:管理员
            q:退出
    '''
    mean2='''
        1:查看余额
        2:提现
        3:还款
        4:转账
        5:查看流水
        6:商城
        b:返回上一级
    '''
    mean_dict1 = {
        "1":register,
        "2":login,
        "3":manage,
    }
    mean_dict2 = {
        "1": show_balance,
        "2": withdraw,
        "3": repay,
        "4": transfer,
        "5": show_flow,
        "6": market,
    }

    while True:
        print(mean1)
        choice = input("请选择>>>").strip()
        if choice in mean_dict1:
                mean_dict1.get(choice)()
        elif choice == "q":
            exit("欢迎再次使用！")
        else:
            print("无此选项，重新输入！")
            continue

def register():
    '''用户层用户注册函数'''
    while True:
        username = input("用户名：").strip()
        if username:
            file_path = os.path.join(setting.DB_PATH, f"{username}.json")
            if os.path.exists(file_path):
                print("该用户名已存在，请重新输入！")
                continue
            else:
                passwd = input("密码：").strip()
                re_passwd = input("确认密码：").strip()
                if passwd == re_passwd:
                    #传参给接口层进行注册
                    flag = user_interface.register_interface(username,passwd,balance=1000)
                    if flag:
                        print("%s用户注册成功！" %username)
                    else:
                        print("%s用户注册失败！" %username)
                    break
        else:
            print("输入错误！")

def login():
    '''用户层登录函数'''
    mean2='''
        1:查看余额
        2:提现
        3:还款
        4:转账
        5:查看流水
        6:商城
        b:返回上一级
    '''
    mean_dict2 = {
        "1": show_balance,
        "2": withdraw,
        "3": repay,
        "4": transfer,
        "5": show_flow,
        "6": market,
    }
    count = 0
    flag = True
    while flag:
        username = input("用户名：").strip()
        if username:
            file_path = os.path.join(setting.DB_PATH, f"{username}.json")
            if os.path.exists(file_path):
                while flag:
                    passwd = input("密码：").strip()
                    passwd = common.get_pwd_md5(passwd)
                    #调用逻辑层函数进行登录根据返回的数据进行判断是否登录成功
                    user_data = user_interface.login_interface(username,passwd)
                    if user_data:
                        global login_user  #全局变量
                        login_user = username
                        while flag:
                            print(mean2)
                            choice = input("请选择>>>").strip()
                            if choice in mean_dict2:
                                mean_dict2.get(choice)(username)
                            elif choice == "b":
                                flag = False
                            else:
                                print("输入错误！")
                    else:
                        count +=1
                        print("密码错误！")
                        if count >3:
                            print("重复超过3次密码错误！退出！")
                            flag = False
                        else:
                            continue
            else:
                print("用户不存在，重新输入！")
        else:
            print("输入错误！")

@common.login_auth    #使用装饰器进行认证登录（在此只是为了展示功能使用，这里可以不用到装饰器）
def show_balance(username):
    '''显示余额'''
    balance = bank_interface.show_balance_interface(username)
    print("余额为：{}".format(float(balance)))

def withdraw(username):
    '''提现'''
    money = input("提现金额：").strip()
    if money.isdigit() and float(money)>0:
        money = float(money)
        balance,msg = bank_interface.withdraw_interface(username,money)
        print(msg)
    else:
        print("输入错误！")

def repay(username):
    '''还款'''
    money = input("还款金额：").strip()
    if money.isdigit() and float(money) > 0:
        money = float(money)
        flag,msg = bank_interface.repay_interface(username,money)
        print(msg)
    else:
        print("输入错误！")

def transfer(username):
    '''转账'''
    money = input("转账金额：").strip()
    if money.isdigit() and float(money) > 0:
        money = float(money)
        to_username = input("对方账户：").strip()
        flag ,msg = bank_interface.transfer_interface(username,to_username,money)
    else:
        print("输入错误！")

def show_flow(username):
    '''显示流水'''
    flag,msg = bank_interface.show_flow_interface(username)
    print(msg)

def market(username):
    '''商城'''
    mean4='''
    1:查看商品,
    2:查看购物车,
    3:清空购物车,
    4:管理购物车,
    b:返回上一级,
    '''
    mean_dict4={
        "1":show_good,
        "2":show_car,
        "3":pay_car,
        "4":manage_car,
    }
    while True:
        print(mean4)
        choice = input("请选择：").strip()
        if choice in mean_dict4:
            mean_dict4.get(choice)(username)
        elif choice == "b":
            break
        else:
            print("输入错误！")

def show_good(username):
    '''显示商城商品'''
    good_list = [
        ["matebook", 1000],
        ["macbook", 10000],
        ["huawei P50", 500],
        ["xiaomi 11", 10],
        ["显示器", 10],
    ]
    shop_dict = {}  # {{商品名称：{价格：xx，数量：xx},{商品名称：{价格：xx，数量：xx}}
    while True:
        print("="*20,"Wellcom to shopping","="*20)
        for index, good_info in enumerate(good_list):
            print(f"{index + 1} - 商品名称：{good_info[0]}   价格：{good_info[1]}")
        print("b返回上一级")
        print("已经选择商品：", shop_dict)
        choice = input("选择商品(y支付|n添加到购物车|c修改选择)：")
        if choice.isdigit() and int(choice) in range(1, len(good_list) + 1):
            #判断商品是否已经在例表中，如果在了就数量+1，不在就添加
            if good_list[int(choice)-1][0] in shop_dict:
                shop_dict[good_list[int(choice)-1][0]]["数量"] += 1
            else:
                shop_dict[good_list[int(choice)-1][0]] = {"价格": good_list[int(choice)-1][1], "数量": 1}
        elif choice == "y":
            if shop_dict:
                # 调用支付接口
                flag , msg = shop_interface.pay_interface(username,shop_dict)
                if flag:
                    break
            else:
                print("没有选择商品！")
                continue
        elif choice == "a":
            if shop_dict:
                # 调用添加购物车接口
                flag , msg = shop_interface.add_car_interface(username,shop_dict)
                print(msg)
                if flag:
                    break
            else:
                print("没有选择商品！")
                continue
        elif choice == "c":
            if shop_dict:
                # 修改已经选择的商品数量
                enter = input("要修改的商品：").strip()
                if enter in shop_dict:
                    count = input("修改数量为：").strip()
                    if count.isdigit():
                        if int(count) != 0:
                            shop_dict[enter]["数量"] = int(count)
                        else:
                            shop_dict.pop(enter)
                    else:
                        print("请正确输入！")
                else:
                    print("抱歉，您还没有选择该商品！")
            else:
                print("抱歉，您还没有选择商品！")
                continue
        elif choice == "b":
            break
        else:
            print("输入错误！")

def show_car(suername):
    '''显示购物车'''
    shop_car =  shop_interface.show_car_interface(suername)
    print(shop_car)

def pay_car(username):
    '''清空购物车'''
    flag , msg = shop_interface.pay_interface(username)
    print(msg)

def manage_car(username):
    '''管理购物车（修改商品数量）'''
    good = input("请输入商品：").strip()
    new_count = input("修改数量为：").strip()
    if new_count.isdigit():
        flag,msg = shop_interface.manage_car_interface(username,good,int(new_count))
        print(msg)
    else:
        print("输入数量错误！")

def manage():
    '''管理员入口'''
    mean3 = '''
======= 管理员 ======
    1、修改用户ID
    2、修改用户密码
    3、修改用户金额
    4、冻结客户
    b、返回上一级
    '''
    mean_dict3 = {
    "1":"a",
    "2":"b",
    "3":"c",
    "4":"d",
    }
    flag = True
    count = 1
    while flag:
        manage_user = input("管理员：").strip()
        manage_pw = input("管理员密码：").strip()
        flag1,msg = user_interface.manage_login(manage_user,manage_pw)
        while flag1:
            print(mean3)
            choice = input("请选择：").strip()
            if choice in mean_dict3:
                while True:
                    username = input("要操作的用户：").strip()
                    value = input("输入新值：").strip()
                    flag3,msg = bank_interface.manage_interface(username,mean_dict3.get(choice),value)
                    if flag3:
                        print(msg)
                        break
                    else:
                        print(msg)
                        continue
            elif choice == "b":
                flag = False
                break
            else:
                print("输入错误！")
                continue
        else:
            #三次输入错误返回上级
            count +=1
            print(msg)
            if count >3:
                flag = False
            else:
                continue