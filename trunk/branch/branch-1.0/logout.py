#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

import Cookie as ck
import modules.html as html

def ausloggen():
	c=ck.SimpleCookie()
	c['Benutzername']=''
	c['Benutzername']['expires']=-1
	print c
	print 'content-type: text/html'
	print
	output()

def output():
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
	print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="de" lang="de">'
	print '<head>'
	print '<link href="./css/style.css" rel="stylesheet" type="text/css" media="screen" />'
	print '</head>'
	print '<body>'
	print '<div id="output">'
	print '<div id="opt">'
	print '<h1>Logged out ...</h1>'
	print '</div>'
	print html.message(Title='Sie wurden erfolgreich ausgeloggt ...',ButtonLink1='./index.html',ButtonText1='Bis zum nächsten Mal! =)',MType=2).rtn()
	print '</div>'
	print '</body>'
	print '</html>'


if __name__ == '__main__':
	ausloggen()