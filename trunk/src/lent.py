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
    <td><a href="./init.py?mn=lent&act=aus">Ausleihe</a></td>
    <td><a href="./init.py?mn=lent&act=rueck">R�ckgabe</a></td>
    <td><a href="./init.py?mn=lent&act=manaus">Manuelle Ausleihe</a></td>
    <td><a href="./init.py?mn=lent&act=manrueck">Manuelle R�ckgabe</a></td>
    </tr></table>"""
    if 'act' in form.keys():
        if form['act'].value == "manrueck":
            htm.replace('<td><a href="./init.py?mn=lent&act=manrueck">Manuelle R�ckgabe</a></td>',"...")
            if 'bn' in form.keys():
                htm+=manrueck(form['bn'])
            else:
                htm+=manrueck("")
        elif form['act'].value == "manaus":
            htm.replace('<td><a href="./init.py?mn=lent&act=manaus">Manuelle Ausleihe</a></td>',"...")
            if 'bn' and 'ln' in form.keys():
                htm+=manaus(form['ln'],form['bn'])
            else:
                htm+=manaus("","")
        elif form['act'].value == "aus":
            htm.replace('<td><a href="./init.py?mn=lent&act=aus">Ausleihe</a></td>',"...")
            if 'bn' and 'ln' in form.keys():
                htm+=aus(form['ln'],form['bn'])
            else:
                htm+=aus("","")
        elif form['act'].value == "rueck":
            htm.replace('<td><a href="./init.py?mn=lent&act=rueck">R�ckgabe</a></td>',"...")
            if 'bn' in form.keys():
                htm+=rueck(form['bn'])
            else:
                htm+=rueck("")
        else:
            htm+=html.message("Ung�ltiger Modus!","Leider gab es einen Fehler beim Aufruf...",0).rtn()
    else:
        htm+=html.paragraph("Beginnen Sie mit einem Klick auf die jeweilige Aktion...").rtn()

    return htm

def manrueck(buchnummer):
    import modules.ausleihe as ausleihe
    htm = ""
    a = ausleihe.Ausleihe

    return htm


def manaus(lesernummer,buchnummer):
    htm=""
    return htm

def aus(lesernummer,buchnummer):
    htm=""
    return htm

def rueck(buchnummer):
    htm=""
    return htm