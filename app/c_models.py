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
