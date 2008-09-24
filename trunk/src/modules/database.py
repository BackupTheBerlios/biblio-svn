import MySQLdb as mysql

class Database():
    def __init__(self):
        mysql.connect()