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
    tvar_lower = None
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
    sem_id = None
    sufix = None
    prefix = None
    vzor = None
    pocitatelnost = None

    def daj_popis(self):
        return "{slovny_druh} Pád: {pad} Číslo: {cislo} Osoba:{osoba}".format(slovny_druh=self.slovny_druh,
                                                                              pad=self.pad,
                                                                              cislo=self.cislo,
                                                                              osoba=self.osoba)


class SlovnyDruhExport(object):
    id = None
    zak_tvar = None
    druh = None
    koncept_id = None
    koncept_nazov = None


class SlovnyDruhHierExport(object):
    id = None
    sd_id = None
    parent_sd_id = None
    sd = None
    parent_sd = None


class slovo_data(object):
    data = []
    cisla = []

    def __init__(self):
        self.data = []
        self.cisla = []

