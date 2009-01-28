#Aus-/Rückgabe Frontend
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

    if 'act' in form.keys():
        if form['act'].value == "manrueck":

        elif form['act'].value == "manaus":
        elif form['act'].value == "aus":
        elif form['act'].value == "rueck":
        else:

    return htm

def manrueck(buchnummer):
    return htm

def manaus(lesernummer,buchnummer):
    return htm

def aus(lesernummer,buchnummer):
    return htm

def rueck(buchnummer):
    return htm