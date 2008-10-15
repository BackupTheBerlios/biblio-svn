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
            if len(var)==13: ##ISBN 13
                for i in range(0,11):
                    if type(var[i])!="int": ##Pruefe auf Zahlen
                        return False
                    if (i%2)==1:
                        pruef+=3*var[i]
                    else:
                        pruef+=var[i]
                if var[12]==(((10-pruef)%10)%10): ##Pruefziffernkontrolle
                    return True

            if len(var)==10: ##ISBN 10
                for i in range(0,8):
                    if type(var[i])!="int": ##Pruefe auf Zahlen
                        return False
                    pruef+=i*var[i]
                if (pruef%11)!=10 and var[9]==(pruef%11): ##Pruefziffernkontrolle
                    return True
                elif (pruef%11)==10 and var[9]=="X": ##Pruefziffernkontrolle
                    return True
        elif type=="text":

            return
        elif type=="date":
            from time import strftime
            if len(var)==4 and var>-3000 and var<int(strftime("%Y")):
                return True
            else:
                return False
        elif type=="nr":
            for i in range(0,len(var)-1):
                if type(var[i])!="int":
                    return False
            return True
        else:
            return False
    def __del__(self):
        try:
            con.close()
        except:
            raise