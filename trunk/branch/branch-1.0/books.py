# -*- coding: cp1252 -*-

import start as ini
import modules.book as book
import modules.html as html
import cgi


def bar():
        mylink = html.link(Datei='books.py',Text='Umschalt')
        mylink.add_param(Name='state',Wert=str(main.nextState()))
        return mylink.rtn()

def content():
        return main.rtn()

class Main():        
        def nextState(self):
                try: self.state=int(query.getvalue('state'))
                except: self.state=0
                if self.state==0: return 1
                else: return 0
        
        def rtntype(self):
                suchformular=html.form(Titel='Suche',Datei='start.py')
                suchformular.open_paragraph()
                suchformular.add_Hidden(ElementName='mn',Wert='books')
                SuchListe=["ID",
                           "Titel",
                           "Autor",
                           "Fachbereich"]
                for Element in SuchListe:
                    suchformular.add_Entry(ElementName=Element,Beschriftung=Element)
                suchformular.add_Button(Beschriftung='Suche starten!')
                suchformular.end_paragraph()
                self.cnt+=suchformular.rtn()
                seek=dict()
                Typnum=str(query.getvalue('Typnummer')).replace('None','')
                try: Typnum=kl.mach_kurz(int(Typnum))
                except: pass
                seek['t.nr']=Typnum
                seek['t.title']=str(query.getvalue('Titel')).replace('None','')
                seek['t.author']=str(query.getvalue('Autor')).replace('None','')
                seek['t.fachbereich']=str(query.getvalue('Fachbereich')).replace('None','')
                
                return self.cnt
                

        def rtnbook(self):
                suchformular=html.form(Titel='Suche',Datei='start.py')
                suchformular.open_paragraph()
                suchformular.add_Hidden(ElementName='mn',Wert='books')
                SuchListe=["ID",
                           "Titel",
                           "Druckstatus",
                           "Autor",
                           "Fachbereich",
                           "Typnummer"]
                for Element in SuchListe:
                    suchformular.add_Entry(ElementName=Element,Beschriftung=Element)
                suchformular.add_Button(Beschriftung='Suche starten!')
                suchformular.end_paragraph()
                self.cnt+=suchformular.rtn()
                seek=dict()
                seek['b.nr']=str(query.getvalue('ID')).replace('None','')
                seek['t.title']=str(query.getvalue('Titel')).replace('None','')
                seek['b.druck']=str(query.getvalue('Druckstatus')).replace('None','')
                seek['t.author']=str(query.getvalue('Autor')).replace('None','')
                seek['t.fachbereich']=str(query.getvalue('Fachbereich')).replace('None','')
                Typnum=str(query.getvalue('Typnummer')).replace('None','')
                try: Typnum=kl.mach_kurz(int(Typnum))
                except: pass
                seek['t.nr']=Typnum
                self.cnt+=Suche.Search(seek)
                return self.cnt

        def rtn(self):
                self.cnt=''
                #query=cgi.FieldStorage()
                try: self.state=int(query.getvalue('state'))
                except: self.state=0
                if self.state==1: return self.rtntype()
                else: return self.rtnbook()
    
class SearchFunctions():
        def __init__(self):
                self.Book=book.book()
                self.Columns=("ID",
                           "Titel",
                           "Druckstatus",
                           "Autor",
                           "Fachbereich",
                           "Typnummer",
                           "Schueler",
                           "Schuelernr.",
                           "Optionen")
                self.TypeColumns=("ID",
                           "Titel",
                           "Autor",
                           "Fachbereich",
                           "Optionen")
        def Search(self,kw):
                Table=self.__CreateTable(self.Book.BookSearch(kw))
                return Table
        def SearchType(self,kw):
                Table=''
                return Table
                
        def __CreateTable(self,liste):
                exec "Table=html.table"+str(self.Columns)
                try:
                        for item in liste:
                                item=list(item)+[None]
                                exec "Table.createLine"+str(tuple(item))
                except: pass
                return Table.rtn()

Suche=SearchFunctions()
main=Main()
query=cgi.FieldStorage()
