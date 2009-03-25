import html

def zeigeJahrgang(jahr):
    import database as database
    db=database.Database()
    Inhalt = db.query("select p.vor, p.nach, t.Fachbereich, t.title, b.nr from pupil as p, book as b, type as t, ausleihe as a where a.pnr = p.nr and b.nr = a.bnr and t.nr = b.type and p.jahrgang = %s order by t.Fachbereich, p.nach"%str(jahr))
    Liste = html.table("Vorname", "Nachname", "Fachbereich", "Buchtitel", "Buchnummer")
    for Row in Inhalt:
        exec "Liste.createLine"+str(tuple(Row))
    return Liste.rtn()
def zeige_buch(pupilnummer):
    import html,ausleihe,book
    a=ausleihe.Ausleihe()
    b=book.Book()
    htm=''

    try:
        bks=a.pupil_got(pupilnummer)
    except Exception, e:
        htm+=html.paragraph('<div style="background-color:red">Fehler bei der Abfrage der ausgeliehenen B&uuml;cher!</div>').rtn()
        bks=()
    if bks==False:
        htm+=html.paragraph('<div style="background-color:green">Sch&uuml;ler hat kein Buch mehr ausgeliehen! :)</div>').rtn()
    else:
        t=html.table('Fachbereich','Titel','Buchnummer')
        for book in bks:
            info=b.info(book)
            t.createLine(info[3],info[2],str(book))
        htm+=t.rtn()
    return htm
