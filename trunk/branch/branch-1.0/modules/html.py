#!C:/Python25/python.exe
# -*- coding: cp1252 -*-

#Allgemeine Einstellungen
Base = 'start.py'
img_pfad = './css/img'

#+++++++++++++++++++++HTML-Tabelle(table)+++++++++++++++++++

class table():
    def __init__(self,*arg):
        self.Names=arg
        self.TableString=''
        self.klasse=0
        self.__createTable()

    def __createTable(self):
        self.__expand(self.__openTable())
        self.__expand(self.__createHeader())
        for name in self.Names:
            self.__expand(self.__createHead(name))
        self.__expand(self.__closeHeader())

        self.__expand(self.__createFooter())
        for name in self.Names:
            self.__expand(self.__createFoot(name))
        self.__expand(self.__closeFooter())
        self.__expand(self.__createBody())

    def __expand(self, string):
        self.TableString+=string
    def __openTable(self):
        return '<table>'
    def __closeTable(self):
        return '</table>'
    def __createBody(self):
        return '<tbody>'
    def __closeBody(self):
        return '</tbody>'

    def __createHeader(self):
        return '<thead><tr>'
    def __createHead(self,name):
        return '<th>%s</th>'%name
    def __closeHeader(self):
        return '</tr></thead>'

    def __createFooter(self):
        return '<tfoot><tr>'
    def __createFoot(self, name):
        return '<td>%s</td>'%name
    def __closeFooter(self):
        return '</tr></tfoot>'

    def __createLine(self):
        if self.klasse%2==1:
            return '<tr>'
        else:
            return '<tr class="sc">'
    def __createLineContent(self,value):
        return '<td>%s</td>'%value
    def __closeLine(self):
        return '</tr>'

    def createLine(self,*arg):
        self.klasse+=1
        if not len(arg)==len(self.Names):
            raise ValueError
        self.__expand(self.__createLine())
        for value in arg:
            self.__expand(self.__createLineContent(value))
        self.__expand(self.__closeLine())

    def rtn(self):
        self.__expand(self.__closeBody())
        self.__expand(self.__closeTable())
        return self.TableString

#+++++++++++++++++++++HTML-Meldung (message)+++++++++++++++++++

class message():
    '''Erklärung der Klasse message:
=============================
Die Klasse Message dient zur Darstellungen von Meldungen:

Meldungstypen:
--------------------
Fehler (MType=0) --> Icon: Fehlerkreuz, X
Warnungen(MType=1) --> Icon: Warndreieck, /!\
Informationen (MType=2) --> Icon: Info-Zeichen i
Frage (MType=3) --> Icon: Fragezeichen ?
Sonstige Meldungen (MType=jeder andere Wert) --> kein Icon

Verwenden der Klasse:
------------------
message(Eigenschaften).rtn()

Generelle Eigenschaften:
--------------
Title: Titel der Meldung
Description (optional): Weitergehende Beschreibung

Buttons:
--------
- Bis zu drei Buttons erstellbar (mind. 1 Button ist Pflicht)
- ButtonText[i], ButtonLink[i], ButtonTitle[i] -- [i] durch die Indexzahl 1,2 oder 3 ersetzen

ButtonText: Beschriftung des Buttons
ButtonLink: Wohin der Button zurückführt
ButtonTitle: Titel eines Buttons (ähnlich einem Tooltip, der beim Überfahren des Links erscheint) (optional)
'''
    def __init__(self,Title,ButtonText1,ButtonLink1,MType,ButtonTitle1='',Description='',ButtonText2='',ButtonTitle2='',ButtonLink2='',ButtonText3='',ButtonTitle3='',ButtonLink3=''):
        self.TextString=''
        self.ButtonNummer=0
        self.__createTitle(Title,MType)
        if not Description == '': self.__createDescription(Description)
        self.__startParagraph()
        self.__createButton(ButtonLink1,ButtonTitle1,ButtonText1)
        if not (ButtonText2 and ButtonLink2) == '': self.__createButton(ButtonLink2,ButtonTitle2,ButtonText2)
        if not (ButtonText3 and ButtonLink3) == '': self.__createButton(ButtonLink3,ButtonTitle3,ButtonText3)
        self.__endParagraph()


##Code
    def __expand(self,string):
        self.TextString+=string
    def __verify(self,MType):
        if -1 < MType < 4:
            return True
        else:
            return False


##Title
    def __startTitle(self):
        return '<tt>'
    def __endTitle(self):
        return '</tt>'
    def __TitleImage(self,MType):
        return '<img src="css/img/MType/%s.png" title="" alt="" />'%MType
    def __createTitle(self,Title,MType):
        self.__expand(self.__startTitle())
        if self.__verify(MType) == True: self.__expand(self.__TitleImage(MType))
        self.__expand(Title)
        self.__expand(self.__endTitle())


##Description
    def __startDescription(self):
        return '<p>'
    def __endDescription(self):
        return '</p>'
    def __createDescription(self,Description):
        self.__expand(self.__startDescription())
        self.__expand(Description)
        self.__expand(self.__endDescription())


##Buttons
    def __startButton(self,mode):
        self.ButtonNummer+=1
        if self.ButtonNummer > 1:
            space='&nbsp;'
        else:
            space=''
        if mode == 0:
            return '%s<a'%space
        else:
            return '>'
    def __endButton(self):
        return '</a>'
    def __ButtonLink(self,link):
        return ' href="%s"'%link
    def __ButtonTitle(self,title):
        return ' title="%s"'%title
    def __createButton(self,link,title,text):
        if title=='': title=text
        self.__expand(self.__startButton(0))
        self.__expand(self.__ButtonLink(link))
        self.__expand(self.__ButtonTitle(title))
        self.__expand(self.__startButton(1))
        self.__expand(text)
        self.__expand(self.__endButton())


##Paragraph
    def __startParagraph(self):
        self.__expand('<p>')
    def __endParagraph(self):
        self.__expand('</p>')


##Öffentliche Funktion
    def rtn(self):
        return self.TextString

#+++++++++++++++++++++HTML-Absatz (paragraph)+++++++++++++++++++
class paragraph():
    def __init__(self,cnt):
        self.TextString=''
        self.Insert=cnt
        self.__createParagraph()

    def __expand(self,string):
        self.TextString+=string

    def __createParagraph(self):
        self.__expand(self.__openParagraph())
        self.__expand(self.__fillContent())
        self.__expand(self.__closeParagraph())
    def __openParagraph(self):
        return '<p>'
    def __closeParagraph(self):
        return '</p>'

    def __fillContent(self):
        return str(self.Insert)

    def rtn(self):
        return self.TextString

#+++++++++++++++++++++HTML-h2-Überschrift (headline)+++++++++++++++++++
class headline():
    def __init__(self,cnt):
        self.TextString=''
        self.Insert=cnt
        self.__createHeadline()

    def __expand(self,string):
        self.TextString+=string

    def __createHeadline(self):
        self.__expand(self.__openHeadline())
        self.__expand(self.__fillContent())
        self.__expand(self.__closeHeadline())
    def __openHeadline(self):
        return '<h2>'
    def __closeHeadline(self):
        return '</h2>'

    def __fillContent(self):
        return str(self.Insert)

    def rtn(self):
        return self.TextString
#+++++++++++++++++++++Link-Box (shortcut)+++++++++++++++++++
class shortcut():
    def __init__(self,Title,Link,Icon='',Text=''):
        self.TextString=''
        self.ButtonNummer=0
        self.Link=Link
        self.Title=Title
        if Icon=='' and not Text=='':
            self.Text=Text
            self.__TextLink()
        elif Text=='' and not Icon=='':
            self.Icon=Icon
            self.__ImageLink()
        elif Text=='' and Icon=='':
            self.Text=Title
            self.__TextLink()
        else:
            self.Icon=Icon
            self.__ImageLink()
    def __expand(self,string):
        self.TextString+=string

    def __ImageLink(self):
        self.__expand(self.__openLink(0))
        self.__expand(self.__linkHref())
        self.__expand(self.__linkTitle())
        self.__expand(self.__linkClass())
        self.__expand(self.__openLink(1))
        self.__Image()
        self.__expand(self.__endLink())
    def __linkClass(self):
        return ' class="button"'
    def __openLink(self,mode):
        self.ButtonNummer+=1
        if self.ButtonNummer > 1:
            space='&nbsp;'
        else:
            space=''
        if mode == 0:
            return '%s<a'%space
        else:
            return '>'
    def __linkHref(self):
        return ' href="%s"'%self.Link
    def __linkTitle(self):
        return ' title="%s"'%self.Title
    def __endLink(self):
        return '</a>'

    def __Image(self):
        self.__expand(self.__openImage())
        self.__expand(self.__imageSrc())
        self.__expand(self.__imageAlt())
        self.__expand(self.__imageTitle())
        self.__expand(self.__endImage())
    def __openImage(self):
        return '<img'
    def __endImage(self):
        return ' />'
    def __imageSrc(self):
        return ' src="%s/%s"'%('./img',self.Icon)
    def __imageAlt(self):
        return ' alt="%s"'%self.Title
    def __imageTitle(self):
        return ' title="%s"'%self.Title

    def __TextLink(self):
        self.__expand(self.__openLink(0))
        self.__expand(self.__linkHref())
        self.__expand(self.__linkTitle())
        self.__expand(self.__linkClass())
        self.__expand(self.__openLink(1))
        self.__expand(self.Text)
        self.__expand(self.__endLink())

    def rtn(self):
        return self.TextString

#+++++++++++++++++++++Formular (form)+++++++++++++++++++
class form():
    def __init__(self,Titel,Datei,Save=''):
        self.TextString=''
        self.Title=Titel
        self.Action=Datei
        if Save==1:
            self.Method='post'
        else:
            self.Method='get'
        self.__createFieldset()
        self.__createForm()
    def __expand(self,string):
        self.TextString+=string

    def __createFieldset(self):
        self.__expand(self.__openFieldset())
        self.__expand(self.__openLegend())
        self.__expand(self.Title)
        self.__expand(self.__endLegend())
    def __openFieldset(self):
        return '<fieldset>'
    def __finishFieldset(self):
        self.__expand('</fieldset>')
    def __openLegend(self):
        return '<legend>'
    def __endLegend(self):
        return '</legend>'

    def __createForm(self):
        self.__expand(self.__openForm(0))
        self.__expand(self.__action())
        self.__expand(self.__method())
        self.__expand(self.__openForm(1))
    def __openForm(self,mode):
        if mode==0:
            return '<form'
        else:
            return '>'
    def __action(self):
        return ' action="%s"'%self.Action
    def __method(self):
        return ' method="%s"'%self.Method
    def __endForm(self):
        self.__expand('</form>')

    def open_paragraph(self):
        self.__expand('<p>')
    def add_Entry(self,ElementName,Beschriftung,Wert=''):
        self.__expand('<label for="%s">%s</label>'%(ElementName,Beschriftung))
        self.__expand('<input type="text" name="%s" value="%s" />'%(ElementName,Wert))
    def add_Hidden(self,ElementName,Wert):
        self.__expand('<input type="hidden" name="%s" value="%s" />'%(ElementName,Wert))
    def add_Button(self,Beschriftung,ElementName='',Wert=''):
        if not ElementName=='' and not Wert=='':
            self.__expand('<button type="submit" name="'+str(ElementName)+'" value="'+str(Wert)+'">'+str(Beschriftung)+'</button>')
        else:
            self.__expand('<button type="submit">'+str(Beschriftung)+'</button>')
    def add_List(self,ElementName):
        self.__expand('<select name="'+str(ElementName)+'">')
    def add_List_Element(self,Wert):
        self.__expand('<option>%s</option>'%Wert)
    def refresh_List(self):
        self.__expand('</select>')
    def end_paragraph(self):
        self.__expand('</p>')
    def rtn(self):
        self.__endForm()
        self.__finishFieldset()
        return self.TextString

#+++++ HTML_H1-Headline (opthead)+++++

class opthead():
    def __init__(self,cnt):
        self.TextString=''
        self.Insert=cnt
        self.__createHeadline()

    def __expand(self,string):
        self.TextString+=string

    def __createHeadline(self):
        self.__expand(self.__openHeadline())
        self.__expand(self.__fillContent())
        self.__expand(self.__closeHeadline())
    def __openHeadline(self):
        return '<h1>'
    def __closeHeadline(self):
        return '</h1>'

    def __fillContent(self):
        return str(self.Insert)

    def rtn(self):
        return self.TextString

#+++++ Link erstellen(link)+++++
class link():
    def __init__(self,Datei,Text,Titel=''):
        self.TextString = ''
        self.Href = ''
        self.time = 0
        if Datei[(len(Datei)-3):len(Datei)] == '.py':
            self.Datei = Datei[0:(len(Datei)-3)]
        else:
            self.Datei = Datei
        self.Text = Text
        self.Titel = Titel
        self.__createHref()
    def __expand(self,string):
        self.TextString += string
    def __write(self,string):
        self.Href += string

    def __createHref(self):
		if (self.Datei.find('=') == -1):
			self.__write(Base)
			self.add_param(Name='mn',Wert=self.Datei)
		elif (self.Datei[0:4] == 'main'):
			self.__write(self.Datei[5:len(self.Datei)]+'.py')
		elif (self.Datei[0:5] == 'other'):
			self.__write(self.Datei[6:len(self.Datei)])
    def __createLink(self):
        self.__expand(self.__openLink() + self.__add_LinkText() + self.__endLink())
    def __openLink(self):
        return '<a href="'+self.Href+'" title="'+self.Titel+'">'
    def __add_LinkText(self):
        return self.Text
    def __endLink(self):
        return '</a>'

    def add_param(self,Name,Wert):
        self.time += 1
        if (self.time == 1):
            self.__write('?')
        else:
            self.__write('&')
        self.__write(Name)
        self.__write('=')
        self.__write(Wert)
    def rtn(self):
        self.__createLink()
        return self.TextString

#Seperator
class seperator():
    def __init__(self):
        self.sep = '&middot;'
    def __sep(self):
        return ' '
    def rtn(self):
        sep = ''
        sep += self.__sep()
        sep += self.sep
        sep += self.__sep()
        return sep

#Bilder (image)
class image():
    def __init__(self,Datei,Alternativ='',Titel=''):
        self.Datei = Datei
        self.Alt = Alternativ
        self.Titel = Titel
        self.Pfad = img_pfad
        self.TextString = ''
        self.__createPic()
    def __expand(self,string):
        self.TextString += string

    def __createPic(self):
        self.__expand(self.__openIMG())
        self.__expand(self.__sep())
        self.__expand(self.__imgSRC())
        self.__expand(self.__sep())
        self.__expand(self.__imgALT())
        self.__expand(self.__sep())
        self.__expand(self.__imgTITLE())
        self.__expand(self.__sep())
        self.__expand(self.__closeIMG())
    def __sep(self):
        return ' '
    def __openIMG(self):
        return '<img'
    def __imgSRC(self):
        return 'src="%s/%s"'%(self.Pfad,self.Datei)
    def __imgALT(self):
        return 'alt="%s"'%self.Alt
    def __imgTITLE(self):
        return 'title="%s"'%self.Titel
    def __closeIMG(self):
        return '/>'

    def rtn(self):
        return self.TextString