# -*- coding: cp1252 -*-
#Aus-/R�ckgabe Frontend
#===============================================================================
#
# ein/zwei-eingabefelder formular
# linkleiste
# zugriff auf suche
#===============================================================================

def content():
    #TODO: Titelleiste & Parameterabfrage /-weiterleitung
    import cgi,html
    form=cgi.FieldStorage()
    htm=""

    htm+="""<table><tr>
    <td>Ausleihe</td>
    <td>R�ckgabe</td>
    <td>Manuelle Ausleihe</td>
    <td>Manuelle R�ckgabe</td>
    </tr></table>"""
    if 'act' in form.keys():
        if form['act'].value == "manrueck":
            htm.replace("<td>Manuelle R�ckgabe</td>","...")
            htm+=manrueck(form['bn'])
        elif form['act'].value == "manaus":
            htm.replace("<td>Manuelle Ausleihe</td>","...")
            htm+=manaus(form['ln'],form['bn'])
        elif form['act'].value == "aus":
            htm.replace("<td>Ausleihe</td>","...")
            htm+=aus(form['ln'],form['bn'])
        elif form['act'].value == "rueck":
            htm.replace("<td>R�ckgabe</td>","...")
            htm+=rueck(form['bn'])
        else:
            htm+=html.message("Ung�ltiger Modus!","Leider gab es einen Fehler beim Aufruf...",0).rtn()
    else:
        htm+=html.paragraph("Beginnen Sie mit einem Klick auf die jeweilige Aktion...").rtn()

    return htm

def manrueck(buchnummer):
    return htm

def manaus(lesernummer,buchnummer):
    return htm

def aus(lesernummer,buchnummer):
    return htm

def rueck(buchnummer):
    return htm