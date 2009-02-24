import html as html
import database as database
import kurzlang as kl
db=database.Database()

#def content():
#    x=book()
#    return x.returnFunc()
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
        info_dict=db.query('SELECT t.isbn, t.author, t.title, t.fachbereich, t.mittelstufe, b.druck, t.nr FROM TYPE AS t, book AS b WHERE (b.nr = "'+str(booknr)+'" AND b.type = t.nr)')
        return (info_dict[0])

    def type_info(self,nr):
        if db.check("nr",nr):
            info_dict=db.query('Select isbn, author, title, fachbereich, mittelstufe from type where nr="'+str(nr)+'"')
            try: return (info_dict[0])
            except: raise ValueError,"Number not found"

    def typenr_max(self):
        typenr=db.query('select max(nr) from type')
        return typenr[0][0]

    def booknr_max(self):
        booknr=db.query('select max(nr) from book')
        return booknr[0][0]
        
    def poobore(self,nr):
        if db.check ("nr",nr):
            infodict=db.query('select a.pnr, p.vor, p.nach from ausleihe as a, pupil as p where a.bnr= '+str(nr)+' and p.nr=a.pnr')
        else: infodict=[]
        return infodict
    
class book():
    def __init__(self):
        self.BookSql=Book()

    def books(self):
        self.table=html.table("ID",
                              "Titel",
                              "Druckstatus",
                              "Author",
                              "Fachbereich",
                              "Typnummer",
                              "Ausgeliehen an",
                              "Schuelernummer")
        self.Data=[]
        maxNr=self.BookSql.booknr_max()
        x=0
        for i in range(1,maxNr+1):
            try:
                self.bookData=self.BookSql.info(str(i))
                self.Data.append([kl.mach_lang(str(i)),
                                  self.bookData[2],
                                  self.bookData[5],
                                  self.bookData[1],
                                  self.bookData[3],
                                  kl.mach_lang(self.bookData[6])])
                x+=1
                
                try: 
                    self.bookData2=self.BookSql.poobore(str(i))[0]
                    self.Data[x-1].append(self.bookData2[1]+' '+self.bookData2[2])
                    self.Data[x-1].append(kl.sch2lang(self.bookData2[0]))
                except:
                    self.Data[x-1].append("")
                    self.Data[x-1].append("")
            except: pass
        #print self.Data
        #datei=file("D:/bla.txt",'w')
        #datei.write(str(self.Data))
        #datei.close()
        return self.Data

    def BookSearch(self,values):
        KeysUseEqualSign=('b.nr','b.druck', 't.nr')
        where=''
        for key in values.keys():
            if values[key]!='':
                if len(where)>0: where+=' and '
                if key in KeysUseEqualSign: where+=key+' = "'+values[key]+'"'
                else: where+=key+' like "%'+values[key]+'%"'
        if where!='':
            #print where
            BlaDict= db.query('select b.nr, t.title, b.druck, t.author, t.fachbereich, t.nr from book as b, type as t where b.type=t.nr and('+where+')')
            #print BlaDict
            rtnList=[]
            for i in range(len(BlaDict)):
                rtnList.append(list(BlaDict[i]))
                try: 
                    BlubList=self.BookSql.poobore(str(BlaDict[i][0]))
                    rtnList[i].append(self.BlubList[1]+' '+self.BlubList[2])
                    rtnList[i].append(self.BlubList[0])
                except:
                    rtnList[i].append("")
                    rtnList[i].append("")
            return rtnList
        return self.books()

    def returnFunc(self):
        return self.table.rtn()
         
if __name__=="__main__":
    x=book()
    print x.returnFunc()
    

    '''
            #self.bookData2=self.BookSql.poobore(str(i))
            #print self.Data
            for LineID in range(len(self.Data)):
                string="self.table.createLine("
                for i in range(len(self.Data[LineID])):
                    string+=str("'"+str(self.Data[LineID][i])+"',")
                string+=")"
                exec string
    '''

    '''
                             
        def books(self):
            self.table=html.table("ID",
                                  "Titel",
                                  "Druckstatus",
                                  "Author",
                                  "Fachbereich",
                                  "Typnummer",
                                  "Ausgeliehen an",
                                  "Schuelernummer")
            self.Data=[]
            maxNr=self.BookSql.booknr_max()
            x=0
            for i in range(1,maxNr+1):
                try:
                    self.bookData=self.BookSql.info(str(i))
                    self.Data.append([str(i),
                                      self.bookData[2],
                                      self.bookData[5],
                                      self.bookData[1],
                                      self.bookData[3],
                                      self.bookData[6]])
                    x+=1
                    try: 
                        self.bookData2=self.BookSql.poobore(str(i))[0]
                        self.Data[x-1].append(self.bookData2[1]+self.bookData2[2])
                        self.Data[x-1].append(self.bookData2[0])
                    except:
                        self.Data[x-1].append("")
                        self.Data[x-1].append("")
                except: pass
                self.bookData2=self.BookSql.poobore(str(i))
            #print self.Data
            for LineID in range(len(self.Data)):
                string="self.table.createLine("
                for i in range(len(self.Data[LineID])):
                    string+=str("'"+str(self.Data[LineID][i])+"',")
                string+=")"
                exec string
                    try: 
                        self.bookData2=self.BookSql.poobore(str(i))[0]
                        self.Data[x-1].append(self.bookData2[1]+self.bookData2[2])
                        self.Data[x-1].append(self.bookData2[0])
                    except:
                        self.Data[x-1].append("")
                        self.Data[x-1].append("")
                except: pass
                self.bookData2=self.BookSql.poobore(str(i))
            #print self.Data
            for LineID in range(len(self.Data)):
                string="self.table.createLine("
                for i in range(len(self.Data[LineID])):
                    string+=str("'"+str(self.Data[LineID][i])+"',")
                string+=")"
                exec string
            
        def __bookTypes(self):
            self.table=html.table("Book ID",
                                  "Titel", 
                                  "Anzahl Gesamt",
                                  "Anzahl Ausgeliehen",
                                  "ISBN",
                                  "Author",
                                  "Fachbereich",
                                  "Mittelstufe")
            self.Data=[]
            maxNr=self.BookSql.typenr_max()
            for i in range(1,maxNr+1):
                try:
                    self.typeData=self.BookSql.type_info(str(i))
                    self.Data.append([str(i),self.typeData[2],"","",self.typeData[0],self.typeData[1],self.typeData[3],self.typeData[4]])
                except: pass
            for LineID in range(len(self.Data)):
                string="self.table.createLine("
                for i in range(len(self.Data[LineID])):
                    string+=str("'"+str(self.Data[LineID][i])+"',")
                string+=")"
                exec string
    '''
