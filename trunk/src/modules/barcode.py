# -*- coding: cp1252 -*-
import Tkinter as tk
#import random as ra
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
        index=0
        for Buch in Codes:
            Buchtitel=''
            for i in range(12):
                try:
                    Buchtitel+=Buch[1][i]
                except:
                    Buchtitel+=' '
            print Buchtitel
            BuchtitelZeile+=Buchtitel
            BarcodeZeile+='*'+Buch[0]+'*'
            index+=1
            if index==5:
                Lines.append((BuchtitelZeile,BarcodeZeile))
                index=0
                BuchtitelZeile=''
                BarcodeZeile=''
            else:
                BuchtitelZeile+=' '
                BarcodeZeile+=' '
        if len(Codes)/5.0>len(Codes)/5:
            Lines.append((BuchtitelZeile,BarcodeZeile))
        print Lines
        #'''
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
            self.printer.print_textblock(
                text = '   ',
                font_weight = 700,
                font_size=12,
                font_name = "IDAutomationHC39M")
        self.printer.print_textblock()
        self.printer.enddoc()

if __name__ == "__main__":
    klasse=Main()
    klasse.PrintCodes((("1000018933","Titel"),("1000018933","zu langer Titel"),
                       ("1000018933","blablablabla"),("1000018933","bla"),
                       ("1000018933","bla"),("1000018933","bla"),("1000018933","bla")))

