from loguru import logger

from myutil.mysql_diver import mysql_diver
from myutil import global_var as gl
from myutil.ssh_diver import ssh_diver

config = dict()
config['mysql_db'] = {'host': '192.168.31.116',
                      'port': '3306',
                      'username': 'root',
                      'password': '123456',
                      'database': 'sys'}

config['ssh'] = {'host': '192.168.31.116',
                 'port': '22',
                 'username': 'root',
                 'password': '123456'}


# 获取config配置文件
def get_config(section, key, default: str = None):
    if config[section][key] is None:
        return default
    return config[section][key]


DB_HOST: str = get_config("mysql_db", "host", default="127.0.0.1")
DB_PORT: int = int(get_config("mysql_db", "port", default="3306"))
DB_USERNAME: str = get_config("mysql_db", "username", default="root")
DB_PASSWORD: str = get_config("mysql_db", "password", default="")
DB_DATABASE: str = get_config("mysql_db", "database", default="sys")

SSH_HOST: str = get_config("ssh", "host", default="127.0.0.1")
SSH_PORT: int = int(get_config("ssh", "port", default="22"))
SSH_USERNAME: str = get_config("ssh", "username", default="root")
SSH_PASSWORD: str = get_config("ssh", "password", default="")


def __init():
    mysql_connect(host=DB_HOST, port=DB_PORT, database=DB_DATABASE, user=DB_USERNAME, password=DB_PASSWORD)
    ssh_connect(host=SSH_HOST, port=SSH_PORT, user=SSH_USERNAME, password=SSH_PASSWORD)


def mysql_connect(host, port, database, user, password):
    try:
        a = mysql_diver(host=host, port=port, database=database, user=user, password=password)
        if not a.status:
            b = 1 / 0
        gl.set_value("mysql_diver", a)
        logger.info("数据库连接成功")
    except:
        logger.info("数据库连接失败")


def ssh_connect(host, port, user, password):
    try:
        a = ssh_diver(host=host, port=port, user=user, password=password)
        gl.set_value("ssh_diver", a)
        logger.info("ssh连接成功")
    except:
        logger.info("ssh连接失败")
