# -*- coding: utf-8 -*-
import MySQLdb as mysql
class Database():
    host='pc17'
    user='biblio'
    pw='test'
    db_name='biblio'
    def __init__(self):
        try:
            self.con=mysql.connect(host=self.host,user=self.user,passwd=self.pw)
            self.cur=self.con.cursor()
        except:
            raise
    def query(self,sqlcode):
        try:
            self.cur.execute(sqlcode)
            return self.cur.fetchall()
        except IndexError:
            return
        except:
            raise
    def check(self,type,var):
        ##TODO:ISBN-Prüfnummer
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
        ##TODO:Text auf ungültige Zeichen prüfen
        elif type=="text":
            return
        ##TODO:Test: check(date)
        elif type=="date":
            from time import strftime
            if len(var)==4 and var>-3000 and var<int(strftime("%Y")):
                return True
            else:
                return False
        ##TODO:Nummer
        elif type=="nr":
            for i in range(0,len(var)-1):
                if type(var[i])!="int":
                    return False
            return True
        else:
            return False
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
        self.query("USE "+self.db_name)
        dat=self.query("SELECT * FROM ausleihe")
        for data in dat:
            wr+="INSERT INTO 'ausleihe' VALUES ('"+str(data[0])+"','"+str(data[1])+"')\n"
        dat2=self.query("SELECT * FROM book")
        for data2 in dat2:
            wr+="INSERT INTO 'book' VALUES ('"+str(data2[0])+"','"+str(data2[1])+"')\n"
        dat3=self.query("SELECT * FROM pupil")
        for data3 in dat3:
            wr+="INSERT INTO 'pupil' VALUES ('"+str(data3[0])+"','"+str(data3[1])+"','"+str(data3[2])+"','"+str(data3[3])+"')\n"
        dat4=self.query("SELECT * FROM type")
        for data4 in dat4:
            wr+="INSERT INTO 'type' VALUES ('"+str(data4[0])+"','"+str(data4[1])+"','"+str(data4[2])+"','"+str(data4[3])+"','"+str(data4[4])+"')\n"
        return wr
    def __del__(self):
        try:
            self.con.close()
        except:
            raise

if __name__=="__main__":
    db=Database()
    print db.backup()