#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

import modules.database as dtb
db=dtb.Database()
import modules.html as html

def content():
	import cgi
	global Inhalt
	form=cgi.FieldStorage()
	if ('action' in form.keys()):
		try:
			task='%s'%form['action'].value
			if task == 'save':
				Inhalt='%s'%form['ct'].value
				Inhalt=Inhalt.replace('"','&quot;') #Zur Vorbeugung von MySQL-Injection
				if not Inhalt == '':
					nts=notes(ncnt=Inhalt)
					msg = nts.save() #Notiz speichern
			elif task == 'clear':
				Nummer='%s'%form['ID'].value
				nts=notes(nnmb=Nummer)
				msg = nts.clear() #Notiz löschen
			elif task == 'editor':
				Nummer='%s'%form['ID'].value
				nts=notes(nnmb=Nummer)
				msg = nts.editor() #Notiz bearbeiten
			elif task == 'edit':
				Inhalt='%s'%form['ct'].value
				Nummer='%s'%form['ID'].value
				if not Inhalt=='':
					nts=notes(ncnt=Inhalt, nnmb=Nummer)
					msg = nts.edit() #Änderungen speichern
			elif task == 'new':
				nts=notes()
				msg = nts.new()
		except:
			msg = html.message(Title='Es ist ein Fehler aufgetreten!',Description='Vermutlich haben Sie keine oder eine ungültige Eingabe gemacht ...',ButtonText1='Zurück',ButtonLink1='start.py?mn=home',MType=0).rtn() #Wenn gar nix klappt ...
	else:
		nts=notes()
		msg = nts.show() #Alle Notizen anzeigen
	return msg

class notes():
	def __init__(self,ncnt='',nnmb=-1):
		self.ncnt = ncnt #Notizinhalt
		self.nnmb = nnmb #Notiz-ID

	def save(self):
		import Cookie, os
		c=Cookie.SimpleCookie()
		c.load(os.environ['HTTP_COOKIE'])
		Autor='%s'%c['Benutzername'].value
		db.query('INSERT INTO notizen (ID, Inhalt, Autor ,Zeitpunkt) VALUES (NULL,"'+self.ncnt+'", "'+Autor+'",CURRENT_TIMESTAMP)')
		return html.message(Title='Notiz gespeichert.',Description='Aktuelle &Auml;nderungen sind sofort einsehbar ...',ButtonText1='Zur&uuml;ck',ButtonLink1='start.py?mn=home',MType=2).rtn()

	def clear(self):
		db.query('DELETE FROM notizen WHERE ID ='+str(self.nnmb))
		db.query('OPTIMIZE TABLE notizen')
		return html.message(Title='Gew&uuml;nschter Datensatz gel&ouml;scht ...',ButtonText1='Zur&uuml;ck',ButtonLink1='start.py?mn=home',MType=2).rtn()

	def editor(self):
		content=db.query('SELECT Inhalt FROM notizen WHERE ID ='+str(self.nnmb))[0][0]
		cnt='<fieldset class="wide"><legend>Notiz bearbeiten</legend><form action="start.py" method="get"><input type="hidden" name="action" value="edit" /><p><input type="hidden" name="ID" value="%s" /></p><label for="ct">Inhalt:</label><p><textarea name="ct">%s</textarea></p><p><button type="submit">Speichern</button></p></form></fieldset>'%(str(self.nnmb),content)
		cnt += html.link(Datei = 'home.py',Text = 'Zur&uuml;ck ...').rtn()
		return cnt

	def edit(self):
		import Cookie, os
		c=Cookie.SimpleCookie()
		c.load(os.environ['HTTP_COOKIE'])
		Autor='%s'%c['Benutzername'].value
		db.query('UPDATE notizen SET Inhalt = "'+self.ncnt+'", Zeitpunkt = NOW( ) WHERE ID = '+str(self.nnmb))
		return html.message(Title='&Auml;nderungen gespeichert.',Description='Aktuelle &Auml;nderungen sind sofort einsehbar ...',ButtonText1='Zur&uuml;ck',ButtonLink1='start.py?mn=home',MType=2).rtn()

	def show(self):
		import Cookie, os, re
		global notes_anz, ID_list
		c=Cookie.SimpleCookie()
		c.load(os.environ['HTTP_COOKIE'])
		ID_list=db.query('SELECT ID FROM notizen ORDER BY Zeitpunkt DESC')
		cnt=''
		cnt+=html.headline('Willkommmen '+c['Benutzername'].value+'! &middot;&nbsp;&middot;&nbsp;&middot; '+html.link(Datei='main=logout',Text='Ausloggen?',Titel='Logout').rtn()).rtn()
		if not (len(ID_list) == 0):
			mylink = html.link(Datei='home.py',Text='Neue Notiz anlegen ...')
			mylink.add_param(Name='action',Wert='new')
			neu = mylink.rtn()
			cnt+=html.paragraph(neu).rtn()
			notizen=html.table('Autor','Datum','Inhalt','Optionen')
			for ID in ID_list:
				Autor=db.query('SELECT Autor FROM notizen WHERE ID='+str(ID[0]))[0][0]
				if Autor == 'System':
					Autor = '<span class="highlight">'+Autor+'</span>'
				Datum=db.query('SELECT Zeitpunkt FROM notizen WHERE ID='+str(ID[0]))[0][0]
				Inhalt = db.query('SELECT Inhalt FROM notizen WHERE ID='+str(ID[0]))[0][0]
				tags=re.compile('<+([\w]*|[\W]*)\>',(re.I|re.U|re.S))
				Preview = Inhalt
				for tag in tags.findall(Inhalt): #Entfernen der HTML-Codierung im Vorschaumodus
					Preview = Preview.replace('<'+tag+'>','')
					Preview = Preview.replace('</'+tag+'>','')
				Inhalt = '<div id="note-'+str(ID[0])+'-pre">'+Preview[0:167]+'</div><div class="note" style="display : none;" id="note-'+str(ID[0])+'-full">'+Inhalt+'</div>'
				Optionen = ''
				change = html.link(Datei='other=javascript:change('+"'"+str(ID[0])+"'"+');',Text='Formatierung ein/aus')
				Optionen += change.rtn() #Vollanzeige
				Optionen += html.seperator().rtn()  #Seperator
				edit = html.link(Datei='home.py',Text='Bearbeiten')
				edit.add_param(Name='action',Wert='editor')
				edit.add_param(Name='ID',Wert=str(ID[0]))
				Optionen += edit.rtn() #Bearbeiten
				Optionen += html.seperator().rtn() #Seperator
				loeschen = html.link(Datei='home.py',Text='L&ouml;schen')
				loeschen.add_param(Name='action',Wert='clear')
				loeschen.add_param(Name='ID',Wert=str(ID[0]))
				Optionen += loeschen.rtn() #Löschen
				notizen.createLine(Autor,Datum,Inhalt,Optionen)
			cnt+=notizen.rtn()
			cnt+=html.paragraph(neu).rtn()
		else:
			neu = html.link(Datei='home.py',Text='Neue Notiz anlegen ...')
			neu.add_param(Name='action',Wert='new')
			cnt += html.paragraph('Keine Notizen vorhanden! &middot; &middot; &middot; '+neu.rtn()).rtn()
		return cnt

	def new(self):
		cnt='<fieldset class="wide"><legend>Neue Notiz</legend><form action="start.py" method="get"><input type="hidden" name="action" value="save" /><label for="ct">Inhalt:</label><p><textarea name="ct"></textarea></p><p><button type="submit">Speichern</button></p></form></fieldset>'
		cnt += html.link(Datei = 'home.py',Text = 'Zur&uuml;ck ...').rtn()
		return cnt