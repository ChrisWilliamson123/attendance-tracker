import os

MYSQL_USER = os.getenv('MYSQL_USER', 'admin')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_DB = os.getenv('MYSQL_DB', 'test')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
