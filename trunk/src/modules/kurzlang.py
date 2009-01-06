def mach_lang(nr_kurz):
    if int(nr_kurz)<10**9:
        return str(10**9+int(nr_kurz))
    else:
        raise ValueError,"Ungueltige Nummer!"
def mach_kurz(nr_lang):
    if int(nr_lang)>10**9:
        return str(int(nr_lang)-(10**9))
    else:
        raise ValueError,"Ungueltige Nummer!"