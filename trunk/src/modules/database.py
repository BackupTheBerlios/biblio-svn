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
    def check(self,type,var):
        if type=="isbn":
            return
        elif type=="text":
            return
        elif type=="date":
            return
        elif type=="nr":
            return
        else:
            raise
    def __del__(self):
        try:
            con.close()
        except:
            raise