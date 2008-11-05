import database
db=database.Database()
class Book():
    def create(self):
        db.query('insert into book')
        booknr=db.query('select MAX (nr)')
        return booknr
    
    def create_type (self,isbn,author,title):
        if (db.check ("isbn",isbn) and db.check("text",author) and db.check("text",title)):
            suc=False
        else:
            db.query ('insert into type')
            
    def edit(self,nr,isbn,author,title):
        if(db.check("nr",nr) and db.check("isbn",isbn) and db.check("text",author) and db.check("text",title)):
            if db.query('select nr from book where nr='+nr+''):
                if db.query('update book (nr='+nr+',isbn='+isbn+',author='+author+',title='+title+')'):
                    suc=True
            else:
                    suc=False
        return suc
    
    def exist(self,booknr):
        if db.check("nr",booknr):
            if db.query('select nr from book where nr='+nr+''):
                suc=True
            else:
                    suc=False
        return suc
    
    def delete(self,booknr):
     if db.check("nr",booknr):
            if db.query ('select nr from book where nr='+nr+''):
                db.query ('delete booknr (nr)')
                suc=True
            else:
                    suc=False
        return
    
    def info(self,booknr):
        info_dict={'select booknr, nr, isbn, author, title from type as t, from book as b where t.booknr=b.booknr' }
        if db.query('select nr from book where nr='+nr''):
            suc=True
            
        else:
            suc=False
            
        
    
        return (info_dict)
    
class Pupil():
    def create(self):
        db.query('insert into pupil')
        booknr=db.query('select MAX (nr)')
        return pupilnr
    
    def edit(self,nr,vorname,nachname,geburtsdatum):
        if(db.check("nr",nr) and db.check("text",vorname) and db.check("text",nachname) and db.check("text",geburtsdatum)):
            if db.query('select nr from book where nr='+nr+''):
                if db.query('update pupil (nr='+nr+',vorname='+vorname+',nachname='+nachname+',gebursdatum='+gebursdatum+')'):
                    suc=True
            else:
                    suc=False
        return suc

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