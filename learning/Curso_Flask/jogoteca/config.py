import os

SECRET_KEY = 'matheus'
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Senha123"
MYSQL_DB = "jogoteca"
MYSQL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
