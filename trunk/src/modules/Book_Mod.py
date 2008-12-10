import database
db=database.Database()

class Book():
    def create(self):
        db.query('insert into book values()')
        booknr=db.query('select max(nr) from book')
        return booknr[0][0]

    def create_type (self,isbn,author,title):
        if not(db.check ("isbn",isbn) and db.check("text",author) and db.check("text",title)):
            return False
        else:
            if db.query('select isbn from type where isbn='+isbn+''):
                return False
            else:
                db.query ('insert into type values (Null,"'+isbn+'", "'+author+'", "'+title+'")')
                return db.query('SELECT nr from type WHERE (nr = "'+str(booknr)+'" AND b.type = t.nr)')

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
    
    def book_type_connect(self,booknr,typenr):
        if db.check("nr",booknr) and db.check("nr",typenr):
            #liste=db.query('select nr from book where nr='+booknr+''), db.query('select nr from type where nr='+typenr+'')
            db.query('update book set type="'+typenr+'" where nr='+booknr+'')
            return True
        else:
            return False
    
    def delete(self,booknr):
        if db.check("nr",booknr):
            try:
                if db.query ('Select nr from book where nr="'+booknr+'"') ==(): return False
                db.query ('delete from book where nr="'+booknr+'"')
                return True
            except: return False
        else: return False

    def info(self,booknr):
        info_dict=db.query('SELECT t.isbn, t.author, t.title FROM TYPE AS t, book AS b WHERE (b.nr = "'+str(booknr)+'" AND b.type = t.nr)')
        #if db.query('select nr from book where nr='+nr+'')==True:
        #    suc=True

        #else:

        return (info_dict[0])
    
    def type_info(self,nr):
        if db.check("nr",nr):
            info_dict=db.query('Select isbn, author, title from type where nr="'+str(nr)+'"')
            
            try: return (info_dict[0])
            except: return False
            
        


if "__main__"==__name__:
     buch=Book()
     #print buch.create()                                                     #True
     #print buch.create_type("9783596271207" , "DUUUL" , "Allgemeine Chemie" )#True
     #print buch.exist("30")                                                  #True
     #print buch.edit("3", "3499612453" , "DL" , "Allgemeine Chemie")         #True
     #print buch.info("23")                                                   #True
     #print buch.delete("9")                                                  #True
     #print buch.type_info("3")                                               #True
     #print buch.book_type_connect("7","3")                                   #True

