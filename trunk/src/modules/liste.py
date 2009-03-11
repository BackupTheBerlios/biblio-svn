class Liste:
    def zeige_buch(pupilnummer):
        import html,ausleihe
        a=ausleihe.Ausleihe()
        htm=''

        try:
            bks=a.pupil_got(pupilnummer)
        except ValueError, e:
            htm=html.paragraph('<div style="background-color:red">Fehler bei der Abfrage der ausgeliehenen B&uuml;cher!</div>').rtn()
        print bks
        return htm