'''配置文件'''

import os
import time

#项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#用户信息文件存放路径
DB_PATH = os.path.join(BASE_DIR,"db","accounts")
#日志文件
LOG_PATH = os.path.join(BASE_DIR,"logs")

#设置管理员账号密码
MANAGE_NAME = "manage"
MANAGE_PASSWD = "123"

#时间
DATE = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

