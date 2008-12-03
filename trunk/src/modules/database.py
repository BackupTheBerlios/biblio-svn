# -*- coding: utf-8 -*-
class Database():
    host='pc17'
    user='biblio'
    pw='test'
    db_name='biblio'
    def __init__(self):
        try:
            import MySQLdb as mysql
            self.__con=mysql.connect(host=self.host, user=self.user, passwd=self.pw)
            self.__cur=self.__con.cursor()
            self.query("USE "+ self.db_name)
        except:
            raise
    def query(self, sqlcode):
        try:
            self.__cur.execute(sqlcode)
            return self.__cur.fetchall()
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
                    raise Warning,"Invalid checknumber"
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
        wr="""DROP TABLE IF EXISTS `ausleihe`;
CREATE TABLE IF NOT EXISTS `ausleihe` (
  `pnr` int(11) NOT NULL,
  `bnr` int(11) NOT NULL,
  KEY `pnr` (`pnr`,`bnr`));
DROP TABLE IF EXISTS `book`;
CREATE TABLE IF NOT EXISTS `book` (
  `nr` int(11) NOT NULL auto_increment,
  `type` int(11) NOT NULL default '0',
  `druck` tinyint(1) NOT NULL default '0',
  UNIQUE KEY `nr` (`nr`));
DROP TABLE IF EXISTS `pupil`;
CREATE TABLE IF NOT EXISTS `pupil` (
  `nr` int(11) NOT NULL auto_increment,
  `vor` text collate utf8_unicode_ci,
  `nach` text collate utf8_unicode_ci,
  `geb` date default NULL,
  PRIMARY KEY  (`nr`));
DROP TABLE IF EXISTS `type`;
CREATE TABLE IF NOT EXISTS `type` (
  `nr` int(11) NOT NULL auto_increment,
  `isbn` text collate utf8_unicode_ci,
  `author` text collate utf8_unicode_ci,
  `title` text collate utf8_unicode_ci,
  PRIMARY KEY  (`nr`));\n"""

        wr+="INSERT INTO `ausleihe` ( `pnr` , `bnr` ) VALUES\n"
        for data in self.query("SELECT * FROM ausleihe"):
            wr+="('"+str(data[0])+"','"+str(data[1])+"'),\n"
        wr=wr[0:-2]+";\n"
        wr+="INSERT INTO `book` ( `nr` , `type` , `druck` ) VALUES\n"
        for data2 in self.query("SELECT * FROM book"):
            wr+="('"+str(data2[0])+"','"+str(data2[1])+"', '"+str(data2[2])+"'),\n"
        wr=wr[0:-2]+";\n"
        wr+="INSERT INTO `pupil` ( `nr` , `vor` , `nach` , `geb` ) VALUES\n"
        for data3 in self.query("SELECT * FROM pupil"):
            wr+="('"+str(data3[0])+"','"+str(data3[1])+"','"+str(data3[2])+"','"+str(data3[3])+"'),\n"
        wr=wr[0:-2]+";\n"
        wr+="INSERT INTO `type` ( `nr` , `isbn` , `author` , `title` ) VALUES\n"
        for data4 in self.query("SELECT * FROM type"):
            wr+="('"+str(data4[0])+"','"+str(data4[1])+"','"+str(data4[2])+"','"+str(data4[3])+"'),\n"
        wr=wr[0:-2]+";\n"
        return wr
    def __del__(self):
        try:
            self.__con.close()
        except:
            raise

if __name__=="__main__": ##Debug-Funktion
    db=Database()
    print db.check("isbn","350710606X") #valid 10
    print db.check("isbn","9783429019976") #valid 13
    print db.check("text", "Hallo!") #valid
    print db.check("date", "1990") #valid
    print db.check("date", "19900823") #valid
    print db.check("nr", "123456") #valid
    print "---"
#===============================================================================
#    print db.check("isbn","9999999998") #invalid 10
#    print db.check("isbn","9999999999999") #invalid 13
#    print db.check("isbn","333") #invalid length
#    print db.check("text", "el';)delete * from books") #invalid
#   print db.check("date", "3500") #invalid
#    print db.check("date", "19900231") #invalid
#    print db.check("nr", "abc") #invalid
#    print db.check("else", "murks") #invalid type
#    print "---"
#===============================================================================
#    print db.backup()
#   print "---"
#    print db.query("SELECT * from book")
#   print "---"
    print "Test erfolgreich absolviert."
