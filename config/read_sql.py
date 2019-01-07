import json
import os


# 获取MySQL的配置文件
import pymysql


def get_mysql_conf():
    user_home = os.environ.get("HOME")
    conf_base_path = user_home + "/conf"
    mysql_conf_path = conf_base_path + "/mysql.conf"
    with open(mysql_conf_path, "r") as f1:
        res_str = f1.read()
    mysql_dict = json.loads(res_str)
    return mysql_dict


# 链接数据库,返回db对象
def get_mysql_db():
    # 获取配置文件
   # mysql_dict = get_mysql_conf()
    #链接数据库
    connection=pymysql.connect(
        host="0.0.0.0",
        user="root",
        password="xml123",
        port=3306,
        db="books",charset='utf8')
    return connection
