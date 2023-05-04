import jwt
import datetime
import time
from jwt.exceptions import ExpiredSignatureError

# 全局密钥
secret = 'xxx'


# 生成token
def encode_func(user):
    # user = {'id': 1, 'password':12121}
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
        'iat': datetime.datetime.now() - datetime.timedelta(days=1),  # 开始时间
        'iss': 'wufang',  # 签发者
        'data': user
    }
    encoded = jwt.encode(dic, secret, algorithm='HS256')
    # print('encoded->', encoded)
    return encoded


# 解析token
def decode_func(token):
    decode = jwt.decode(token, secret, issuer='wufang', algorithms=['HS256'])
    print(decode)
    # 返回解码出来的data
    return decode['data']



# if __name__ == '__main__':
#     print('生成token，解析token', '-' * 50)
#     encoded = encode_func()
#     decode_func(encoded)

    # print('exp token', '-' * 50)
    # token = encode_exp_func()
    # time.sleep(3)
    # decode_exp_func(token=token)
