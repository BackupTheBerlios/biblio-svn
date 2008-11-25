# -*- coding: utf-8 -*-
import MySQLdb as mysql
class Database():
    host='pc17'
    user='biblio'
    pw='test'
    db_name='biblio'
    def __init__(self):
        try:
            self.con=mysql.connect(host=self.host, user=self.user, passwd=self.pw)
            self.cur=self.con.cursor()
            self.query("USE "+ self.db_name)
        except:
            raise
    def query(self, sqlcode):
        try:
            self.cur.execute(sqlcode)
            return self.cur.fetchall()
        except IndexError:
            return
        except:
            raise
    def check(self, type, var):

        if type=="isbn":
            pruef=0
            if len(var)==13: ##ISBN 13
                for i in range(0, 11+1):
                    print var[i]
                    try:
                        v=int(var[i])
                        if i%2==1:
                            pruef+=3*v
                        else:
                            pruef+=v
                    except:
                        raise TypeError,"Invalid character in ISBN-13"
                print pruef%10
                if (pruef%10)==int(var[12]):
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
            if var.find(";)")==-1:
                raise ValueError,"Invalid characters in Text -- SQL-Injection vermutet!"
            else:
                return True

        elif type=="date":
            import time
            import datetime

            if len(var)==4 and int(var)>-3000 and int(var)<int(time.strftime("%Y")):
                return True
            if len(var)==8:
                year=int(var[0:4])
                month=int(var[4:6])
                day=int(var[6:8])
                if datetime.date(year, month, day):
                    return True
            else:
                raise ValueError,"Invalid format of date"

        elif type=="nr":
            for i in range(0, len(var)):
                try:
                    int(var[i])
                except:
                    raise TypeError,"Invalid character in nr"
            return True
        else:
            raise TypeError,"You didn't define a valid type to check!"
    def backup(self):
        wr=""
        wr+="""
        CREATE TABLE 'ausleihe' (
        'pnr' int(11) NOT NULL,
        'bnr' int(11) NOT NULL,
        KEY 'pnr' ('pnr','bnr')
        )
        CREATE TABLE 'book' (
        'nr' int(11) NOT NULL auto_increment,
        'type' int(11) NOT NULL,
        UNIQUE KEY 'nr' ('nr')
        )
        CREATE TABLE 'pupil' (
        'nr' int(11) NOT NULL auto_increment,
        'vor' text collate utf8_unicode_ci,
        'nach' text collate utf8_unicode_ci,
        'geb' date default NULL,
        PRIMARY KEY  ('nr')
        )
        CREATE TABLE 'type' (
        'nr' int(11) NOT NULL auto_increment,
        'isbn' bigint(13) default NULL,
        'author' text collate utf8_unicode_ci,
        'title' text collate utf8_unicode_ci,
        'meta' text collate utf8_unicode_ci,
        PRIMARY KEY  ('nr')
        )\n\n"""
        for data in self.query("SELECT * FROM ausleihe"):
            wr+="INSERT INTO 'ausleihe' VALUES ('"+str(data[0])+"','"+str(data[1])+"')\n"
        for data2 in self.query("SELECT * FROM book"):
            wr+="INSERT INTO 'book' VALUES ('"+str(data2[0])+"','"+str(data2[1])+"')\n"
        for data3 in self.query("SELECT * FROM pupil"):
            wr+="INSERT INTO 'pupil' VALUES ('"+str(data3[0])+"','"+str(data3[1])+"','"+str(data3[2])+"','"+str(data3[3])+"')\n"
        for data4 in self.query("SELECT * FROM type"):
            wr+="INSERT INTO 'type' VALUES ('"+str(data4[0])+"','"+str(data4[1])+"','"+str(data4[2])+"','"+str(data4[3])+"','"+str(data4[4])+"')\n"
        return wr
    def __del__(self):
        try:
            self.con.close()
        except:
            raise

if __name__=="__main__": ##Debug-Funktion
    db=Database()
#===============================================================================
#    print db.check("isbn","350710606X") #valid 10
    print db.check("isbn","9783507106062") #valid 13
#    print db.check("text", "Hallo!") #valid
#    print db.check("date", "1990") #valid
#    print db.check("date", "19900823") #valid
#    print db.check("nr", "123456") #valid
#    print "---"
#===============================================================================
    #print db.check("isbn","9999999998") #invalid 10
    #print db.check("isbn","9999999999999") #invalid 13
    #print db.check("isbn","333") #invalid length
    #print db.check("text", "el';)delete * from books") #invalid
    #print db.check("date", "3500") #invalid
    #print db.check("date", "19900231") #invalid
    #print db.check("nr", "abc") #invalid
    #print db.check("else", "murks") #invalid type
#===============================================================================
#    print "---"
#    print db.backup()
#    print "---"
#    print db.query("SELECT * from book")
#===============================================================================
    print "---"
    print "Test erfolgreich absolviert."