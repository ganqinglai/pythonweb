import secrets
import string
# import hashlib
import time
import datetime
import decimal
import json
import jwt
import uuid
import base64
from config import redisPool
# from methods.firebirddb import FdbObj

token = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
# print(token)
'''
m = hashlib.md5()
with open(r'D:/2.png', 'rb') as f:
    for line in f:
        m.update(line)
# print(m.hexdigest())  # 47a6b079cc33a4f312786b46e61e0305

m = hashlib.md5()
with open(r'F:/2.png', 'rb') as f:
    for line in f:
        m.update(line)
# print(m.hexdigest())
'''

alphanum = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphanum) for i in range(4))
# print(password)

alphanum = string.digits
password = ''.join(secrets.choice(alphanum) for i in range(6))
# print(password)

ticks = time.time()
# print('当前时间戳： ', ticks)

new_ticks = str(ticks).replace('.', '')


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S.%f')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.time):
            return o.strftime('%X')
        elif isinstance(o, decimal.Decimal):
            return float(o)


# pip install PyJWT
'''
"""headers 中一些固定参数名称的意义"""
# jku: 发送JWK的地址；最好用HTTPS来传输
# jwk: 就是之前说的JWK
# kid: jwk的ID编号
# x5u: 指向一组X509公共证书的URL
# x5c: X509证书链
# x5t：X509证书的SHA-1指纹
# x5t#S256: X509证书的SHA-256指纹
# typ: 在原本未加密的JWT的基础上增加了 JOSE 和 JOSE+ JSON。JOSE序列化后文会说及。适用于JOSE标头的对象与此JWT混合的情况。
# crit: 字符串数组，包含声明的名称，用作实现定义的扩展，必须由 this->JWT的解析器处理。不常见。

"""payload 中一些固定参数名称的意义, 同时可以在payload中自定义参数"""
# iss 【issuer】发布者的url地址
# sub 【subject】该JWT所面向的用户，用于处理特定应用，不是常用的字段
# aud 【audience】接受者的url地址
# exp 【expiration】 该jwt销毁的时间；unix时间戳
# nbf 【not before】 该jwt的使用时间不能早于该时间；unix时间戳
# iat 【issued at】 该jwt的发布时间；unix 时间戳
# jti 【JWT ID】 该jwt的唯一ID编号
'''
# headers = {"typ": "JWT", "alg": "HS256"}
# payloadb = {"username": "gan", "pwd": "888"}
payloada = {
    'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
    'iat': datetime.datetime.now(),  # 开始时间
    'iss': 'visen',  # 签名
}


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def sf_EncodeJwt(payload):
    payload = Merge(payloada, payload)
    jwtToken = jwt.encode(payload, 'visen', algorithm='HS256')  # 加密生成字符串
    return jwtToken


def sf_DecodeJwt(jwtToken):
    rData = jwt.decode(jwtToken, 'visen', issuer='visen',
                       algorithms=['HS256'])  # 解密，校验签名
    '''
    可以通过MD5，根据注册信息生成token
    print(hashlib.md5(str(rData).encode(encoding='UTF-8')).hexdigest())
    '''
    return rData


async def sf_UsrAuth(jwttoken):
    jwtDict = sf_DecodeJwt(jwttoken)
    username = jwtDict.get("username")
    pwd = jwtDict.get("pwd")
    exp = jwtDict.get("exp")
    if not redisPool.hexists(name="czy", key=username):
        return False
    else:
        datetime_array = datetime.datetime.utcfromtimestamp(exp)
        expDateTime = datetime_array.strftime("%Y-%m-%d %H:%M:%S")
        nowDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        oldDateTime = datetime.datetime.strptime(expDateTime,
                                                 "%Y-%m-%d %H:%M:%S")
        newDateTime = datetime.datetime.strptime(nowDateTime,
                                                 "%Y-%m-%d %H:%M:%S")
        oldTime = int(time.mktime(oldDateTime.timetuple()))
        newTime = int(time.mktime(newDateTime.timetuple()))
        vMinutes = newTime - oldTime
        if vMinutes > 0:
            return False
        else:
            password = redisPool.hget("czy", username)
            if password == pwd:
                return True
            else:
                return False


'''
# https://www.jianshu.com/p/69e486be412f
# 生成服务器端私钥
openssl genrsa -out server.key 1024
# 生成证书
openssl req -new -x509 -key server.key -out server.crt -days 3650
# 生成服务器端公钥
openssl rsa -in server.key -pubout -out server.pem
----------------------------------------------------------------------------------------------------
'''
