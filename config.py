import os

DEBUG = True

# or.urandom(24):利用os模块的urandom()函数生成一个24位的随机字符串
SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlktqa'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD,
                                                              HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
