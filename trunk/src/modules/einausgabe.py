import database
db=database.Database()
class Book():
    def create(self):
        db.query('insert into book')
        booknr=db.query('select MAX (nr)')
        return booknr
    def edit(self,nr,isbn,author,title):
        if :
            db.query('update book (nr,isbn,author,title)')
        return
    def exist(self,booknr):
        db.query()
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