#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

import cgi
import Cookie, os
import modules.html as html
import re
import xml.dom.minidom as xml
import cgitb
cgitb.enable()

global address

#Erstellen des Templates
class template():
	def __init__(self):
		self.URL=address
		file=open('css/template.tpl','r')
		self.Template=file.read()
		file.close()
		self.__templatetags()
		self.__ictags()
	def __templatetags(self):
		#Templatetags
		tt=re.compile('<§+([\w]*|[\W]*)\>',(re.I|re.U|re.S))
		Doc=xml.parse('XML/options.xml')
		Root=Doc.documentElement
		Configs=Root.getElementsByTagName('config')
		for t in tt.findall(self.Template):
			for Config in Configs:
				Titel=str(Config.getAttribute('title'))
				if Titel==t:
					tag=str(Config.firstChild.data)
					self.Template=self.Template.replace('<§'+t+'>',tag)
	def __ictags(self):
		#IC-Tags
		ic=re.compile('<§+([\w]*|[\W]*)>',(re.I|re.U|re.S))
		for i in ic.findall(self.Template):
		#DEBUGGER
#			try:
			import modules.database as dtb
			db=dtb.Database()
			db.query('set character set utf8') #Legt die UTF-8 Codierung fest!!
			exec 'inhalt=%s().rtn()'%i
			self.Template=self.Template.replace('<§'+i+'>',inhalt)
#			except:
#				self.Template=self.Template.replace('<§'+i+'>','')
	def rtn(self):
		return self.Template

class menue():
	def __init__(self):
		self.Menue=''
		self.__createMenue()
	def __createMenue(self):
		Doc=xml.parse('XML/menue.xml')
		Root=Doc.documentElement
		Groups=Root.getElementsByTagName('group')
		for Group in Groups:
			Items=Group.getElementsByTagName('item')
			for Item in Items:
				Titel=str(Item.getAttribute('title'))
				Name=str(Item.getAttribute('name'))
				if Item is Items[len(Items)-1] and Group is not Groups[len(Groups)-1]:
					self.Menue+='<dl class="objs">'
				else:
					self.Menue+='<dl class="obj">'
				Bild = html.image(Datei = Name+'.png').rtn()
				Bildlink = html.link(Datei=Name,Text=Bild)
				self.Menue+='<dt>'+Bildlink.rtn()+'</dt>'
				Textlink = html.link(Datei=Name,Text=Titel)
				self.Menue+='<dd>'+Textlink.rtn()+'</dd>'
				self.Menue+='</dl>'
	def rtn(self):
		return str(self.Menue)

class options():
	def __init__(self):
		self.URL=address
		self.headline=''
		self.__headline()
	def __headline(self):
		Doc=xml.parse('XML/menue.xml')
		Root=Doc.documentElement
		Items=Root.getElementsByTagName('item')
		for Item in Items:
			Titel=str(Item.getAttribute('title'))
			Name=str(Item.getAttribute('name'))
			if self.URL == Name:
				self.headline=str(Titel)
		if self.URL=='log-error': self.headline='Verbindungsstop'
	def rtn(self):
		leiste = ''
		leiste += html.opthead(self.headline).rtn()
		mini = html.image(Datei = 'mini.jpg', Alternativ = '[Minimieren]', Titel = 'Seitenleiste minimieren').rtn()
		leiste += html.link(Datei = 'other=javascript:flupp();',Text = mini,Titel = 'Seitenleiste minimieren').rtn()
		oben = html.image(Datei = 'top.jpg', Alternativ = '[Nach oben]', Titel = 'Zum Seitenanfang').rtn()
		leiste += html.link(Datei = 'other=#oben',Text = oben,Titel = 'Zum Seitenanfang').rtn()
		logout = html.image(Datei = 'logout.jpg', Alternativ = '[Logout]', Titel = 'Loggt Sie aus dem System aus ...').rtn()
		leiste += html.link(Datei='main=logout',Text = logout).rtn()
		return leiste

class bar():
	def __init__(self):
		try:
			exec 'import %s as cnt'%address
			self.Inhalt = cnt.bar()
		except:
			self.Inhalt = ''
	def rtn(self):
		return self.Inhalt

class content():
	def __init__(self):
		if not address == 'log-error':
		#DEBUGGER
#			try:
			exec 'import %s as cnt'%address
			self.Inhalt=cnt.content()
#			except:
#				msg=html.headline('Fehlendes Modul!').rtn()
#				Fehler='Das Modul <strong><em>%s.py</em></strong> konnte nicht gefunden werden!'%address
#				msg+=html.paragraph(Fehler).rtn()
#				self.Inhalt=msg
		else:
			self.Inhalt=html.message(Title='Der Zugang wurde Ihnen untersagt!',Description='Womöglich wurden Sie durch ein Timeout ausgeloggt ...',ButtonText1='Einloggen',ButtonLink1='index.html',MType=0).rtn()
	def rtn(self):
		return self.Inhalt

if __name__ == '__main__':
	c=Cookie.SimpleCookie()
	try:
		c.load(os.environ['HTTP_COOKIE'])
		nn=1 #Cookie vorhanden!!! - User ist angemeldet
		c['Benutzername']['expires']=3*3600 #Cookielebensdauer auf drei Stunden setzen (3*3600 Sekunden)
		print c
	except:
		nn=0 #User ist noch nicht angemeldet!
	global query
	print 'content-type: text/html'
	print
	if nn==1:
		query=cgi.FieldStorage()
		address=query.getvalue('mn')
		if address == None: address='home'
		print template().rtn()
	else:
		address='log-error'
		print template().rtn()
