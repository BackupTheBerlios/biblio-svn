# -*- coding: cp1252 -*-
import Tkinter as tk
import simplewinprint as druck
class Main():
    '''Druckfunktion für Bibliothekscodes.
    Funktionen:
        __init__()
        PrintCodes(Codes)
    '''
    def __init__(self):
        '''__init__():
            Initialisiert den Drucker'''
        self.printer = druck.Printer("Default", 100, 400, 800, 800, 800)
        self.printer.default_font_name = "IDAutomationHC39M"
        self.printer.default_font_size =14.5

    def PrintCodes(self,Codes):
        '''
        PrintCodes(Codes)
            Codes müssen in folgender Form übergeben werden:
            ((ID,Buchtitel)[,(ID,Buchtitel)[,...]])
        '''
        Lines=[]
        BuchtitelZeile=''
        BarcodeZeile=''
        for Index in range(len(Codes)):
            Buchtitel=''
            for i in range(12):
                try: Buchtitel+=Codes[Index][1][i]
                except: Buchtitel+=' '
            BuchtitelZeile+=Buchtitel
            BarcodeZeile+='*'+str(Codes[Index][0])+'*'
            if (Index+1)%5==0:
                Lines.append((BuchtitelZeile,BarcodeZeile))
                BuchtitelZeile=''
                BarcodeZeile=''
            else:
                BuchtitelZeile+=' '
                BarcodeZeile+=' '
        if len(Codes)%5!=0: Lines.append((BuchtitelZeile,BarcodeZeile))
        self.printer.startdoc()
        for Line in Lines:
            self.printer.print_textblock(
               text = Line[0],
               font_weight = 700,
               font_name = "Courier New")
            self.printer.print_textblock(
               text = Line[1],
               font_weight = 700,
               font_size=30,
               font_name = "IDAutomationHC39M")
            if (Lines.index(Line)+1)%14!=0:
                self.printer.print_textblock(
                    text = '   ',
                    font_weight = 700,
                    font_size=12,
                    font_name = "IDAutomationHC39M")
        self.printer.print_textblock()
        self.printer.enddoc()

if __name__ == "__main__":
    klasse=Main()
    bla=[("1000018933","Titel"),("1000018933","zu langer Titel"),("1000018933","blablablabla"),("1000018933","bla"),("1000018933","bla")]
    liste=[]
    for i in range(15): liste.extend(bla)
    liste.append(("1000018933","Titel"))
    klasse.PrintCodes(liste)

