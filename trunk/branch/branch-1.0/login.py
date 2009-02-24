#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

import cgi
import Cookie as ck
import modules.database as dtb
import modules.html as html
import httplib as http
db=dtb.Database()
import cgitb
cgitb.enable()

def content():
	einloggen()
	if logstatus==True:
		c=ck.SimpleCookie()
		c['Benutzername']=benutzer
		print c
	print 'content-type: text/html'
	print
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
	print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de" lang="de">'
	print '<head>'
	print '<link href="./css/style.css" rel="stylesheet" type="text/css" media="screen" />'
	if logstatus==True:
		print '<meta http-equiv="refresh" content="0; URL=start.py" />'
	print '</head>'
	print '<body>'
	print '<div id="output">'
	print '<div id="opt">'
	if logstatus==True:
		print '<h1>Logging in ...</h1>'
	else:
		print '<h1>Loginfehler</h1>'
	print '</div>'
	if logstatus==True:
		print html.message(Title='Weiterleitung aktiv ...',Description='Bitte haben Sie Geduld!',ButtonLink1='./start.py',ButtonText1='Ich werde nicht weitergeleitet!',MType=2).rtn()
	else:
		print html.message(Title='Fehler beim Login!',Description='Ihre eingegebenen Daten konnten nicht verwertet werden.',ButtonText1='Zurück',ButtonLink1='index.html',MType=0).rtn()
	print '</div>'
	print '</body>'
	print '</html>'

def einloggen():
	global logstatus, benutzer
	try:
		form=cgi.FieldStorage()
		benutzer='%s'%form['bn'].value
		passwort='%s'%form['pw'].value
		db.query('INSERT INTO logstatus VALUES ("'+benutzer+'", MD5("'+passwort+'"), CURRENT_TIMESTAMP)')
		log=db.query('SELECT Passwort FROM logstatus WHERE Benutzername = "'+benutzer+'"')[0]
		try:
			ben=db.query('SELECT Passwort FROM benutzer WHERE Benutzername = "'+benutzer+'"')[0]
			if log == ben:
				logstatus=True
			else:
				logstatus=False
		except:
			logstatus=False
		db.query('DELETE FROM logstatus WHERE Passwort = MD5("'+passwort+'")')
		db.query('OPTIMIZE TABLE logstatus')
	except:
		logstatus=False

content()