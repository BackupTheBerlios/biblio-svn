# -*- coding: cp1252 -*-
#Aus-/Rückgabe Frontend
#===============================================================================
#
# ein/zwei-eingabefelder formular
# linkleiste
# zugriff auf suche
#===============================================================================

def content():
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
            try: bn=form['bn'].value
            except KeyError: bn=""
            try: ln=form['ln'].value
            except KeyError: ln=""

            #Mode-Auswahl
            if 'lend' in form.keys():
               htm+=aus(ln,bn,"lend")
            elif 'save' in form.keys():
                htm+=aus(ln,bn,"save")
            else:
                htm+=aus()
        elif form['act'].value == "rueck":
            htm=htm.replace('<a href="./init.py?mn=lent&act=rueck">Rückgabe</a>',"...")
            if 'bn' in form.keys():
                htm+=rueck(form['bn'].value)
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

def aus(lesernummer="",buchnummer="",mode=""):
    import html
    htm=''
    ln=""
    bn=""

    if mode!="":
        if lesernummer and buchnummer != "":
            import ausleihe,kurzlang
            a=ausleihe.Ausleihe()
            try:
                l=kurzlang.sch2kurz(lesernummer)
                b=kurzlang.buch2kurz(buchnummer)
                try:
                    a.borrow(l,b)
                    htm+=html.paragraph('<div style="background-color:green">Buch '+buchnummer+' wurde an '+lesernummer+' erfolgreich ausgeliehen.</div>').rtn()
                except ValueError, error:
                    htm+=html.paragraph('<div style="background-color:red">'+error.message+'</div>').rtn()
                    pass
            except ValueError:
                htm+=html.paragraph('<div style="background-color:red">Bitte geben Sie gültige Nummern ein!</div>').rtn()

        else:
            htm+=html.paragraph('<div style="background-color:red">Bitte Buch- <i>und</i> Lesernummer eingeben</div>').rtn()
        if mode=="save":
            ln=str(lesernummer)
            htm+='<body onload="document.fo.bn.focus();">'
        else:
            htm+='<body onload="document.fo.ln.focus();">'
    else:
        htm+='<body onload="document.fo.ln.focus();">'

    htm+='''<form name="fo" action="./init.py" method="get">
            <input type="hidden" name="mn" value="lent" />
            <input type="hidden" name="act" value="aus" />
            <p>Scannen oder wählen Sie bitte Leser- und Buchnummer aus:</p>
            <p>
            Lesernummer: <input type="text" name="ln" value="'''+ln+'''" maxlength="10" tabindex="1" onkeyup="if(document.fo.ln.value.length==10){document.fo.bn.focus()};" /><br />
            Buchnummer: <input type="text" name="bn" value="'''+bn+'''" maxlength="10" tabindex="2" onkeyup="if(document.fo.bn.value.length==10){document.fo.lend.focus()};" /><br />
            <input type="submit" name="lend" value="Ausleihen." tabindex="3" />
            <input type="submit" name="save" value="Ausleihen und Lesernummer beibehalten..." tabindex="4" />
            </p>
            </form>'''

    return htm


def rueck(buchnummer=""):
    import html
    htm = ''

    if buchnummer!="":
        import ausleihe, kurzlang
        a = ausleihe.Ausleihe()

        try:
            buchnummer = kurzlang.buch2kurz(buchnummer)
        except:
            pass
        try:
            a.handback(buchnummer)
            htm+=html.paragraph('<div style="background-color:green">Buch '+buchnummer+' wurde erfolgreich zurückgegeben.</div>').rtn()
        except ValueError, error:
            htm+=html.paragraph('<div style="background-color:red">'+error.message+'</div>').rtn()

    htm+='''<body onload="document.fo.bn.focus();">
            <form name="fo" action="./init.py" method="get">
            <input type="hidden" name="mn" value="lent" />
            <input type="hidden" name="act" value="rueck" />
            <p><U>Scannen oder wählen Sie bitte die Buchnummer aus:</U></p>
            <p>
            <input type="text" name="bn" maxlength="10" tabindex="1" onkeyup="if(document.fo.bn.value.length==10){document.fo.mysubmit.focus()};" /><br />
            <input type="submit" name="mysubmit" value="Rückgabe" tabindex="2" />
            </p>
            </form>'''
    return htm