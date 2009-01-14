import database
db=database.Database()

class Book():
    def create(self):
        db.query('insert into book values()')
        booknr=db.query('select max(nr) from book')
        return booknr[0][0]

    def create_type (self,isbn,author,title,fachbereich,mittelstufe):
        if (db.check ("isbn",isbn) and db.check("text",author) and db.check("text",title) and db.check("text",fachbereich)and db.check ("nr",mittelstufe)):
            if db.query('select isbn from type where isbn='+isbn+''):
                raise ValueError, "Isbn already exist"
            else:
                db.query ('insert into type values (Null,"'+isbn+'", "'+author+'", "'+title+'", "'+fachbereich+'", "'+mittelstufe+'")')
                return db.query('SELECT nr from type WHERE isbn="'+isbn+'"')[0][0]

    def edit(self,nr,isbn,author,title,fachbereich,mittelstufe):
        if(db.check ("isbn",isbn) and db.check("text",author) and db.check("text",title) and db.check("text",fachbereich)and db.check ("nr",mittelstufe)):
            if self.type_exist(nr):
                db.query('update type set isbn="'+isbn+'" ,author="'+author+'" ,title="'+title+'" ,fachbereich="'+fachbereich+'" ,mittelstufe="'+mittelstufe+'"where nr='+nr+'')
                return True
            else:
                raise ValueError,"Invalid Number"

    def type_exist(self,typenr):
        if db.check("nr",typenr):
            if db.query('select nr from type where nr='+typenr+''):
                return True
            else:
                raise ValueError,"Number doesn't exist"

    def exist(self,booknr):
        if db.check("nr",booknr):
            if db.query('select nr from book where nr='+booknr+''):
                return True
            else:
                raise ValueError,"Number doesn't exist"

    def book_type_connect(self,booknr,typenr):
        if db.check("nr",booknr) and db.check("nr",typenr):
            db.query('update book set type="'+typenr+'" where nr='+booknr+'')
            return True
        else:
            raise ValueError,"Invalid Booknumber"

    def delete(self,booknr):
        if db.check("nr",booknr):
            try:
                if db.query ('Select nr from book where nr="'+booknr+'"') ==(): raise ValueError,"Number doesn't exist"
                db.query ('delete from book where nr="'+booknr+'"')
                return True
            except: raise ValueError,"Error in Delete"

    def info(self,booknr):
        info_dict=db.query('SELECT t.isbn, t.author, t.title t.fachbereich t.mittelstufe FROM TYPE AS t, book AS b WHERE (b.nr = "'+str(booknr)+'" AND b.type = t.nr)')
        return (info_dict[0])

    def type_info(self,nr):
        if db.check("nr",nr):
            info_dict=db.query('Select isbn, author, title, fachbereich, mittelstufe from type where nr="'+str(nr)+'"')
            try: return (info_dict[0])
            except: raise ValueError,"Number not found"




if "__main__"==__name__:
     buch=Book()
     #print buch.create()
     #print buch.create_type("9783507107229" , "Schroedel" , "Physik" , "Mathe" ,"1")
     #print buch.edit("16", "3499612453" , "Schroedel" , "Physik12/13" , "Physik" ,"0" )
     #print buch.type_exist("16")
     #print buch.exist("99")
     #print buch.info("23")
     #print buch.delete("9")
     #print buch.type_info("1006")
     #for i in range (30):
     #print buch.book_type_connect(str(i+1),"3")
     #print buch.book_type_connect ("33","16")
