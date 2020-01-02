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


class MorfoFilter(object):
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

    koren = None
    prefix = None
    sufix = None
    vzor = None
    vzor_stup = None
    paradigma = None
    sd_id = None

