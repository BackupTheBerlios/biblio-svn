#!/usr/bin/env python 
# -*- coding: iso-8859-1 -*- 

""" 
*************************************************************************** 
* Description:  Vereinfacht das Drucken unter Windows durch Kapselung 
*               der wichtigsten Funktionen der Windows-API. 
*                
*               Ermöglicht einfache Ausdrucke auf in Windows installierte 
*               Drucker. Bitmaps können auch ausgedruckt werden. 
* 
* Created:      2005-04-22 by Gerold 
* 
* Requirements: Python 2.4:  http://www.python.org/ 
*               pywin32:     http://sourceforge.net/projects/pywin32/ 
* 
* Beispiel: 
*   import simplewinprint 
*   text = self.ergebnis 
        p = simplewinprint.Printer("Default", 100, 800, 800, 800, 800) 
        p.default_font_name = "Arial" 
        p.default_font_size = 12
        p.startdoc() 
        p.print_textblock( 
           text = "Liste aus der Datenbank", 
           font_size = 16, 
           font_weight = 700, 
           lineheight_percent = 150 
        )
        p.print_textblock()
        p.print_textblock(text = 'Hallo')    
        p.enddoc()
        
*************************************************************************** 
""" 


#********************************************* 
# Konstanten fuer GetDeviceCaps 
#********************************************* 
# HORZRES / VERTRES = printable area 
HORZRES = 8 
VERTRES = 10 

# LOGPIXELS = dots per inch 
LOGPIXELSX = 88 
LOGPIXELSY = 90 

# PHYSICALWIDTH/HEIGHT = total area 
PHYSICALWIDTH = 110 
PHYSICALHEIGHT = 111 

# PHYSICALOFFSETX/Y = left / top margin 
PHYSICALOFFSETX = 112 
PHYSICALOFFSETY = 113 


#---------------------------------------------------------------------- 
class Printer(object): 
   """ 
   Diese Klasse stellt das Drucker-Objekt dar und kümmert sich darum, 
   dass die übergebenen Daten korrekt ausgedruckt werden. 
   """ 
    

   #---------------------------------------------------------------------- 
   def twips2pixels( 
      self, 
      twips, 
      horizontal = True, 
   ): 
      """ 
      Konvertiert Twips in Pixel 
      twips:      
         Zu konvertierende Twips 
      horizontal: 
         Gibt an, ob es sich um horizontale Twips handelt. 
            True = horizontal 
            False = vertikal 
      """ 
      
      nTwipsPerInch = 1440 
      
      if horizontal: 
         pixels_per_inch = self.pixels_per_inch_x 
      else: 
         pixels_per_inch = self.pixels_per_inch_y 
      
      return (twips / nTwipsPerInch) * pixels_per_inch 


   #---------------------------------------------------------------------- 
   def pixels2twips( 
      self, 
      pixels, 
      horizontal = True, 
   ): 
      """ 
      Konvertiert Pixel in Twips 
      pixels: 
         Zu konvertierende Pixel 
      horizontal: 
         Gibt an, ob es sich um horizontale Pixel handelt. 
            True = horizontal 
            False = vertikal 
      """ 

      nTwipsPerInch = 1440.0 
      
      if horizontal: 
         pixels_per_inch = self.pixels_per_inch_x 
      else: 
         pixels_per_inch = self.pixels_per_inch_y 
      
      return float(pixels) / pixels_per_inch * nTwipsPerInch 


   #---------------------------------------------------------------------- 
   def __init__( 
      self, 
      printer_name = "Default", 
      lineheight_percent = 100, 
      margin_left = 800, 
      margin_top = 800, 
      margin_right = 800, 
      margin_bottom = 800, 
      document_name = "SimpleWinPrint" 
   ): 
      """ 
      Initialisiert die Klasse "Printer". Dabei werden die 
      Einstellungen (Rand, Druckbereich,...) herausgefunden. 
      printer_name: 
         Wenn "Default", dann wird der Standarddrucker verwendet. Ansonsten 
         wird der übergebene Drucker(name) verwendet. 
      lineheight_percent: 
         Zeilenhöhe in Prozent in Bezug zur Schrifthöhe. 
      margin_xxx: 
         Rand links, oben, rechts und unten in Twips. 
      document_name: 
         Name, mit dem der Druckjob im Spooler angelegt wird. 
      """ 
      
      import win32ui 
      import time 
      import win32print 
      import win32con 

      # Zeilenhoehe in Prozent 
      self.lineheight_percent = float(lineheight_percent) 
      self._lineheight_twips = 0 
      
      # Dokumentname 
      self.document_name = document_name 
      
      # Rand 
      self.margin_left = margin_left 
      self.margin_top = margin_top 
      self.margin_right = margin_right 
      self.margin_bottom = margin_bottom 
      
      # vpos = aktuelle Zeile = vertikale Position von oben als negative Zahl 
      # Wird mit None initialisiert 
      self.vpos = None 
      
      # hpos = Aktuelle Position von Links 
      self.hpos = self.margin_left 
      
      # Standardschrift festlegen 
      self.default_font_name = "" 
      self.default_font_size = 0 
      self.default_font_weight = 0 
      
      # Wurde der Druck abgebrochen? 
      self.canceled = False 
      
      # Gerätekontext holen und Einheit auf TWIPS einstellen 
      self.hdc = win32ui.CreateDC() 
      if printer_name == "Default": 
         self.hdc.CreatePrinterDC(win32print.GetDefaultPrinter()) 
      else: 
         self.hdc.CreatePrinterDC(printer_name) 
      self.hdc.SetMapMode(win32con.MM_TWIPS) 
          
      # Pixel pro Zoll herausfinden 
      # Wird später zur Umrechnung von Pixel in Twips benötigt 
      self.pixels_per_inch_x = float(self.hdc.GetDeviceCaps(LOGPIXELSX)) 
      self.pixels_per_inch_y = float(self.hdc.GetDeviceCaps(LOGPIXELSY)) 
      
      # Bedruckbarer Bereich in Pixel 
      self.printable_area = [ 
         self.hdc.GetDeviceCaps(HORZRES), 
         self.hdc.GetDeviceCaps(VERTRES) 
      ] 
      self.printable_area[0] = self.pixels2twips(self.printable_area[0], True) 
      self.printable_area[1] = self.pixels2twips(self.printable_area[1], False) 

      # Physikalische Breite und Höhe der Seite in Pixel 
      self.printer_size = [ 
         self.hdc.GetDeviceCaps(PHYSICALWIDTH), 
         self.hdc.GetDeviceCaps(PHYSICALHEIGHT) 
      ] 
      self.printer_size[0] = self.pixels2twips(self.printer_size[0], True) 
      self.printer_size[1] = self.pixels2twips(self.printer_size[1], False) 

      # Rand in Pixel 
      self.printer_margins = [ 
         self.hdc.GetDeviceCaps(PHYSICALOFFSETX), 
         self.hdc.GetDeviceCaps(PHYSICALOFFSETY) 
      ] 
      self.printer_margins[0] = self.pixels2twips(self.printer_margins[0], True) 
      self.printer_margins[1] = self.pixels2twips(self.printer_margins[1], False) 

    
   #---------------------------------------------------------------------- 
   def __del__(self): 
      """ 
      Destruktor 
      """ 
      
      try: 
         self.hdc.AbortDoc() 
      except: 
         pass 


   #---------------------------------------------------------------------- 
   def startdoc(self): 
      """ 
      Versetzt den Druckerspooler in den Bereitschaftsmodus und 
      startet eine neue Seite. 
      """ 
      
      import time 

      new_docname = "%s %s" % ( 
         self.document_name, 
         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
      ) 
      
      self.hdc.StartDoc(new_docname) 
      self.hdc.StartPage () 


   #---------------------------------------------------------------------- 
   def nextpage(self): 
      """ 
      Erzwingt eine neue Seite 
      """ 
      
      self.hdc.EndPage () 
      self.hdc.StartPage () 
      self.vpos = None 


   #---------------------------------------------------------------------- 
   def print_textblock( 
      self, 
      text = "", 
      align_str = "left", 
      break_long_lines = 'words', 
      on_linebreak_lstrip = True, 
      font_name = "", 
      font_size = 0, 
      font_weight = 0, 
      font_italic = False, 
      font_underline = False, 
      hpos = None, 
      vpos = None, 
      lineheight_percent = None 
   ): 
      """ 
      Schreibt einen Textblock. Dieser kann auch aus mehreren Zeilen bestehen. 
      Zeilenumbrüche (\n) im Text werden umgebrochen. 
      Unterstützt auch das automatische Umbrechen von zu langem Text 
      in mehrere Zeilen. Dabei kann unterschieden werden, 
      ob der Text bei jedem Zeichen oder bei Wörtern umgebrochen wird. 
      text: 
         Zu schreibender Text 
      align_str: 
         Textausrichtung als String: 
            'left' 
            'right' 
      break_long_lines: 
         Gibt an, ob der Text automatisch am Zeilenende umgebrochen werden soll. 
            'no': Kein automatischer Zeilenumbruch 
            'words': Umbruch nur nach einem Wort 
            'chars': Umbruch nach jedem Zeichen 
      on_linebreak_lstrip: 
         Wenn True, dann werden nach einem automatischen Zeilenumbruch, die 
         Leerzeichen der nächsten Zeile mit "lstrip()" entfernt. 
      font_name: 
         Name der zu verwendenden Schrift 
      font_size: 
         Schriftgröße der zu verwendenden Schrift 
      font_weight: 
         Schriftgewichtung (Fett) der zu verwendenden Schrift 
            FW_DONTCARE 0         FW_SEMIBOLD 600 
            FW_THIN 100           FW_DEMIBOLD 600 
            FW_EXTRALIGHT 200     FW_BOLD 700 
            FW_ULTRALIGHT 200     FW_EXTRABOLD 800 
            FW_LIGHT 300          FW_ULTRABOLD 800 
            FW_NORMAL 400         FW_HEAVY 900 
            FW_REGULAR 400        FW_BLACK 900 
            FW_MEDIUM 500 
      font_italic: 
         Wenn True, dann wird die Schrift kursiv gedruckt 
      font_underline: 
         Wenn True, dann wird die Schrift unterstrichen gedruckt 
      hpos: 
         Überschreibt die horizontale Druckposition in Twips 
      vpos: 
         Überschreibt die vertikale Druckposition in Twips 
      lineheight_percent: 
         Überschreibt für die aktuelle Zeile die Zeilenhöhe in Prozent 
      """ 
      
      import win32ui 
      import win32con 
      import textwrap 
      
      # Leerzeile drucken ->> "" durch " " ersetzen 
      if (text is None) or (text == ""): 
         text = " " 
          
      # Schrift 
      if not(font_weight): 
         font_weight = self.default_font_weight 
      font_dict = { 
         "weight": font_weight 
      } 
      if font_name: 
         font_dict["name"] = font_name 
      else: 
         if self.default_font_name: 
            font_dict["name"] = self.default_font_name 
      if font_size: 
         font_dict["height"] = int( 
            self.pixels2twips( 
               (font_size * self.pixels_per_inch_y), False 
            ) / 72 * -1 
         ) 
      else: 
         if self.default_font_size: 
            font_dict["height"] = int( 
               self.pixels2twips( 
                  (self.default_font_size * self.pixels_per_inch_y), False 
               ) / 72 * -1 
            ) 
      if font_italic: 
         font_dict["italic"] = True 
      if font_underline: 
         font_dict["underline"] = True 
      font_object = win32ui.CreateFont(font_dict) 
      self.hdc.SelectObject(font_object) 
      
      # Zeilenhöhe errechnen 
      if lineheight_percent is None: 
         lineheight_percent = self.lineheight_percent 
      self._lineheight_twips = int( 
         float(self.hdc.GetTextMetrics()["tmHeight"]) \
         / 100.0 * lineheight_percent 
      ) + 1
      # Rand Links 
      if hpos is None: 
         self.hpos = self.margin_left 
      else: 
         self.hpos = hpos 
      
      # Zeile in druckbare Bereiche aufteilen 
      if len(text) > 1: 

         max_width_twips = self.printable_area[0] - self.hpos - self.margin_right 
         new_line = "" 
         textlist = [] 

         if break_long_lines == "chars": 
            # Zeilenumbruch bei jedem Zeichen 

            enforced_linebreak = False 
            for item in text: 
               new_line += item 
                
               if on_linebreak_lstrip and enforced_linebreak: 
                  new_line = new_line.lstrip() 

               if item == "\n": 
                  textlist.append(new_line[:-1]) 
                  new_line = item 
                  enforced_linebreak = False 
               else: 
                  if self.hdc.GetTextExtent(new_line)[0] > max_width_twips: 
                     textlist.append(new_line[:-1]) 
                     new_line = item 
                     enforced_linebreak = True 
                
            if len(new_line) > 0: 
               textlist.append(new_line) 
                
         elif break_long_lines == "words": 
            # Zeilenumbruch nach Wörtern 
            
            slice_begin = 0 
            korrektur = 0 
            enforced_linebreak = False 
            for i in xrange(len(text) * 3): 
               slice_end = i + korrektur 
               new_line = text[slice_begin:slice_end] 

               if new_line.endswith("\n"): 
                  textlist.append(new_line[:-1].replace("\r", "")) 
                  if on_linebreak_lstrip and enforced_linebreak: 
                     textlist[-1] = textlist[-1].lstrip() 
                  slice_begin = slice_begin + len(new_line) 
                  korrektur = slice_begin - i 
                  enforced_linebreak = False 
               else: 
                  if self.hdc.GetTextExtent(new_line)[0] >= max_width_twips: 
                     slice_end -= 1 
                     new_line = text[slice_begin:slice_end + 100] 
                     new_line = textwrap.wrap(new_line, slice_end - slice_begin)[0] 
                     textlist.append(new_line) 
                     if on_linebreak_lstrip and enforced_linebreak: 
                        textlist[-1] = textlist[-1].lstrip() 
                        
                     slice_begin = slice_begin + len(new_line) 
                     korrektur = slice_begin - i 
                     enforced_linebreak = True 
                  
                  if slice_begin >= len(text): 
                     break 
                
            if len(new_line) > 0: 
               textlist.append(new_line) 
               if on_linebreak_lstrip and enforced_linebreak: 
                  textlist[-1] = textlist[-1].lstrip() 
            
         else: 
            textlist = [text] 

      else: 
         textlist = [text] 
      
      # Jeden Eintrag der Textliste durchlaufen 
      for item in textlist: 
      
         # Neue Zeilenposition setzen (wichtig für neue Seitenanfänge) 
         #------------------------------------------------------------ 
         def __new_rowpos_first(vpos): 
            if vpos is None: 
               if self.vpos is None: 
                  self.vpos = self.margin_top * -1 
            else: 
               if vpos > 0: 
                  self.vpos = vpos * -1 
               else: 
                  self.vpos = vpos 
         __new_rowpos_first(vpos) 
          
         # Seitenumbruch 
         max_height_twips = self.printable_area[1] - self.margin_bottom 
         if (self.vpos * -1) >= max_height_twips: 
            self.nextpage() 
            __new_rowpos_first(vpos) 

         # Ausrichtung 
         if align_str == "right": 
            align = win32con.DT_RIGHT 
            hpos_real = self.printable_area[0] - self.hpos 
            if on_linebreak_lstrip: 
               item = item.rstrip() 
         else: 
            align = win32con.DT_LEFT 
            hpos_real = self.hpos 
         self.hdc.SetTextAlign(align) 
          
         # Zeile drucken 
         self.hdc.TextOut( 
            int(hpos_real), 
            int(self.vpos), 
            item 
         ) 
          
         # Neue Zeilenposition setzen (nur wenn bereits gesetzt) 
         if vpos is None: 
            self.vpos -= self._lineheight_twips 
         else: 
            if vpos > 0: 
               self.vpos = vpos * -1 
            else: 
               self.vpos = vpos 


   #---------------------------------------------------------------------- 
   def print_rawtext( 
      self, 
      text = "", 
      font_name = None, 
      hpos = None, 
      vpos = None, 
      auto_pagebreak = False 
   ): 
      """ 
      Diese Funktion ist dafür geeignet, einem Drucker 
      (z.B. Bondrucker) Steuercodes und reinen Text zu schicken. 
      Die Schriftgroesse kann nicht umgestellt werden. 
      Rufen Sie vorher die Funktion "startdoc" und nachher "enddoc" auf. 
      text: 
         Zu schreibender Text 
      font_name: 
         Schriftname 
      hpos: 
         Überschreibt die horizontale Druckposition in Twips 
      vpos: 
         Überschreibt die vertikale Druckposition in Twips 
      auto_pagebreak: 
         Wenn True, dann werden Seitenumbrüche automatisch durchgeführt 
      """ 
      
      import win32ui 
      import win32con 

      # Leerzeile drucken ->> "" durch " " ersetzen 
      if (text is None) or (text == ""): 
         text = " " 

      # Schrift 
      if not(font_name): 
         if self.default_font_name: 
            font_name = self.default_font_name 
      font_dict = { 
         "name": font_name, 
         "width": 0, 
         "height": 0, 
         "weight": 0, 
      } 
      font_object = win32ui.CreateFont(font_dict) 
      self.hdc.SelectObject(font_object) 

      # Zeilenhöhe in Twips errechnen 
      self._lineheight_twips = int( 
         self.hdc.GetTextMetrics()["tmHeight"] 
      ) + 1 
      
      # Umschalten in den reinen Textmodus 
      old_mode = self.hdc.SetMapMode(win32con.MM_TEXT) 
      
      # Zeilenhöhe im Textmodus herausfinden 
      lineheight_textmode = self.hdc.GetTextMetrics()["tmHeight"] 
      
      # Divident für Umrechnung der Zeilenhöhe ausrechnen 
      lineheight_divident = self._lineheight_twips / lineheight_textmode 

      # Rand Links 
      if hpos is None: 
         self.hpos = self.margin_left 
      else: 
         self.hpos = hpos 

      # Neue Zeilenposition setzen (wichtig für neue Seitenanfänge) 
      #------------------------------------------------------------ 
      def __new_rowpos_first(vpos): 
         if vpos is None: 
            if self.vpos == None: 
               self.vpos = self.margin_top * -1 
         else: 
            if vpos > 0: 
               self.vpos = vpos * -1 
            else: 
               self.vpos = vpos 
      __new_rowpos_first(vpos) 
      
      # Seitenumbruch 
      if auto_pagebreak: 
         max_height_twips = self.printable_area[1] - self.margin_bottom 
         if (self.vpos * -1) >= max_height_twips: 
            self.nextpage() 
            __new_rowpos_first(vpos) 

      # Zeile drucken 
      self.hdc.TextOut( 
         int(int(float(self.hpos) / float(lineheight_divident))), 
         int(int(float(self.vpos) / float(lineheight_divident))) * -1, 
         text 
      ) 

      # In den alten Modus umschalten 
      new_mode = self.hdc.SetMapMode(old_mode) 

      # Neue Zeilenposition setzen (nur wenn bereits gesetzt) 
      if vpos is None: 
         self.vpos -= self._lineheight_twips 
      else: 
         if vpos > 0: 
            self.vpos = vpos * -1 
         else: 
            self.vpos = vpos 


   #---------------------------------------------------------------------- 
   def print_bitmapfile( 
      self, 
      file_name, 
      hpos = None, 
      vpos = None, 
      padding_top = 0, 
      padding_left = 0, 
      padding_bottom = 0, 
      paramlist = [] 
   ): 
      """ 
      Druckt ein Bitmapfile an der aktuellen Zeilenposition aus. 
      file_name: 
         Name und Pfad des auszudruckenden Bitmaps. 
      hpos: 
         Überschreibt die horizontale Druckposition in Twips. 
      vpos: 
         Überschreibt die vertikale Druckposition in Twips. 
      padding_xxx: 
         Abstand des Bildes. 
      paramlist: 
         Wenn dieser Parameter übergeben wurde, dann werden 
         die anderen Parameter (ausgenommen file_name) mit dem Inhalt 
         dieser Liste überschrieben. 
         [hpos, vpos, padding_top, padding_left, padding_bottom] 
      """ 
      
      import win32gui 
      import win32con 
      import win32ui 

      # Parameterliste aufteilen 
      if paramlist: 
         hpos = paramlist[0] 
         if len(paramlist) >= 2: 
            if paramlist[1] is not None: 
               vpos = paramlist[1] 
         if len(paramlist) >= 3: 
            if paramlist[2] is not None: 
               padding_top = paramlist[2] 
         if len(paramlist) >= 4: 
            if paramlist[3] is not None: 
               padding_left = paramlist[3] 
         if len(paramlist) >= 5: 
            if paramlist[4] is not None: 
               padding_bottom = paramlist[4] 

      # Bild laden 
      img = win32gui.LoadImage( 
         0, 
         file_name, 
         win32con.IMAGE_BITMAP, 
         0, 
         0, 
         win32con.LR_LOADFROMFILE 
      ) 
      
      # Zum Drucker kompatiblen DC für das Bild erstellen 
      mem_dc = self.hdc.CreateCompatibleDC() 
      
      # Skalierung ausrechnen 
      mem_dc_pixels_per_inch_x = float(mem_dc.GetDeviceCaps(LOGPIXELSX)) 
      mem_dc_pixels_per_inch_y = float(mem_dc.GetDeviceCaps(LOGPIXELSY)) 
      mem_dc_scale_x = self.pixels_per_inch_x / mem_dc_pixels_per_inch_x 
      mem_dc_scale_y = self.pixels_per_inch_x / mem_dc_pixels_per_inch_y 
      
      # Bitmap aus Handle erstellen und in DC holen 
      bmp = win32ui.CreateBitmapFromHandle(img) 
      mem_dc.SelectObject(bmp) 
      
      # Größe des Bildes in Pixel 
      x, y = bmp.GetSize() 

      if not(hpos is None): 
         self.hpos = hpos 

      # Neue Zeilenposition setzen (wichtig für neue Seitenanfänge) 
      if vpos is None: 
         if self.vpos is None: 
            self.vpos = int(self.margin_top) * -1 
      else: 
         if vpos > 0: 
            self.vpos = vpos * -1 
         else: 
            self.vpos = vpos 
      
      # Bild in den Drucker-DC kopieren und dabei skalieren 
      self.hdc.StretchBlt( 
         ( 
            int(self.hpos + padding_left), 
            int(self.vpos - padding_top) 
         ), 
         ( 
            int(self.pixels2twips(float(x), True) * mem_dc_scale_x), 
            int(self.pixels2twips(float(y), False) * mem_dc_scale_y) * -1 
         ), 
         mem_dc, 
         (0, 0), 
         (x, y), 
         win32con.SRCCOPY 
      ) 

      # Neue Zeilenposition setzen 
      self.vpos -= int( 
         (self.pixels2twips(float(y), False) * mem_dc_scale_y) + padding_top + padding_bottom + 10 # 10 ist nur geschätzt 
      ) 


   #---------------------------------------------------------------------- 
   def abortdoc(self): 
      """ 
      Bricht den Druckauftrag ab. 
      """ 
      self.canceled = True 
      self.hdc.AbortDoc() 


   #---------------------------------------------------------------------- 
   def enddoc(self): 
      """ 
      Schliesst den Druckauftrag ab. 
      Der Druckauftrag wird jetzt ausgedruckt. 
      """ 
      
      if self.canceled: 
         try: 
            self.hdc.AportDoc() 
         except: 
            pass 
      else: 
         self.hdc.EndPage () 
         self.hdc.EndDoc () 
