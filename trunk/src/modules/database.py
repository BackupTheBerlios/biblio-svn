import MySQLdb as mysql

class Database():
    host='pc17'
    user='biblio'
    pw='test'
    def __init__(self):
        try:
            con=mysql.connect(host=host,user=user,passwd=pw)
            cur=con.cursor
        except:
            raise
    def query(self,sqlcode):
        try:
            cur.execute(sqlcode)
            ret=cur.fetchall()
        except:
            raise
        return ret
    def __del__(self):
        try:
            con.close()
        except:
            raise