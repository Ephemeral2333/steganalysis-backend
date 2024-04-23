import os


# MySQL
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'steganalysis'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

#Mail Config
MAIL_SERVER = 'smtpdm.aliyun.com'
MAIL_PROT = 80
MAIL_USERNAME = "steganalysis_admin@lili73.xyz"
MAIL_PASSWORD = "LIyh198673"
MAIL_DEFAULT_SENDER = "steganalysis_admin@lili73.xyz"