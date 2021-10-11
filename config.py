import configparser
import json
import os
# import uuid
# import base64
from redis import Redis, ConnectionPool
import fdb
from dbutils.pooled_db import PooledDB
# from syspath import app_path

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, r"base.ini")  # 读取到本机的配置文件
conf = configparser.ConfigParser()
conf.read(cfgpath)

jsonpath = os.path.join(curpath, r"db\dbconst.json")
with open(jsonpath, 'r') as f:
    data = json.load(f)

DBCONST = dict(data)

httpscrt = conf.get("https", "pathcrt")
httpskey = conf.get("https", "pathkey")

host = conf.get("firebird", "host")
port = conf.getint("firebird", "port")
user = conf.get("firebird", "user")
password = conf.get("firebird", "password")
database = conf.get("firebird", "database")

redishost = conf.get("redis", "host")
redisport = conf.getint("redis", "port")
redispassword = conf.get("redis", "password")

svraddress = conf.get("server", "address")
svrport = conf.getint("server", "port")

pool = ConnectionPool(host=redishost,
                      port=redisport,
                      password=redispassword,
                      decode_responses=True)
redisPool = Redis(connection_pool=pool)

# GUID = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
# BASE_DIRS = os.path.dirname(__file__)
settings = {
    # "template_path": os.path.join(BASE_DIRS, "templates"),
    # "static_path": os.path.join(BASE_DIRS, "statics"),
    "cookie_secret": b'ZAVWU9xhSxeEG8+35JjceYA079lD/EQVgvSC3iXU/P8=',  # GUID,
    # "xsrf_cookies": True
}

PYFDB_POOL = PooledDB(
    creator=fdb,  # 使用链接数据库的模块
    maxconnections=100,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=100,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=100,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=0,  # 链接池中最多共享的链接数量，0和None表示全部共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    charset='UTF8')
'''
jsonpath = app_path() + r"\\db\\dbconst.json"
with open(jsonpath, 'r') as f:
    data = json.load(f)

DBCONST = dict(data)

cfgpath = app_path() + r"\base.ini"
conf = configparser.ConfigParser()
conf.read(cfgpath)
'''
