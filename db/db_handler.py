import os,json
from conf import setting

def select(username):
    #接收用户层传进来的用户名称并进行校验
    file_path = os.path.join(setting.DB_PATH,f"{username}.json")
    if os.path.exists(file_path):
        with open(file_path,'r',encoding='utf-8') as fp:
            uaser_data = json.load(fp)
            if uaser_data["username"] == username:
                return uaser_data

def save(user_data):
    file_path = os.path.join(setting.DB_PATH, f"{user_data.get('username')}.json")
    if os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as fp:
            uaser_data = json.dump(user_data,fp)