import database
db=database.Database()

class Book():
    def create(self):
        db.query('insert into book values()')
        booknr=db.query('select max(nr) from book')
        return booknr[0][0]

    def create_type (self,isbn,author,title):
        if not(db.check ("isbn",isbn) and db.check("text",author) and db.check("text",title)):
            suc=False
        else:
            if db.query('select isbn from type where isbn='+isbn+''):
                suc=False
            else:
                db.query ('insert into type values (Null,"'+isbn+'", "'+author+'", "'+title+'")')
                suc=True
        return suc

    def edit(self,nr,isbn,author,title):
        if(db.check("nr",nr) and db.check("isbn",isbn) and db.check("text",author) and db.check("text",title)):
            try:
                db.query('update type set isbn="'+isbn+'" ,author="'+author+'" ,title="'+title+'" where nr='+nr+'')
                suc=True
            except:
                suc=False
        return suc

    def exist(self,booknr):
        if db.check("nr",booknr):
            if db.query('select nr from book where nr='+booknr+''):
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

    def info(self,nr):
        info_dict=db.query('select t.isbn, t.author, t.title from type as t, from book as b where b.nr="'+str(nr)+'") and b.type=t.nr')
        #if db.query('select nr from book where nr='+nr+'')#==True:
        #    suc=True

        #else:

        return (info_dict)
class Pupil():
    def create(self):
        db.query('insert into pupil values()')
        pupilnr=db.query('select max(nr) from pupil')
        return pupilnr [0][0]

    def edit(self,nr,vorname,nachname,geburtsdatum):
        if(db.check("nr",nr) and db.check("text",vorname) and db.check("text",nachname) and db.check("text",geburtsdatum)):
            if db.query('select nr from pupil where nr='+nr+''):
                try:
                    db.query('update pupil SET vor="'+vorname+'",nach="'+nachname+'",geb="'+geburtsdatum+'" where nr='+nr+'')
                    suc=True
                except:
                    suc=False
        return suc

    def exist(self,pupilnr):
        if db.check("nr",pupilnr):
            if db.query('select nr from pupil where nr='+pupilnr+''):
                suc=True
            else:
                    suc=False
        return suc

    def delete(self,pupilnr):
        if db.check("nr",pupilnr):
            if db.query ('select pnr from ausleihe where pnr='+pupilnr+''):
                suc=False
            else:
              db.query ('delete from pupil where nr='+pupilnr+'')
              suc=True

            return suc


    def info(self,pupilnr):
        info_dict=db.query('select * from pupil where nr='+pupilnr+'')
        if db.query('select nr from pupil where nr='+str(pupilnr))==True:
            suc=True

        else:
            suc=False

        return (info_dict)
class Ausleihe():
    def borrow(self,pupilnr,booknr):
        if db.check("nr",pupilnr) and db.check("nr", booknr) and pupilnr!="" and booknr!="":
            if db.query("select nr from book where nr="+booknr+";")==():
                raise ValueError,"Buch existiert nicht!"
            if db.query("select nr from pupil where nr="+pupilnr+";")==():
                raise ValueError,"Schueler existiert nicht!"
            if db.query("select * from ausleihe where pnr="+pupilnr+" and bnr="+booknr+";")!=():
                raise ValueError,"Kombination bereits ausgeliehn!"
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

def mach_lang(nr_kurz):
    if int(nr_kurz)<10**9:
        return str(10**9+int(nr_kurz))
    else:
        raise ValueError,"Ungueltige Nummer!"
def mach_kurz(nr_lang):
    if int(nr_lang)>10**9:
        return str(int(nr_lang)-(10**9))
    else:
        raise ValueError,"Ungueltige Nummer!"

if "__main__"==__name__:
     buch=Book()
#    print buch.create()
#    print buch.create_type("3499612453" , "DUUUL" , "Allgemeine Chemie" )
#    print buch.exist("10")
#    print buch.edit("12", "3499612453" , "DL" , "Allgemeine Chemie")
     print buch.info("12")
#    schueler=Pupil()
#    print schueler.create()
#    print schueler.edit("7","Micky","Mouse","1990-5-22")
     print schueler.info(7)#===============================================================================
#    a=Ausleihe()
#    print a.borrow("", "")
#    print a.book_loaned("5")
#    print a.pupil_got("1")
#    print a.handback("20")
#===============================================================================

#===============================================================================
#    print mach_kurz("1000013765")
#    print mach_lang("1434")
#===============================================================================>>>>>>> .r81
