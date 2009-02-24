#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

import start as ini
from modules.schueler import Pupil
import modules.html as html
import cgi
import cgitb
cgitb.enable()

def content():
        cnt=''
        if query.has_key('Mode'):
                if query.getvalue('Mode')=='delete':
                        return Suche.Question('Wollen Sie den Schueler wirklich loeschen?')
                elif query.getvalue('Mode')=='delete_ok':
                        try: Suche.Delete(query.getvalue('LLesernummer'))
                        except ValueError,e: return Suche.Error(e.message)
                elif query.getvalue('Mode')=='edit':
                        return Suche.Edit(query.getvalue('LLesernummer'))
                elif query.getvalue('Mode')=='edit_now':
                        pass
                        
                else: pass
        #cnt+=Suche.MainBar()
        seek=dict()
        seek['nr']=str(query.getvalue('Lesernummer')).replace('None','')
        seek['vor']=str(query.getvalue('Vorname')).replace('None','')
        seek['nach']=str(query.getvalue('Nachname')).replace('None','')
        seek['jahrgang']=str(query.getvalue('Jahrgang')).replace('None','')
        cnt+=Suche.Search(seek)
        return cnt

def bar():
        suchformular=html.form(Titel='Suche',Datei='start.py')
        suchformular.add_Hidden(ElementName='mn',Wert='pupil')
        suchformular.open_paragraph()
        suchformular.add_Entry(ElementName='Lesernummer',Beschriftung='Lesernummer')
        suchformular.add_Entry(ElementName='Vorname',Beschriftung='Vorname')
        suchformular.add_Entry(ElementName='Nachname',Beschriftung='Nachname')
        suchformular.add_Entry(ElementName='Jahrgang',Beschriftung='Jahrgang')
        suchformular.add_Button(Beschriftung='Suche starten!')
        suchformular.end_paragraph()
        bar=suchformular.rtn()
        return bar

class PupilSearchFunctions():
        def __init__(self):
                self.Pupil=Pupil()
                self.Columns=('Lesernummer','Vorname','Nachname','Geburtstag','Jahrgang','Optionen')
        def Search(self,kw):
                liste=self.Pupil.Search(kw)
                LNR='['
                for x in liste:
                        if len(LNR)>1: LNR+=','
                        LNR +=str(x[0])
                LNR+=']'
                link = html.link(Text='Alle Treffer bearbeiten ...', Datei='pupil.py')
                link.add_param(Name = 'Mode', Wert = 'edit')
                link.add_param(Name = 'LLesernummer', Wert = LNR)
                shortcut=html.paragraph(link.rtn()).rtn()
                Table=self.__CreateTable(liste)
                return shortcut+Table+shortcut
        
        def __CreateTable(self,liste):
                exec "Table=html.table"+str(self.Columns)
                try:
                        for item in liste:
                                myLinks=[html.link(Datei='pupil.py',Text='Bearbeiten'),html.link(Datei='pupil.py',Text='Loeschen')]
                                myLinks[0].add_param(Name='LLesernummer',Wert='['+str(item[0])+']')
                                myLinks[0].add_param(Name='Mode',Wert='edit')
                                myLinks[1].add_param(Name='LLesernummer',Wert=str(item[0]))
                                myLinks[1].add_param(Name='Mode',Wert='delete')
                                item=list(item)+[myLinks[0].rtn()+' '+myLinks[1].rtn()]
                                exec "Table.createLine"+str(tuple(item))
                except: pass
                return Table.rtn()
        
        def Delete(self,Nummer):
                self.Pupil.delete(Nummer)
                
        def Error(self,Error):
                message=html.message(Error,'Ok',"./start.py?mn=pupil",0)
                return message.rtn()
        
        def Question(self,Question):
                message=html.message(Question,'Ja',"./start.py?mn=pupil&Mode=delete_ok&LLesernummer="+query.getvalue('LLesernummer'),
                                     3,ButtonText2='Nein',ButtonLink2="./start.py?mn=pupil")
                return message.rtn()
        
        def Edit(self,Rows):
                exec "Table=html.table"+str(self.Columns[0:-1])
                exec "Rows="+Rows
                for i in range(len(Rows)):
                        seek=dict()
                        seek["nr"]=str(Rows[i])
                        liste=self.Pupil.Search(seek)[0]
                        columns=[liste[0]]
                        for j in range(len(self.Columns)-2):
                                #columns.append('<form> <textarea name="E'+self.Columns[j]+'" cols=1>'+Rows[i][j]+'</textarea> <P> <input TYPE=SUBMIT> </form>')
                                #columns.append('<input type="text" name="E'+str(self.Columns[i+1])+str(Rows[i][0])+'">')
                                #columns.append(str(liste[j+1])+'<BR>'+'<input type="text",name="E'+str(self.Columns[j+1])+str(liste[0])+'",width=5,bg=green>') #Wo is'n dein Wert den Du übergeben willst? bg gibt's nicht, width nicht in dieser Form, html-Modul!, Befehle werden in XHTML klein geschrieben! Dein <br> muss geschlossen werden <br />, nimm aber lieber das p-Tag; KEINE KOMMATAR!
                                columns.append(str(liste[j+1])+'<input type="text" name="E'+str(self.Columns[j+1])+str(liste[0])+'" value="">') #Bei Value den Wert einsetzen!!
                                #So läuft das schon eher, aber Junge wieso machen wir das nicht einheitlich???
                        #exec 'Table.createLine'+str(tuple(Rows[i]))
                        exec 'Table.createLine'+str(tuple(columns))
                return Table.rtn()
        
        def MainBar(self):
                form=html.form(Titel='Allgemeine Funktionen',Datei='start.py')
                form.add_Hidden(ElementName='mn',Wert='pupil')
                form.open_paragraph()
                form.add_Entry(ElementName='AFVorname',Beschriftung='Vorname')
                form.add_Entry(ElementName='AFNachname',Beschriftung='Nachname')
                form.add_Entry(ElementName='AFGeburtstag',Beschriftung='Geburtstag')
                form.add_Entry(ElementName='AFJahrgang',Beschriftung='Jahrgang')
                form.add_Button(Beschriftung='Schueler hinzufuegen!',ElementName='AF',Wert='bla')
                form.end_paragraph()
                return form.rtn()

query=cgi.FieldStorage()
Suche=PupilSearchFunctions()
