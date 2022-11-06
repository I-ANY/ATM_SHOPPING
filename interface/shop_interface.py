'''
逻辑接口层：商城的数据处理
'''

from db import db_handler
from conf import setting

date = setting.DATE

def add_car_interface(username,shop_dict):
    '''逻辑层添加购物车接口'''
    user_data = db_handler.select(username)
    # 判断购物车是否为空，为空的话直接添加购物列表
    if not user_data["shop_car"]:
        user_data["shop_car"] = shop_dict
    else:
        #先判断购物车里面是否有相同的商品，如果已经存在就增加数量
        for good_name,info in shop_dict.items():
            if good_name in user_data["shop_car"].keys():
                user_data["shop_car"][good_name]["数量"] += info["数量"]
            else:
                user_data["shop_car"][good_name] = info
    db_handler.save(user_data)
    return True,"添加购物车成功"

def show_car_interface(username):
    '''查看购物车'''
    user_data = db_handler.select(username)
    return user_data["shop_car"]

def pay_interface(*args):
    '''支付接口'''
    user_data = db_handler.select(args[0])
    #判断是购物车支付还是选择商品之后直接支付的
    if len(args)>1:
        shop_dict = args[1]
    else:
        shop_dict = user_data["shop_car"]
    if shop_dict:
        sum = 0
        for info in shop_dict.values():
            sum += info["价格"] * info["数量"]
        if user_data["balance"] >= sum:
            user_data["balance"] -= sum
            if len(args) == 1:
                user_data["shop_car"].clear()
            user_data["flow"].append(f"{date} 商城支付：{sum}")
            db_handler.save(user_data)
            return True,"已经完成支付！"
        else:
            return False,"余额不足，支付失败！"
    else:
        return False,"还未选择商品！"

def manage_car_interface(username,good,new_count):
    '''管理购物车接口'''
    user_data = db_handler.select(username)
    if user_data["shop_car"]:
        user_data["shop_car"][good]["数量"] = new_count
        db_handler.save(userdata)
        return True,"修改成功！"
    else:
        return False,"购物车为空！"