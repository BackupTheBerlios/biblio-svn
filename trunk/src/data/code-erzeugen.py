import Tkinter as tk
import simplewinprint as druck
class Main():
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Code")
        self.Buchname="Terra 5/6"
        self.Code="*1000018933*"
        self.Label=tk.Label(self.root, text=self.Code,
                            font=('IDAutomationHC39M',30))
        self.Label.pack()
        CodePrint(self.Buchname,self.Code)
        self.root.mainloop()

class CodePrint():
    def __init__(self,Buchname,Code):
        self.Buchname=Buchname
        self.Code=Code
        p = druck.Printer("Default", 100, 800, 800, 800, 800)
        p.default_font_name = "IDAutomationHC39M"
        p.default_font_size = 30
        p.startdoc()
        p.print_textblock(text=self.Buchname,
                          font_name = "Arial",
                          font_size = 10)
        p.print_textblock(
           text = self.Code,
           font_weight = 700,
           font_name = "IDAutomationHC39M",
           lineheight_percent = 150)
        p.enddoc()

Main()
