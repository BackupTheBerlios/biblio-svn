import database
db=database.Database()

class Ausleihe():
    def borrow(self,pupilnr,booknr):
        if db.check("nr",pupilnr) and db.check("nr", booknr) and pupilnr!="" and booknr!="":
            if db.query("select nr from book where nr="+booknr+";")==():
                raise ValueError,"Buch existiert nicht!"
            if db.query("select nr from pupil where nr="+pupilnr+";")==():
                raise ValueError,"Schueler existiert nicht!"
            if db.query("select * from ausleihe where bnr="+booknr+";")!=():
                raise ValueError, "Buch bereits an anderen Schueler ausgeliehen!"
            if db.query("select * from ausleihe where pnr="+pupilnr+" and bnr="+booknr+";")!=():
                raise ValueError,"Kombination bereits ausgeliehen!"
            db.query('insert into ausleihe values((select pupil.nr from pupil where pupil.nr='+pupilnr+'),(select book.nr from book where book.nr='+booknr+'))')
            return True
        else:
            raise ValueError,"Nummer(n) wurde(n) nicht uebergeben!"

    def book_loaned(self,booknr):
        if db.check("nr",booknr) and booknr!="":
            if db.query('select nr from book where nr='+booknr+';')!=():
                for p in db.query('select pnr from ausleihe where bnr='+booknr+';'):
                    return p[0]
                return False
            else:
                raise ValueError,"Buch existiert nicht!"
        else:
            raise ValueError,"Buchnummer wurde nicht uebergeben!"

    def pupil_got(self,pupilnr):
        if db.check("nr",pupilnr) and pupilnr!="":
            if db.query('select nr from pupil where nr='+pupilnr+';'):
                blist=[]
                for b in db.query ('select bnr from ausleihe where pnr='+pupilnr+';'):
                    blist.append(b[0])
                if blist!=[]:
                    return tuple(blist)
                else:
                    return False
            else:
                raise ValueError,"Schueler existiert nicht!"
        else:
            raise ValueError,"Schuelernummer wurde nicht uebergeben!"

    def handback(self,booknr):
        if db.check("nr",booknr) and booknr!="":
            if db.query('select nr from book where nr='+booknr+';')!=():
                if db.query('select bnr from ausleihe where bnr='+booknr+';')!=():
                    db.query('delete from ausleihe where bnr='+booknr+';')
                    return True
                else:
                    raise ValueError,"Buch ist nicht ausgeliehn!"
            else:
                raise ValueError,"Buch existiert nicht!"
        else:
            raise ValueError,"Buchnummer wurde nicht uebergeben!"

if "__main__"==__name__:
    a=Ausleihe()
    print a.borrow("", "")
    print a.book_loaned("5")
    print a.pupil_got("1")
    print a.handback("20")