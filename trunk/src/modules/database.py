# -*- coding: utf-8 -*-
class Database():
    '''Klasse Database():
        .query(sqlcode) --> tupel
        .check(type,var) --> bool|raise ##type= | (isbn,text,date,nr)
        .backup() --> str(sqlcode)'''
    host='pc17'
    user='biblio'
    pw='test'
    db_name='biblio'
    def __init__(self):
        try:
            import MySQLdb as mysql
            self.con=mysql.connect(host=self.host, user=self.user, passwd=self.pw)
            self.cur=self.con.cursor()
            self.query("USE "+ self.db_name)
        except:
            raise
    def query(self, sqlcode):
        try:
            self.cur.execute(sqlcode)
            return self.cur.fetchall()
        except:
            raise
    def check(self, type, var):

        if type=="isbn":
            pruef=0
            if len(var)==13: ##ISBN 13
                for i in range(0, 12+1):
                    try:
                        v=int(var[i])
                        if i%2==1:
                            pruef+=3*v
                        else:
                            pruef+=v
                    except:
                        raise TypeError,"Invalid character in ISBN-13"
                if (pruef%10)==0:
                    return True
                else:
                    raise ValueError,"Invalid checknumber"
            if len(var)==10: ##ISBN 10
                for i in range(0, 9):
                    try:
                        pruef+=(i+1)*int(var[i])
                    except:
                        raise TypeError,"Invalid character in ISBN-10"
                if (pruef%11)!=10 and int(var[9])==(pruef%11): ##Pruefziffernkontrolle
                    return True
                elif (pruef%11)==10 and var[9].upper()=="X": ##Pruefziffernkontrolle
                    return True
                else:
                    raise ValueError,"Invalid checknumber"
            else:
                raise ValueError,"Invalid length of ISBN"

        elif type=="text":
            if var.find(";)")!=-1:
                raise ValueError,"Invalid characters in Text -- SQL-Injection vermutet!"
            else:
                return True

        elif type=="date":
            import time
            import datetime

            if len(var)==4 and int(var)>-3000 and int(var)<int(time.strftime("%Y")):
                return True
            elif len(var)==8:
                year=int(var[0:4])
                month=int(var[4:6])
                day=int(var[6:8])
                if datetime.date(year, month, day):
                    return True
            else:
                raise ValueError,"Invalid format of date"

        elif type=="nr":
            try:
                for i in range(0, len(var)):
                    int(var[i])
            except:
                if var=="1" or var=="0":
                    return True
                    pass
                else:
                    raise TypeError,"Invalid character in nr"
            return True
        else:
            raise TypeError,"You didn't define a valid type to check!"
    def backup(self):
        wr=""
        for table in self.query("SHOW TABLES"):
            wr+="DROP TABLE IF EXISTS `"+table[0]+"`;"
            wr+="CREATE TABLE IF NOT EXISTS `"+table[0]+"`("
            for field in self.query("DESCRIBE "+table[0]):
                wr+="`"+field[0]+"` "+field[1]+" "
                if field[2]=="NO":
                    wr+="NOT NULL "
                if field[5]!="":
                    wr+=field[5]+" PRIMARY KEY"
                wr+=","
            else:
                wr=wr[0:-2]+");\n"
            wr+="INSERT INTO `"+table[0]+"` ("
            for field in self.query("DESCRIBE "+table[0]):
                wr+="`"+field[0]+"`,"
            else:
                wr=wr[0:-1]+") VALUES\n"
                if self.query("SELECT * FROM "+table[0])==():
                    wr+="("
                    for field in self.query("DESCRIBE "+table[0]):
                        wr+="'',"
                    else:
                        wr=wr[:-1]+"),\n"
            for data in self.query("SELECT * FROM "+table[0]):
                wr+="("
                for wert in data:
                    if wert==None:
                        wr+="NULL,"
                        continue
                    wr+="'"+str(wert)+"',"
                else:
                    wr=wr[0:-1]+"),\n"
            else:
                wr=wr[0:-2]+";\n"
        return wr
    def __del__(self):
        try:
            self.con.close()
        except:
            raise

if __name__=="__main__": ##Debug-Funktion
#===============================================================================
    db=Database()
    print db.check("nr",1)
#===============================================================================
#===============================================================================
#    print self.check("isbn","350710606X") #valid 10
#    print self.check("isbn","9783429019976") #valid 13
#    print self.check("text", "Hallo!") #valid
#    print self.check("date", "1990") #valid
#    print self.check("date", "19900823") #valid
#    print self.check("nr", "123456") #valid
#    print "---"
#===============================================================================
#===============================================================================
#    print self.check("isbn","9999999998") #invalid 10
#    print self.check("isbn","9999999999999") #invalid 13
#    print self.check("isbn","333") #invalid length
#    print self.check("text", "el';)delete * from books") #invalid
#   print self.check("date", "3500") #invalid
#    print self.check("date", "19900231") #invalid
#    print self.check("nr", "abc") #invalid
#    print self.check("else", "murks") #invalid type
#    print "---"
#===============================================================================
#   print "---"
#    print self.query("SELECT * from book")
#   print "---"
#    print "Test erfolgreich absolviert."
#    print help(Database)
