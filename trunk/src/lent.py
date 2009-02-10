# -*- coding: cp1252 -*-
#Aus-/Rückgabe Frontend
#===============================================================================
#
# ein/zwei-eingabefelder formular
# linkleiste
# zugriff auf suche
#===============================================================================

class Nummer():
    def buch2lang(self,nr_kurz):
        if int(nr_kurz)<10**9:
            return str(10**9+int(nr_kurz))
        else:
            raise ValueError,"Ungueltige Nummer!"
    def buch2kurz(self,nr_lang):
        if 2*10**9>int(nr_lang)>10**9:
            return str(int(nr_lang)-(10**9))
        else:
            raise ValueError,"Ungueltige Nummer!"
    def sch2lang(self,nr_kurz):
        if int(nr_kurz)<10**9:
            return str(2*10**9+int(nr_kurz))
        else:
            raise ValueError,"Ungueltige Nummer!"
    def sch2kurz(self,nr_lang):
        if int(nr_lang)>2*10**9:
            return str(int(nr_lang)-(2*10**9))
        else:
            raise ValueError,"Ungueltige Nummer!"
def content():
    #TODO: Titelleiste & Parameterabfrage /-weiterleitung
    import cgi,html
    form=cgi.FieldStorage()
    htm=""

    htm+="""<table><tr>
    <td><a href="./init.py?mn=lent&act=aus">Ausleihe</a></td>
    <td><a href="./init.py?mn=lent&act=rueck">Rückgabe</a></td>
    <td><a href="./init.py?mn=lent&act=manaus">Manuelle Ausleihe</a></td>
    <td><a href="./init.py?mn=lent&act=manrueck">Manuelle Rückgabe</a></td>
    </tr></table>"""
    if 'act' in form.keys():
        if form['act'].value == "manrueck":
            htm=htm.replace('<a href="./init.py?mn=lent&act=manrueck">Manuelle Rückgabe</a>',"...")
            if 'bn' in form.keys():
                htm+=manrueck(form['bn'])
            else:
                htm+=manrueck("")
        elif form['act'].value == "manaus":
            htm=htm.replace('<a href="./init.py?mn=lent&act=manaus">Manuelle Ausleihe</a>',"...")
            if 'bn' and 'ln' in form.keys():
                htm+=manaus(form['ln'],form['bn'])
            else:
                htm+=manaus("","")
        elif form['act'].value == "aus":
            htm=htm.replace('<a href="./init.py?mn=lent&act=aus">Ausleihe</a>',"...")
            if 'bn' and 'ln' in form.keys():
                htm+=aus(form['ln'],form['bn'])
            else:
                htm+=aus("","")
        elif form['act'].value == "rueck":
            htm=htm.replace('<a href="./init.py?mn=lent&act=rueck">Rückgabe</a>',"...")
            if 'bn' in form.keys():
                htm+=rueck(form['bn'])
            else:
                htm+=rueck("")
        else:
            htm+=html.message("Ungültiger Modus!","Leider gab es einen Fehler beim Aufruf...",0).rtn()
    else:
        htm+=html.paragraph("Beginnen Sie mit einem Klick auf die jeweilige Aktion...").rtn()

    return htm

def manrueck(booknr):
    import modules.ausleihe as ausleihe
    htm = ""
    a = ausleihe.Ausleihe

    if db.check("nr",booknr) and booknr!="":
        
        


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