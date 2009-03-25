def buch2lang(nr_kurz):
    if int(nr_kurz)<10**9:
        return str(10**9+int(nr_kurz))
    else:
        raise ValueError,"Ungueltige Nummer!"
def buch2kurz(nr_lang):
    if 2*10**9>int(nr_lang)>=10**9:
        return str(int(nr_lang)-(10**9))
    elif int(nr_lang)<10**9:
        return nr_lang
    else:
        raise ValueError,"Ungueltige Nummer!"
def sch2lang(nr_kurz):
    if int(nr_kurz)<10**9:
        return str(2*10**9+int(nr_kurz))
    else:
        raise ValueError,"Ungueltige Nummer!"
def sch2kurz(nr_lang):
    if 3*10**9>int(nr_lang)>=2*10**9:
        return str(int(nr_lang)-(2*10**9))
    elif int(nr_lang)<10**9:
        return nr_lang
    else:
        raise ValueError,"Ungueltige Nummer!"
def type2lang(nr_kurz):
    if int(nr_kurz)<10**9:
        return str(3*10**9+int(nr_kurz))
    else:
        raise ValueError,"Ungueltige Nummer!"
def type2kurz(nr_lang):
    if 4*10**9>int(nr_lang)>=3*10**9:
        return str(int(nr_lang)-(3*10**9))
    elif int(nr_lang)<10**9:
        return nr_lang
    else:
        raise ValueError,"Ungueltige Nummer!"
