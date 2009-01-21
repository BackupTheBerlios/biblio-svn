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
            p+=wiederherstellen(form['ts'].value)
        elif form['act'].value=="del":
            p+=delete(form['ts'].value+".sql")
        elif form['act'].value=="sp":
            p+=speichern(form['ts'].value)
    else:
        p+=html.headline('Backup-Verzeichnis').rtn()
        p+=uebersicht()
    return str(p)

def wiederherstellen(FileName):
    import database, html
    htm=""

    #Datei vorhanden?
    if os.path.isfile(pfad+FileName)==True:
        db = database.Database()
        fl=file(pfad+FileName, 'r')
        fl.close()
        #Versuch, das Backup einzuspielen
        try:
            db.query(fl.read())
            htm+=html.message("Backup wiederhergestellt!","zurück","./init.py?mn=backup",2).rtn()
        except:
            htm+=html.message("Backup fehlerhaft!","zurück","./init.py?mn=backup",1)
    else:
        htm+=html.message("Backup nicht vorhanden!","zurück","./init.py?mn=backup",1)

    return htm

def speichern(timestamp):
    import html,cgi
    htm=""
    form=cgi.FieldStorage()

    if ('conf' in form.keys()):
        #Zweiter Schritt: backup in Datei schreiben
        import database
        db=database.Database()
        fl=open(pfad+timestamp+".sql",'w')
        f="#"+form['kom'].value+"\n"+db.backup()
        fl.write(f)
        fl.close
        htm+=html.message("Backup erstellt","Zurück","./init.py?mn=backup",2).rtn()
    else:
        #Erster Schritt mit Abfrage
        htm+=html.headline("Neues Backup erstellen...").rtn()
        htm+=html.paragraph("Bitte geben Sie ggf. einen kurzen Kommentar ein und drücken Sie dann auf Speichern.").rtn()
        htm+='''<form action="./init.py?mn=backup&act=sp" method="get">
        <input type="hidden" name="mn" value="backup" />
        <input type="hidden" name="act" value="sp" />
        <input name="ts" type="hidden" value="'''+timestamp+'''" />
        <p>Kommentar: <input name="kom" type="text" maxlength="50" /></p>
        <p>
        <input type="hidden" name="conf" value="1" />
        <input type="submit" value="Speichern" />
        <input type="button" name="abort" value="Abbrechen" onclick="window.navigate("./init.py?mn=backup")" />
        </p>
        </form>'''

    return htm

def delete(FileName):
    import html,os

    #Abfrage ob Datei existiert
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
    import time
    h+=html.paragraph('''<div align="right"><a href="init.py?mn=backup&act=sp&ts='''+str(int(time.time()))+'''">Neues Backup erstellen...</a></div>''').rtn()
    return h

if __name__=="__main__":
    #Backup bei Einzelaufruf
    import database
    db=database.Database()
    fl=open(pfad+timestamp+".sql",'w')
    f="#"+form['kom'].value+"\n"+db.backup()
    fl.write(f)
    fl.close