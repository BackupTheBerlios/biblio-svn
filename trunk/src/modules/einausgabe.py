import database
db=database.Database("")
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
            suc=True
        return suc
    
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
         return suc

    def info(self,booknr):
        info_dict=db.query('select booknr, nr, isbn, author, title from type as t, from book as b where t.booknr=b.booknr')
        if db.query('select nr from book where nr='+str(nr))==True:
            suc=True

        else:
            suc=False

        return (info_dict)
        
class Pupil():
    def create(self):
        db.query('insert into pupil')
        pupilnr=db.query('select MAX (nr)')
        return pupilnr

    def edit(self,nr,vorname,nachname,geburtsdatum):
        if(db.check("nr",nr) and db.check("text",vorname) and db.check("text",nachname) and db.check("text",geburtsdatum)):
            if db.query('select nr from pupil where nr='+nr+''):
                if db.query('update pupil (nr='+nr+',vorname='+vorname+',nachname='+nachname+',gebursdatum='+gebursdatum+')'):
                    suc=True
            else:
                    suc=False
        return suc

    def exist(self,pupilnr):
        if db.check("nr",pupilnr):
            if db.query('select nr from pupil where nr='+nr+''):
                suc=True
            else:
                    suc=False
        return suc

    def delete(self,pupilnr):
        if db.check("nr",pupilnr):
            if db.query ('select nr from ausleihe where nr='+nr+''):
                suc=False
            else:
              db.query ('delete pupilnr (nr)')
              suc=True
             
            return suc

        
    def info(self,pupilnr):
        info_dict=db.query('select * from pupil where nr='+nr+'')
        if db.query('select nr from pupil where nr='+str(nr))==True:
            suc=True

        else:
            suc=False

        return (info_dict)
class Ausleihe():
    def borrow(self,pupilnr,booknr):
        if db.query('select nr from book where bnr='+booknr+'and select nr form pupil where pnr='+pupilnr+' and insert into ausleihe'):
            suc=True
        else:
            suc=False   
        return suc
    
    def book_loaned(self,booknr): 
        if db.query ('select pupilnr form ausleihe where bnr='+booknr+''):
            suc=pupilnr
        else:
            suc=False
            
        return suc
    
    def pupil_got(self,pupilnr):
        if db.query ('select all booknr from ausleihe where pnr='+pupilnr+''):
            suc=booknr
        else:
            suc=False
        return suc
    

    def handback(self,booknr):    
        if db.query('select booknr from ausleihe where bnr='+booknr+'and select pupilnr from ausleihe where pnr='+booknr+''):
            db.query('delete booknr and pupilnr where bnr='+booknr+'')
            suc=True
        else:
            suc=False
        return suc

#if "__main__"==__name__:
 #   klasse=Book()
  #  klasse.info(3)