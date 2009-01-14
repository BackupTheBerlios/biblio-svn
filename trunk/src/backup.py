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
pfad="../"

def content():
    p="helloü world!<br />"
    p+=uebersicht()
    return str(p)

def wiederherstellen(FileName):
    import table
    #TODO: öffnen
    #TODO: in db schreiben
    return html

def speichern():
    #TODO: kommentar, ok, speichern, timestamp
    return FileName

def uebersicht():
    import table
    html=""
    t=table.html_table("Nr.","Kommentar","Datum","Wiederherstellen","Löschen")
    #TODO: Dateien abfragen

    f=("1231917163.sql","1231571563.sql")
    #TODO: Kommentare auslesen
    k=("komm1","komm2")

    i=0
    for i in range(len(f)):
        line=[]
        #Nr
        nr=str(i+1)

        #Kommentar
        kom=k[i]

        #Datum
        from datetime import date
        datum=date.fromtimestamp(float(f[i][0:-4])).strftime("%d.%m.%Y")

        #TODO: Wiederherstellenbutton für Admin einbauen
        #Wiederherstellen
        wbutton="..."

        #TODO: Löschenbutton für Admin
        lbutton=".x."

        t.createLine(nr,kom,datum,wbutton,lbutton)
    html+=t.returnTable()
    return html

if __name__=="__main__":
    print uebersicht()