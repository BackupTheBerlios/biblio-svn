import MySQLdb as mysql

class Book():
    def create(self):
        return booknr
    def edit(self,nr,isbn,meta):
        return
    def exist(self,booknr):
        return
    def delete(self,booknr):
        return
    def info(self,booknr):
        ##info_dict=nr,isbn,meta
        return (info_dict)
class Pupil():
    def create(self):
        return pupilnr
    def edit(self,nr,vorname,nachname,geburtsdatum):
        return
    def exist(self,pupilnr):
        return
    def delete(self,pupilnr):
        ##nur, wenn nichts mehr ausgeliehen!!
        return
    def info(self,pupilnr):
        ##info_dict=nr,vor,nach,geb
        return (info_dict)
class Ausleihe():
    def borrow(self,pupilnr,booknr):
        return
    def book_loaned(self,booknr):
        return (pupilnr)
    def pupil_got(self,pupilnr):
        return (booknrs)
    def handback(self,booknr):
        return