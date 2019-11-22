class UnitTestExport(object):
    id = None
    kontext_id = None
    poradie = None
    funkcia = None
    status = None
    autor = None
    datum_zmeny = None


class SlovoExport(object):
    id = None
    zak_tvar = None
    tvar = None
    rod = None
    podrod = None
    pad = None
    stupen = None
    sposob = None
    osoba = None
    cas = None
    pricastie = None
    cislo = None
    je_negacia = None
    je_neurcitok = None
    je_prechodnik = None
    zvratnost = None
    sd_id = None
    slovny_druh = None
    zoznam_padov = None
    popis = None
    anotacia = None

    def daj_popis(self):
        return "{slovny_druh} Pád: {pad} Číslo: {cislo} Osoba:{osoba}".format(slovny_druh=self.slovny_druh,
                                                                              pad=self.pad,
                                                                              cislo=self.cislo,
                                                                              osoba=self.osoba)


class SlovnyDruhExport(object):
    id = None
    zak_tvar = None
    druh = None


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
    zak_tvar = None
    neprekl_vyraz = None
    je_cislo = False
    bolo_vybrate = False
    cely_popis_slova = None
    anotacia = None

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


class RozvijajuceSlovo(object):
    index = 0
    slovo = None
    sid = None
    sd_id = None

    def __str__(self):
        return "RozvijajuceSlovo -{0}".format(self.slovo)


class RozvitelneSlovo(object):
    tvar = None
    index = None
    index_pociatku_rozvoja = None
    rozvijajuce_privlastky = []
    rozvijajuce_slova = []
    priradit_k = None
    je_podmet = None
    je_zo_slovesa = False
    otec = None
    sid = None
    sd_id = None

    def __str__(self):
        v = "[ RozvijatelneSlovo -{0}".format(self.tvar)

        v += "ZPrivlastkyZ:"

        for priv in self.rozvijajuce_privlastky:
            v += str(priv)

        v += "KPrivlastkyK"

        v += "ZPredmetyZ:"

        for pred in self.rozvijajuce_predmety:
            v += str(pred)

        v += "KPredmetyK"

        v += " ]"
        return v


class ObohatenaVeta(object):
    slova = []
    podmety = []
    prisudky = []
    strom_vety = []

    def __str__(self):
        v = "Slova:"

        index = 0
        for s in self.slova:
            v += str(index)+":"+s.tvar
            index += 1

        v += " Podmety:"

        for p in self.podmety:
            v += str(p) + ":" + self.slova[p].tvar

        v += " Prisudky:"

        for p in self.prisudky:
            v += str(p) + ":" + self.slova[p].tvar

        v += " Ostatne slova:"

        for p in self.strom_vety:
            v += str(p)

        return v

