class KontrolaSlovResponse(object):
    data = ""
    uspesnost = 0


class SlovoVKontexte(object):
    id_slova = None
    popis = None
    je_v_slovniku = False
    je_viacej_v_slovniku = False
    slovo = None
    tvar = None
    tvar_lower = None
    zak_tvar = None
    neprekl_vyraz = None
    je_cislo = False
    bolo_vybrate = False
    cely_popis_slova = None
    anotacia = None
    je_prve_upper = None

    def __str__(self):
        return "***************************\n" + \
                "TVAR:"+str(self.tvar)+"|\n" + \
                "Id slova:"+str(self.id_slova)+"|\n" + \
                "popis:"+str(self.popis)+"|\n" + \
                "neprekl_vyraz:"+str(self.neprekl_vyraz)+"|\n" + \
                "bolo_vybrate:"+str(self.bolo_vybrate)+"|\n" + \
                "je_v_slovniku:"+str(self.je_v_slovniku)+"|\n" + \
                "je_viacej_v_slovniku:"+str(self.je_viacej_v_slovniku)+"|\n" + \
                "****************************"


class StromVety(object):
    id = None
    parent = None
    text = None


class Veta(object):
    text_celej_vety = None
    slova_vety = []
