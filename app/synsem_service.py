from app.kt_service import *


def je_sloveso(slovo):
    if slovo.anotacia[0] == "V":
        return True
    return False


def je_indikativ(slovo):
    if slovo.anotacia[1] == "K":
        return True
    return False


def je_imperativ(slovo):
    if slovo.anotacia[1] == "M":
        return True
    return False


def je_lpar(slovo):
    if slovo.anotacia[1] == "L":
        return True
    return False


def je_tpar(slovo):
    if slovo.anotacia[0] == "G":
        return True
    return False


def je_infinitiv(slovo):
    if slovo.anotacia[1] == "I":
        return True
    return False


def je_byt(slovo):
    if slovo.anotacia[1] == "B":
        return True
    return False


def vrat_sloveso(slova):
    pred = True
    slova_pred = []
    slova_po = []
    sloveso = None
    predch_byt = False
    for s in slova:
        if je_sloveso(s) and \
                (je_indikativ(s) or je_imperativ(s) or je_lpar(s) or je_infinitiv(s)) and pred:
            sloveso = s
            pred = False
            ak = "akt"
        elif je_sloveso(s) and je_byt(s):
            predch_byt = True
        elif predch_byt and je_tpar(s):
            predch_byt = False
            sloveso = s
            pred = False
            ak = "pas"
        else:
            if pred:
                slova_pred.append(s)
            else:
                slova_po.append(s)

    return sloveso, slova_pred, slova_po, ak


def veta(data):
    slova = vrat_pole_slov_z_textu(data)

    strom_vety = veta("hl", slova)


def veta(mod, slova):
    sloveso, s_pred, s_po, ak = vrat_sloveso(slova)

    strom = {}

    return strom


def vrat_strom_vety(slova_vety):
    return veta("hl", slova_vety)

