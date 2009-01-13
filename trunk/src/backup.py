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

def content():
    p="hello&uuml; world!"
    return str(p)

def wiederherstellen(FileName):
    #TODO: öffnen, in db schreiben
    return html

def speichern():
    #TODO: kommentar, ok, speichern, timestamp
    return FileName

def uebersicht():
    import table
    html=""
    t=table.html_table("Nr.","Kommentar","Datum","Wiederherstellen","L&ouml;schen")
    #TODO: Dateien abfragen
    f=("file1","file2")
    #TODO: Kommentare auslesen
    k=("komm1","komm2")

    i=0
    for i in range(len(f)):
        line=[]
        #Nr
        nr=str(i)

        #Kommentar
        kom=k[i]

        #TODO: Datum aus timestamp erstellen
        #Datum
        datum=f[i]

        #TODO: Wiederherstellenbutton einbauen
        #Wiederherstellen
        wbutton="..."

        #TODO: Löschenbutton für Admin
        lbutton=".x."

        t.createLine(nr,kom,datum,wbutton,lbutton)
    html+=t.returnTable()
    return html

if __name__=="__main__":
    print uebersicht()