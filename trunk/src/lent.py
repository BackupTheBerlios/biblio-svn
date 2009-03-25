# -*- coding: cp1252 -*-
#Aus-/R&uuml;ckgabe Frontend
#===============================================================================

def submenue():
	sub={}
	sub[0]={'Ausleihe':'start.py?mn=lent&act=aus'}
	sub[1]={'R&uuml;ckgabe':'start.py?mn=lent&act=rueck'}
	return sub

def content():
    import cgi,modules.html as html,modules.liste as liste
    form=cgi.FieldStorage()
    htm=""

    if 'act' in form.keys():
        if form['act'].value == "aus":

            #Zuweisung der Variablen
            try: bn=form['bn'].value
            except KeyError: bn=""
            try: ln=form['ln'].value
            except KeyError: ln=""

            #Mode-Auswahl
            if 'lend' in form.keys():
               htm+=aus(ln,bn,"lend")
               htm+=html.paragraph("Der Sch&uuml;ler hat nun folgende B&uuml;cher ausgeliehen:").rtn()
               htm+=liste.zeige_buch(ln)
            elif 'save' in form.keys():
                htm+=aus(ln,bn,"save")
                htm+=html.paragraph("Der Sch&uuml;ler hat nun folgende B&uuml;cher ausgeliehen:").rtn()
                htm+=liste.zeige_buch(ln)
            else:
                htm+=aus()
        elif form['act'].value == "rueck":
            htm=htm.replace('<a href="./start.py?mn=lent&act=rueck">R&uuml;ckgabe</a>',"...")
            if 'bn' in form.keys():
                try:
                    import modules.ausleihe
                    a=modules.ausleihe.Ausleihe()
                    pupn=a.book_loaned(form['bn'].value)
                except:
                    pupn=0

                htm+=rueck(form['bn'].value)
                htm+=html.paragraph("Der Sch&uuml;ler hat noch folgende B&uuml;cher ausgeliehen:").rtn()
                htm+=liste.zeige_buch(str(pupn))
            else:
                htm+=rueck("")
        else:
            htm+=html.message(Title="Ung&uuml;ltiger Modus!",Description="Leider gab es einen Fehler beim Aufruf...",ButtonText1="Zur&uuml;ck",ButtonLink1="javascript:history.back();",MType=0).rtn()

    else:
        #htm+=html.paragraph("Beginnen Sie mit einem Klick auf die jeweilige Aktion...").rtn()
		htm+=aus()

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
                    pass
            except:
                htm+=html.paragraph('<div style="background-color:red">Bitte geben Sie g&uuml;ltige Nummern ein!</div>').rtn()
                pass


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
            <input type="submit" name="mysubmit" value="Rueckgabe" tabindex="2" />
            </p>
            </form></fieldset>'''
    return htm
