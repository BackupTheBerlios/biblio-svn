# -*- coding: cp1252 -*-
#Aus-/R&uuml;ckgabe Frontend
#===============================================================================

def content():
    import cgi,modules.html as html,modules.liste as liste
    form=cgi.FieldStorage()
    htm=""

    htm+="""<table><tr>
    <td><a href="./start.py?mn=lent&act=aus">Ausleihe</a></td>
    <td><a href="./start.py?mn=lent&act=rueck">R&uuml;ckgabe</a></td>
    </tr></table>"""

    if 'act' in form.keys():
        if form['act'].value == "aus":
            htm=htm.replace('<a href="./start.py?mn=lent&act=aus">Ausleihe</a>',"...")

            #Zuweisung der Variablen
            try: bn=form['bn'].value
            except KeyError: bn=""
            try: ln=form['ln'].value
            except KeyError: ln=""

            #Mode-Auswahl
            if 'lend' in form.keys():
               htm+=aus(ln,bn,"lend")
               htm+=html.paragraph("Der Sch&uuml;ler hat noch folgende B&uuml;cher ausgeliehen:").rtn()
               htm+=liste.zeige_buch(bn)
            elif 'save' in form.keys():
                htm+=aus(ln,bn,"save")
                htm+=html.paragraph("Der Sch&uuml;ler hat noch folgende B&uuml;cher ausgeliehen:").rtn()
                htm+=liste.zeige_buch(bn)
            else:
                htm+=aus()
        elif form['act'].value == "rueck":
            htm=htm.replace('<a href="./start.py?mn=lent&act=rueck">R&uuml;ckgabe</a>',"...")
            if 'bn' in form.keys():
                htm+=rueck(form['bn'].value)
                htm+=html.paragraph("Der Sch&uuml;ler hat noch folgende B&uuml;cher ausgeliehen:").rtn()
                htm+=liste.zeige_buch(form['bn'].value)
            else:
                htm+=rueck("")
        else:
            htm+=html.message("Ung&uuml;ltiger Modus!","Leider gab es einen Fehler beim Aufruf...",0).rtn()

    else:
        htm+=html.paragraph("Beginnen Sie mit einem Klick auf die jeweilige Aktion...").rtn()

    return htm

def aus(lesernummer="",buchnummer="",mode=""):
    import modules.html as html
    htm=''
    ln=""
    bn=""

    if mode!="":
        if lesernummer and buchnummer != "":
            import modules.ausleihe as ausleihe, modules.kurzlang as kurzlang
            a=ausleihe.Ausleihe()
            try:
                l=kurzlang.sch2kurz(lesernummer)
                b=kurzlang.buch2kurz(buchnummer)
                try:
                    a.borrow(l,b)
                    htm+=html.paragraph('<div style="background-color:green">Buch '+buchnummer+' wurde an '+lesernummer+' erfolgreich ausgeliehen.</div>').rtn()
                except ValueError, error:
                    htm+=html.paragraph('<div style="background-color:red">'+error.message+'</div>').rtn()
            except ValueError:
                htm+=html.paragraph('<div style="background-color:red">Bitte geben Sie g&uuml;ltige Nummern ein!</div>').rtn()


        else:
            htm+=html.paragraph('<div style="background-color:red">Bitte Buch- <i>und</i> Lesernummer eingeben</div>').rtn()
        if mode=="save":
            ln=str(lesernummer)
            htm+='<body onload="document.fo.bn.focus();">'
        else:
            htm+='<body onload="document.fo.ln.focus();">'
    else:
        htm+='<body onload="document.fo.ln.focus();">'

    htm+='''<fieldset><form name="fo" action="./start.py" method="get">
            <input type="hidden" name="mn" value="lent" />
            <input type="hidden" name="act" value="aus" />
            <p>Scannen oder w&auml;hlen Sie bitte Leser- und Buchnummer aus:</p>
            <p>
            Lesernummer: <input type="text" name="ln" value="'''+ln+'''" maxlength="10" tabindex="1" onkeyup="if(document.fo.ln.value.length==10){document.fo.bn.focus()};" /><a href="./start.py?mn=pupil" target="_blank">Leser suchen...</a><br />
            Buchnummer: <input type="text" name="bn" value="'''+bn+'''" maxlength="10" tabindex="2" onkeyup="if(document.fo.bn.value.length==10){document.fo.lend.focus()};" /><a href="./start.py?mn=books" target="_blank">Buch suchen...</a><br />
            <input type="submit" name="lend" value="Ausleihen." tabindex="3" />
            <input type="submit" name="save" value="Ausleihen und Lesernummer beibehalten..." tabindex="4" />
            </p>
            </form></fieldset>'''

    return htm


def rueck(buchnummer=""):
    import modules.html as html
    htm = ''

    if buchnummer!="":
        import modules.ausleihe as ausleihe, modules.kurzlang as kurzlang
        a = ausleihe.Ausleihe()

        try:
            buchnummer = kurzlang.buch2kurz(buchnummer)
            try:
                a.handback(buchnummer)
                htm+=html.paragraph('<div style="background-color:green">Buch '+buchnummer+' wurde erfolgreich zur&uuml;ckgegeben.</div>').rtn()
            except ValueError, error:
                htm+=html.paragraph('<div style="background-color:red">'+error.message+'</div>').rtn()
        except ValueError:
            htm+=html.paragraph('<div style="background-color:red">Bitte geben Sie eine g&uuml;ltige Nummer ein!</div>').rtn()

    htm+='''<body onload="document.fo.bn.focus();">
            <fieldset><form name="fo" action="./start.py" method="get">
            <input type="hidden" name="mn" value="lent" />
            <input type="hidden" name="act" value="rueck" />
            <p><U>Scannen oder w&auml;hlen Sie bitte die Buchnummer aus:</U></p>
            <p>
            <input type="text" name="bn" maxlength="10" tabindex="1" onkeyup="if(document.fo.bn.value.length==10){document.fo.mysubmit.focus()};" /><a href="./start.py?mn=books" target="_blank">Buch suchen...</a><br />
            <input type="submit" name="mysubmit" value="R&uuml;ckgabe" tabindex="2" />
            </p>
            </form></fieldset>'''
    return htm