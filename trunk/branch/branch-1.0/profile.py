#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

import cgitb
cgitb.enable()
import modules.database as dtb
db=dtb.Database()
import modules.html as html

def content():
	import cgi
	form=cgi.FieldStorage()
	#Überprüfen der Admin-Rechte
	if user().admin() == True:
		if (form.has_key('action')):
#			try:
			task='%s'%form['action'].value
			if task == 'new':
				prf = profile()
				msg = prf.new()
			elif task=='save':
				Passwort='%s'%form['PW'].value
				CPasswort='%s'%form['CPW'].value
				Benutzername='%s'%form['BN'].value
				try:
					Rechte='%s'%form['rechte'].value
				except:
					Rechte='0'
				if Passwort==CPasswort:
					prf = profile(pbn=Benutzername,ppw=Passwort,pcpw=CPasswort,prgts=int(Rechte))
					msg = prf.save()
				else:
					msg = html.message(Title='Fehler bei der Passworteingabe!',Description='Ihre Eingabe war nicht gleich ...',ButtonLink1='start.py?mn=profile',ButtonText1='Zurück',MType=0).rtn()
			elif task == 'editor':
				Nummer='%s'%form['ID'].value
				prf = profile(pnmb=int(Nummer))
				msg = prf.editor()
			elif task == 'clear':
				Nummer = '%s'%form['ID'].value
				prf = profile(pnmb=int(Nummer))
				msg = prf.clear()
			elif task=='edit':
				Nummer='%s'%form['ID'].value
				Passwort='%s'%form['PW'].value
				CPasswort='%s'%form['CPW'].value
				try:
					Rechte='%s'%form['rechte'].value
				except:
					Rechte='0'
				prf = profile(pnmb=Nummer,ppw=Passwort,pcpw=CPasswort,prgts=Rechte)
				if Passwort==CPasswort:
					msg = prf.edit()
				else:
					msg = html.message(Title='Fehler bei der Passworteingabe!',Description='Ihre Eingabe war nicht gleich ...',ButtonLink1='start.py?mn=profile',ButtonText1='Zur&uuml;ck',MType=0).rtn()
#			except:
#				msg = html.message(Title='Es ist ein Fehler aufgetreten!',Description='Vermutlich haben Sie keine oder eine ung&uuml;ltige Eingabe gemacht ...',ButtonText1='Zur&uuml;ck',ButtonLink1='start.py?mn=profile',MType=0).rtn() #Wenn gar nix klappt ...
		else:
			prf=profile()
			msg = prf.show() #User anzeigen!!
	else:
		usr = user()
		msg = usr.show()
	return msg

class user():
	def __init__(self):
		import Cookie,os
		c=Cookie.SimpleCookie()
		c.load(os.environ['HTTP_COOKIE'])
		self.bn = c['Benutzername'].value
		self.rights = 0
	def admin(self):
		self.rights=db.query('SELECT Backend FROM benutzer WHERE Benutzername="'+self.bn+'"')[0][0]
		if self.rights == 1:
			return True
		else:
			return False
	def show(self):
		cnt = ''
		cnt += html.headline('Benutzer').rtn()
		nn=db.query('SELECT ID FROM benutzer WHERE Benutzername = "'+self.bn+'"')[0][0]
		user_edit = html.form(Titel='Passwort &auml;ndern',Datei='start.py')
		user_edit.add_Hidden(ElementName = 'mn', Wert = 'profile')
		user_edit.add_Hidden(ElementName = 'action', Wert = 'edit')
		user_edit.add_Hidden(ElementName = 'BN', Wert = self.bn)
		user_edit.add_Hidden(ElementName = 'ID', Wert = nn)
		user_edit.add_Hidden(ElementName = 'rechte', Wert = self.rights)
		user_edit.use_table(None)
		user_edit.demand_table('createLine('+"'"+'<label for="PW">Passwort:</label>'+"'"+','+"'"+'<input type="password" name="PW" value="" />'+"'"+')')
		user_edit.demand_table('createLine('+"'"+'<label for="CPW">Passwortwiederholung:</label>'+"'"+','+"'"+'<input type="password" name="CPW" value="" />'+"'"+')')
		user_edit.rtn_Table()
		user_edit.add_Button(Beschriftung = 'Speichern')
		cnt += user_edit.rtn()
		return cnt

class profile():
	def __init__(self,pbn='',ppw='',pcpw='',prgts=0,pnmb=-1):
		import Cookie,os
		c=Cookie.SimpleCookie()
		c.load(os.environ['HTTP_COOKIE'])
		self.bn = c['Benutzername'].value
		self.cnt = ''
		self.pbn = pbn
		self.ppw = ppw
		self.pcpw = pcpw
		self.prgts = prgts
		self.pnmb = pnmb
	
	def new(self):
		self.cnt += '<fieldset><legend>Benutzer hinzuf&uuml;gen</legend><form action="start.py" method="get"><input type="hidden" name="mn" value="profile" /><input type="hidden" name="action" value="save" /><label for="BN">Benutzername:</label><p><input type="text" name="BN" id="BN" value="" /></p><label for="PW">Passwort:</label><p><input type="password" name="PW" id="PW" value="" /></p><label for="CPW">Passwortwiederholung:</label><p><input type="password" name="CPW" id="CPW" value="" /></p><p><input type="checkbox" name="rechte" value="1" /> Diesem Account Adminrechte zuschreiben.</p><p><button type="submit">Hinzuf&uuml;gen</button></p></form></fieldset>'
		self.cnt += html.link(Datei = 'profile.py',Text = 'Zur&uuml;ck ...').rtn()
		return self.cnt

	def save(self):
		import string as sto
		BN_list=db.query('SELECT Benutzername FROM benutzer')
		for row in BN_list:
			unikat=True
			old_BN=''
			for i in str(row)[2:len(str(row))-3]:
				old_BN+=sto.capitalize(i)
			planned_BN=''
			for i in self.pbn:
				planned_BN+=sto.capitalize(i)
			if old_BN == planned_BN:
				unikat=False
				break
		if unikat == True:
			db.query('INSERT INTO benutzer (ID, Benutzername, Passwort, Backend) VALUES (NULL,"'+self.pbn+'", MD5("'+self.ppw+'"),'+str(self.prgts)+')')
			self.cnt += html.message(Title='Gew&uuml;nschter Benutzer erstellt.',Description='Aktuelle &Auml;nderungen sind sofort einsehbar ...',ButtonLink1='start.py?mn=profile',ButtonText1='Zur&uuml;ck',MType=2).rtn()
			if self.prgts==0:
				content='<strong>%s</strong> wurde von %s als neuer Benutzer hinzugef&uuml;gt.'%(self.pbn,self.bn)
			else:
				content='<strong>%s</strong> wurde von %s als neuer Administrator hinzugef&uuml;gt.'%(self.pbn,self.bn)
			db.query('INSERT INTO notizen (ID, Inhalt, Autor ,Zeitpunkt) VALUES (NULL,"'+content+'", "System",CURRENT_TIMESTAMP)')
		else:
			self.cnt += html.message(Title='Fehler beim Erstellen des Accounts!',Description='Der Benutzername ist bereits vorhanden!',ButtonLink1='start.py?mn=profile&action=new',ButtonText1='Zur&uuml;ck',MType=0).rtn()
		return self.cnt

	def show(self):
		import string
		self.cnt += html.headline('Benutzer').rtn()
		new_user = html.link(Datei='profile.py',Text='Benutzer hinzuf&uuml;gen ...')
		new_user.add_param(Name='action',Wert='new')
		new_user = new_user.rtn()
		self.cnt += html.paragraph(new_user).rtn()
		ID_list=db.query('SELECT ID FROM benutzer ORDER BY Benutzername ASC')
		zaehler=len(ID_list)
		benutzerliste=html.table('Benutzername','Passwort (MD5)','Adminrechte','Optionen')
		for i in range(zaehler):
			x=ID_list[i][0]
			current_bn=db.query('SELECT Benutzername FROM benutzer WHERE ID='+str(x))[0][0]
			passwort=(db.query('SELECT Passwort FROM benutzer WHERE ID='+str(x))[0][0])[0:25]
			if (db.query('SELECT Backend FROM benutzer WHERE ID='+str(x))[0][0])==0:
				adminrechte='Nein'
			else:
				adminrechte='Ja'
			optionen=''
			edit = html.link(Datei = 'profile.py',Text = 'Bearbeiten')
			edit.add_param(Name = 'action', Wert = 'editor')
			edit.add_param(Name = 'ID', Wert = str(x))
			optionen += edit.rtn()
			UC_current_bn = ''
			for c in current_bn:
				UC_current_bn += string.capitalize(c)
			UC_self_bn = ''
			for s in self.bn:
				UC_self_bn += string.capitalize(s)
			if UC_current_bn != UC_self_bn:
				optionen+= html.seperator().rtn()
				clear = html.link(Datei = 'profile.py', Text = 'L&ouml;schen')
				clear.add_param(Name = 'action', Wert = 'clear')
				clear.add_param(Name = 'ID', Wert = str(x))
				optionen += clear.rtn()
			benutzerliste.createLine(current_bn,passwort[0:20]+'...',adminrechte,optionen)
		self.cnt+=benutzerliste.rtn()
		self.cnt += html.paragraph(new_user).rtn()
		return self.cnt

	def edit(self):
		res=db.query('SELECT Backend FROM benutzer WHERE ID = '+str(self.pnmb))[0]
		db.query('UPDATE benutzer SET Passwort = MD5("'+self.ppw+'"), Backend = '+str(self.prgts)+' WHERE ID ='+str(self.pnmb))
		self.cnt += html.message(Title='Gew&uuml;nschter Benutzer bearbeitet.',Description='Aktuelle &Auml;nderungen sind sofort einsehbar ...',ButtonLink1='start.py?mn=profile',ButtonText1='Zur&uuml;ck',MType=2).rtn()
		if not (str(res[0]) == str(self.prgts)):
			if self.prgts==0:
				content='<strong>%s</strong> wurde von %s zum Benutzer herabgestuft.'%(self.pbn,self.bn)
			else:
				content='<strong>%s</strong> wurde von %s zum Administrator heraufgestuft.'%(self.pbn,self.bn)
			db.query('INSERT INTO notizen (ID, Inhalt, Autor, Zeitpunkt) VALUES (NULL,"'+content+'", "System",CURRENT_TIMESTAMP)')
		return self.cnt

	def editor(self):
		res=db.query('SELECT Benutzername, Backend FROM benutzer WHERE ID ='+str(self.pnmb))[0]
		self.cnt += '<fieldset><legend>Benutzer ('+res[0]+') bearbeiten</legend><form action="start.py" method="get"><input type="hidden" name="mn" value="profile" /><input type="hidden" name="action" value="edit" /><input type="hidden" name="ID" value="%s" /><table><tr><td><label for="PW">Passwort:</label></td><td><input type="password" name="PW" value="" /></td></tr><tr><td><label for="CPW">Passwortwiederholung:</label></td><td><input type="password" name="CPW" value="" /></td></tr></table> '%self.pnmb
		self.cnt+='<p><button type="submit">&Auml;ndern</button></p>'
		if res[1]==0:
			self.cnt += '<p><input type="checkbox" name="rechte" value="1" /> Diesem Account Adminrechte zuschreiben.'
		else:
			self.cnt += '<p><input type="checkbox" name="rechte" value="1" checked="checked" /> Diesem Account Adminrechte zuschreiben.'
		self.cnt += '</form></fieldset>'
		self.cnt += html.link(Datei = 'profile.py',Text = 'Zur&uuml;ck ...').rtn()
		return self.cnt

	def clear(self):
		import string
		self.pbn=db.query('SELECT Benutzername FROM benutzer WHERE ID ='+str(self.pnmb))[0][0]
		UC_current_bn = ''
		for c in self.pbn:
			UC_current_bn += string.capitalize(c)
		UC_self_bn = ''
		for s in self.bn:
			UC_self_bn += string.capitalize(s)
		if UC_current_bn != UC_self_bn:
			db.query('DELETE FROM benutzer WHERE ID ='+str(self.pnmb))
			db.query('OPTIMIZE TABLE benutzer')
			content='<strong>%s</strong> wurde von %s gel&ouml;scht.'%(self.pbn,self.bn)
			db.query('INSERT INTO notizen (ID, Inhalt, Autor ,Zeitpunkt) VALUES (NULL,"'+content+'", "System",CURRENT_TIMESTAMP)')
			self.cnt += html.message(Title='Gew&uuml;nschter Benutzer ('+self.pbn+') gel&ouml;scht.',Description='Aktuelle &Auml;nderungen sind sofort einsehbar ...',ButtonLink1='start.py?mn=profile',ButtonText1='Zur&uuml;ck',MType=2).rtn()
		else:
			self.cnt += html.message(Title='Sie k&ouml;nnen sich nicht selbst l&ouml;schen!',ButtonLink1='start.py?mn=profile',ButtonText1='Zur&uuml;ck',MType=1).rtn()
		return self.cnt