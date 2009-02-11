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
    </tr></table>"""

    #<td><a href="./init.py?mn=lent&act=manaus">Manuelle Ausleihe</a></td>
    #<td><a href="./init.py?mn=lent&act=manrueck">Manuelle Rückgabe</a></td>

    if 'act' in form.keys():
#===============================================================================
#        if form['act'].value == "manrueck":
#            htm=htm.replace('<a href="./init.py?mn=lent&act=manrueck">Manuelle Rückgabe</a>',"...")
#            if 'bn' in form.keys():
#                htm+=manrueck(form['bn'])
#            else:
#                htm+=manrueck("")
#        elif form['act'].value == "manaus":
#            htm=htm.replace('<a href="./init.py?mn=lent&act=manaus">Manuelle Ausleihe</a>',"...")
#            if 'bn' and 'ln' in form.keys():
#                htm+=manaus(form['ln'],form['bn'])
#            else:
#                htm+=manaus("","")
#        el
#===============================================================================
        if form['act'].value == "aus":
            htm=htm.replace('<a href="./init.py?mn=lent&act=aus">Ausleihe</a>',"...")

            #Zuweisung der Variablen
            try: bn=form['bn']
            except KeyError: bn=""
            try: ln=form['ln']
            except KeyError: ln=""

            #Mode-Auswahl
            if 'lend' in form.keys():
               htm+=aus(ln,bn,"lend")
            elif 'save' in form.keys():
                htm+=aus(ln,bn,"save")
            else:
                htm+=aus(ln,bn,"")
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

#===============================================================================
# def manrueck(booknr):
#    import modules.ausleihe as ausleihe
#    htm = ""
#    a = ausleihe.Ausleihe
#
#    if db.check("nr",booknr) and booknr!="":
#
#
#
#
#    return htm
#
#
# def manaus(lesernummer,buchnummer):
#    htm=""
#    return htm
#===============================================================================

def aus(lesernummer,buchnummer,mode=""):
    htm=''

    if mode=="":
        htm+='''<body onload="document.fo.ln.focus();">
            <form name="fo" action="./init.py" method="get">
            <input type="hidden" name="mn" value="lent" />
            <input type="hidden" name="act" value="aus" />
            <p>Scannen oder wählen Sie bitte Leser- und Buchnummer aus:</p>
            <p>
            <input type="text" name="ln" maxlength="10" tabindex="1" onkeyup="if(document.fo.ln.value.length==10){document.fo.bn.focus()};" />
            <input type="text" name="bn" maxlength="10" tabindex="2" onkeyup="if(document.fo.bn.value.length==10){document.fo.lend.focus()};" />
            <input type="submit" name="lend" value="Ausleihen." tabindex="3" />
            <input type="submit" name="save" value="Ausleihen und Lesernummer beibehalten..." tabindex="4" />
            </p>
            </form>'''
    elif mode=="lend":
        #TODO: Lend-Mode schreiben
        print "lend"
    elif mode=="save":
        #TODO: Save-Mode schreiben
        print "save"

    return htm


def rueck(buchnummer):
    htm='''<body onload="document.fo.ln.focus();">
        <form name="fo" action="./init.py" method="get">
        <input type="hidden" name="mn" value="lent" />
        <input type="hidden" name="act" value="rueck" />
        <p>Scannen oder wählen Sie bitte Buchnummer aus:</p>
        <p>
        <input type="text" name="bn" maxlength="10" tabindex="1" />
        <input type="submit" name="mysubmit" value="Rückgabe" tabindex="2" />
        </p>
        </form>'''
    return htm