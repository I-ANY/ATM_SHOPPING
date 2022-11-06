import os
import sys

#创建路径环境变量，让其可识别到所有的它同级目录下的其他目录下的包
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
#添加环境变量
sys.path.append(BASE_DIR)

from core import main_plus

#程序入口
if __name__ == "__main__":
    main_plus.run()
