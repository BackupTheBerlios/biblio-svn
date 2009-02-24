#!C:/Python25/python.exe
# -*- coding: cp1252 -*-
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
pfad="backups/"
adm_user="root"
adm_pw=""
import cgitb
cgitb.enable()

def content():
    import modules.html as html,cgi
    p=""

    form=cgi.FieldStorage()
    if ('act' in form.keys()) and ('ts' in form.keys()):
        if form['act'].value=="wh":
            p+=wiederherstellen(form['ts'].value+".sql")
        elif form['act'].value=="del":
            p+=delete(form['ts'].value+".sql")
        elif form['act'].value=="sp":
            p+=speichern(form['ts'].value)
    else:
        p+=html.headline('Backup-Verzeichnis').rtn()
        p+=uebersicht()
    return str(p)

def wiederherstellen(FileName):
    import modules.database as database, modules.html as html, os
    htm=""

    #Datei vorhanden?
    if os.path.isfile(pfad+FileName)==True:
        #Versuch, das Backup einzuspielen
        try:
            fl=file(pfad+FileName, 'r')
            db = database.Database()
            db.user=adm_user
            db.pw=adm_pw
            db.__init__()
            db.query(fl.read())
            fl.close()
            htm+=html.message("Backup wiederhergestellt!","Zur&uuml;ck","start.py?mn=backup",2).rtn()
        except:
            htm+=html.message("Backup fehlerhaft!","Zur&uuml;ck","start.py?mn=backup",1).rtn()
    else:
        htm+=html.message("Backup nicht vorhanden!","Zur&uuml;ck","start.py?mn=backup",1).rtn()

    return htm

def speichern(timestamp):
    import modules.html as html,cgi
    htm=""
    form=cgi.FieldStorage()

    if ('conf' in form.keys()):
        #Zweiter Schritt: backup in Datei schreiben
        import modules.database as database
        db=database.Database()
        fl=open(pfad+timestamp+".sql",'w')
        try:
            kom=form['kom'].value
        except:
            kom=""
        f="#"+kom+"\n"+db.backup()
        fl.write(f)
        fl.close
        htm+=html.message("Backup erstellt","Zur&uuml;ck","start.py?mn=backup",2).rtn()
    else:
        #Erster Schritt mit Abfrage
        htm+=html.headline("Neues Backup erstellen...").rtn()
        htm+=html.paragraph("Bitte geben Sie ggf. einen kurzen Kommentar (max. 30 Zeichen) ein und dr&uuml;cken Sie dann auf Speichern.").rtn()
        htm+='''<fieldset><legend>Backup erstellen</legend><form action="./start.py" method="get">
        <input type="hidden" name="mn" value="backup" />
        <input type="hidden" name="act" value="sp" />
        <input name="ts" type="hidden" value="'''+timestamp+'''" />
        <p>Kommentar: <input name="kom" type="text" maxlength="30" /></p>
        <p>
        <input type="hidden" name="conf" value="1" />
        <input type="submit" value="Speichern" />
        <input type="button" name="abort" value="Abbrechen" onclick="window.navigate("./start.py?mn=backup")" />
        </p>
        </form></fieldset>'''

    return htm

def delete(FileName):
    import modules.html as html,os

    #Abfrage ob Datei existiert
    if os.path.isfile(pfad+FileName)==True:
        os.remove(pfad+FileName)
        h=html.message("Backup erfolgreich gel&ouml;scht!","Zur&uuml;ck","start.py?mn=backup",2).rtn()
    else:
        h=html.message("Backup existiert nicht...","Zur&uuml;ck","start.py?mn=backup",1).rtn()

    return h

def uebersicht():
    import modules.html as html, time
    neu = html.link(Datei = 'backup', Text = 'Neues Backup erstellen ...')
    neu.add_param(Name = 'act', Wert = 'sp')
    neu.add_param(Name = 'ts', Wert = str(int(time.time())))
    neu = neu.rtn()
    h=""
    h+=html.paragraph(neu).rtn()
    t=html.table("Nr.","Kommentar","Datum","Optionen")

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

    #Tabelle mit Daten f&uuml;llen
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
        import Cookie, os, modules.database as database
        db=database.Database()
        c=Cookie.SimpleCookie()
        c.load(os.environ['HTTP_COOKIE'])
        bn=c['Benutzername'].value
        rights=db.query('SELECT Backend FROM benutzer WHERE Benutzername="'+bn+'"')[0][0]
        del(db)

        #Wiederherstellen / L&ouml;schen
        if rights==1:
			wbutton=html.link(Datei = 'backup',Text = 'Restore')
			wbutton.add_param(Name = 'act', Wert = 'wh')
			wbutton.add_param(Name = 'ts', Wert = f[i][:-4])
			wbutton = wbutton.rtn()
            #wbutton='''<a href="start.py?mn=backup&act=wh&ts='''+f[i][:-4]+'''">Restore</a>'''
			lbutton=html.link(Datei = 'backup',Text = 'L&ouml;schen')
			lbutton.add_param(Name = 'act', Wert = 'del')
			lbutton.add_param(Name = 'ts', Wert = f[i][:-4])
			lbutton = lbutton.rtn()
            #lbutton='''<a href="start.py?mn=backup&act=del&ts='''+f[i][:-4]+'''">L&ouml;schen</a>'''
        else:
            wbutton="..."
            lbutton="..."

        t.createLine(nr,kom,datum,wbutton+html.seperator().rtn()+lbutton)
    h+=t.rtn()
    h+=html.paragraph(neu).rtn()
    return h

if __name__=="__main__":
    print 'content-type: text/html'
    print
    print "main!"
    #Backup bei Einzelaufruf
    import modules.database as database, time
    db=database.Database()
    fl=open(pfad+str(int(time.time()))+".sql",'w')
    f="#Automatisches Backup vom "+time.strftime("%d.%m.%Y")+"\n"+db.backup()
    fl.write(f)
    fl.close

