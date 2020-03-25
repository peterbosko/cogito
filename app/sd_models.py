class SDExport(object):
    id = None
    zak_tvar = None
    popis = None
    typ = None
    rod = None
    podrod = None
    cislo = None
    je_privlastnovacie = None
    zvratnost = None
    je_negacia = None
    hodnota = None
    pady = None
    pricastie = None
    sloveso_id = None
    sloveso_tvar = None
    pocitatelnost = None
    sem_priznak_id = None
    vzor = None
    koren = None
    prefix = None
    sufix = None
    vzor_stup = None
    paradigma = None
    koncept_id = None
    koncept_nazov = None

    tab = None

    slova = []

    zmazaneSlova = []


class SemStrom(object):
    id = None
    parent = None
    text = None
    sem_priznak_id = None


class VzorExport(object):
    id = None
    typ = None
    vzor = None
    rod = None
    podrod = None
    deklinacia = None
    alternacia = None
    sklon_stup = None
    popis = None


class PrefixSufixExport(object):
    id = None
    typ = None
    prefix_sufix = None
    hodnota = None


class SlovoFilterExport(object):
    tvar = None
    rod = None
    podrod = None
    pad = None
    cislo = None
    osoba = None
    cas = None
    sposob = None
    stupen = None
    pricastie = None
    anotacia = None
    pricastie_sufix = None
    pricastie_sufix_m = None
    pricastie_sufix_t = None
    koren_slovesa = None

    koren = None
    pzkmen = None
    prefix = None
    sufix = None
    vzor = None
    vzor_stup = None
    paradigma = None
    sd_id = None
    vid = None

    afirmacia = None

    deklin1 = None
    deklin2 = None
    deklin3 = None
    deklin4 = None
    deklin5 = None
    deklin6 = None
    deklin7 = None

    co_generovat = None


class VzorSoStatistikou(object):
    vzor = None
    hodnota = None
    popis = None
    pocet = None


class DotiahniVzor(object):
    koren = None
    pzkmen = None
    vzor = None

