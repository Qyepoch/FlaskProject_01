import os
# 配置文件，连接数据库
hostname = '127.0.0.1'
port = '3306'
database = 'qa_platform'
username = 'root'
password = '064516'
DB_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8'

SQLALCHEMY_DATABASE_URI = DB_URI


#邮箱配置信息
MAIL_SERVER ="smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME ="qyepoch@qq.com"
MAIL_PASSWORD ="ayljbiwdpgdzdaif"
MAIL_DEFAULT_SENDER ="3281187584@qq.com"




#加密cookis中的信息就像吃饭的”盐“
# SECRET_KEY = os.urandom(24)
SECRET_KEY = "ababbababababxsxsxswsws"