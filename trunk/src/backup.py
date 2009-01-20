# -*- coding: utf-8 -*-
#Wiederherstellen
#Speichern
#Tabellenzeichenfunktion
#"geplanter Task" name=main
#===============================================================================
#
# Speicherort:
# ordner/timestamp.sql
#
# FrontEnd-Tabelle:
# Wiederherstellen (-->db.query)
# Automatisches Backup
# Kommentar
#
# Backup erstellen:
# Kommentar
#
# Datei:
# # Kommentar hier...
# Inhalt
#===============================================================================
pfad="../backups/"

def content():
    import html,cgi
    p=""

    form=cgi.FieldStorage()
    if ('act' in form.keys()) and ('ts' in form.keys()):
        if form['act'].value=="wh":
            wiederherstellen(form['ts'].value)
        elif form['act'].value=="del":
            p=delete(form['ts'].value+".sql")
        elif form['act'].value=="sp":
            speichern()
    else:
        p+=html.headline('Backup-Verzeichnis').rtn()
        p+=uebersicht()
    return str(p)

def wiederherstellen(FileName):
    import database, html

    db = database.Database()
    fl=file(pfad+FileName, 'r')
    fl.close()

    db.query(fl.read())
    htm=""
    if os.path.isfile(pfad+FileName)==True:
        htm+=html.message("Backup wiederhergestellt!","zurück","./init.py?mn=backup",2).rtn()
    else:
        htm+=html.message("Backup nicht vorhanden!","zurück","./init.py?mn=backup",1)
    return htm

def speichern():
    #TODO: kommentar, ok, speichern, timestamp
    return html

def delete(FileName):
    import html,os

    if os.path.isfile(pfad+FileName)==True:
        os.remove(pfad+FileName)
        h=html.message("Backup erfolgreich gelöscht!","Zurück","./init.py?mn=backup",2).rtn()
    else:
        h=html.message("Backup existiert nicht...","Zurück","./init.py?mn=backup",1).rtn()

    return h

def uebersicht():
    import html
    h=""
    t=html.table("Nr.","Kommentar","Datum","Wiederherstellen","Löschen")

    #Dateien abfragen
    import os
    f=os.listdir(pfad)
    f.sort()

    #Kommentare auslesen
    k=[]
    for fs in f:
        fl=file(pfad+fs, 'r')
        k.append(fl.readline()[1:])
        fl.close()

    #Tabelle mit Daten füllen
    i=0
    for i in range(len(f)):
        line=[]
        #Nr
        nr=str(i+1)

        #Kommentar
        kom=k[i]

        #Datum
        from datetime import date
        datum=date.fromtimestamp(float(f[i][:-4])).strftime("%d.%m.%Y")

        #Adminrechte?
        import Cookie, os, database
        db=database.Database()
        c=Cookie.SimpleCookie()
        c.load(os.environ['HTTP_COOKIE'])
        bn=c['Benutzername'].value
        rights=db.query('SELECT Backend FROM benutzer WHERE Benutzername="'+bn+'"')[0][0]
        del(db)

        #Wiederherstellen / Löschen
        if rights==1:
            wbutton='''<a href="./init.py?mn=backup&act=wh&ts='''+f[i][:-4]+'''">Admin!</a>'''
            lbutton='''<a href="./init.py?mn=backup&act=del&ts='''+f[i][:-4]+'''">Admin!</a>'''
        else:
            wbutton="..."
            lbutton="..."

        t.createLine(nr,kom,datum,wbutton,lbutton)
    h+=t.rtn()
    h+=html.paragraph('''<div align="right"><a href="init.py?mn=backup?act=sp">Neues Backup erstellen...</a></div>''').rtn()
    return h

if __name__=="__main__":
    print uebersicht()