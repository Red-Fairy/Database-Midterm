class Config(object):

    # 数据库的配置
    DIALCT = "mysql"
    DRITVER = "pymysql"
    HOST = '127.0.0.1'
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = "rainsheep@321212"
    DBNAME = 'tlatpku'

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SQLALCHEMY_DATABASE_URI = f"{DIALCT}+{DRITVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# 密钥，可随意修改
SECRET_KEY = 'redfairy'

# 输入限制

USER_NAME_REGEX = '[0-9A-Fa-f]{1,20}'
PASSWORD_REGEX = '[0-9A-Fa-f]{1,20}'