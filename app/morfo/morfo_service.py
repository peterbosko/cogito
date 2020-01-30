from app.db_models import *
from sqlalchemy.sql.expression import func
from sqlalchemy import or_
from app.c_helper import *

# ----------------------------- SPOLOCNE METODY --------------------------------
# ----------------------------- SPOLOCNE METODY --------------------------------
# ----------------------------- SPOLOCNE METODY --------------------------------


def daj_anotaciu_afirmacie(a):
    if a:
        return "+"
    return "-"


def daj_anotaciu_osoby(osoba):
    anot_osoba = "a"

    if osoba == "2":
        anot_osoba = "b"
    elif osoba == "3":
        anot_osoba = "c"

    return anot_osoba


def daj_anotaciu_stupna(stupen):
    anot_stupen = "x"

    if stupen == "2":
        anot_stupen = "y"
    elif stupen == "3":
        anot_stupen = "z"

    return anot_stupen


def daj_anotaciu_padu(pad):
    anot_pad = 1

    if pad == "Nom":
        anot_pad = "1"
    elif pad == "Gen":
        anot_pad = "2"
    elif pad == "Dat":
        anot_pad = "3"
    elif pad == "Aku":
        anot_pad = "4"
    elif pad == "Vok":
        anot_pad = "5"
    elif pad == "Lok":
        anot_pad = "6"
    elif pad == "Ins":
        anot_pad = "7"

    return anot_pad


def daj_anotaciu_rodu(rod, podrod):
    anot_rod = "m"

    if rod == "M" and podrod == "Z":
        anot_rod = "m"
    elif rod == "M" and podrod == "N":
        anot_rod = "i"
    elif rod == "Z":
        anot_rod = "f"
    elif rod == "S":
        anot_rod = "n"
    elif rod == "h":
        anot_rod = "h"
    elif rod == "o":
        anot_rod = "o"

    return anot_rod


def daj_anotaciu_cisla(cislo):

    anot_cislo = "s"

    if cislo == "J":
        anot_cislo = "s"
    else:
        anot_cislo = "p"

    return anot_cislo


def daj_pole_znakov(string):
    result = []

    index = 0

    prvy_je_upper = string[index].upper() == string[index]

    string = string.lower()

    while index < len(string):
        if string[index] == "d":
            if len(string) > index+1:
                if string[index+1] == "z":
                    result.append("dz")
                    index += 2
                elif string[index+1] == "ž":
                    result.append("dž")
                    index += 2
                else:
                    result.append(string[index])
                    index += 1
            else:
                result.append(string[index])
                index += 1

        elif string[index] == "c":
            if len(string) > index+1:
                if string[index+1] == "h":
                    result.append("ch")
                    index += 2
                else:
                    result.append(string[index])
                    index += 1
            else:
                result.append(string[index])
                index += 1
        elif string[index] == "i":
            if len(string) > index+1:
                if string[index+1] in ("a", "e", "u"):
                    result.append("i"+string[index+1])
                    index += 2
                else:
                    result.append(string[index])
                    index += 1
            else:
                result.append(string[index])
                index += 1
        else:
            result.append(string[index])
            index += 1

    if prvy_je_upper:
        result[0] = result[0].upper()

    return result


def zretaz_pole_znakov(pole):
    res = ""

    for p in pole:
        res += p

    return res


def daj_parhlaska(hlaska):
    d = {"á": "a", "ia": "a", "ie": "e", "ô": "o", "ý": "y", "í": "i", "ú": "u", "ŕ": "r", "ĺ": "l"}

    return d[hlaska]


def daj_vsetky_vzory():
    data = []

    for v in SDVzor.query.all():
        data.append(v.exportuj())

    return data


def daj_vsetky_prefix_sufix():
    data = []

    for v in SDPrefixSufix.query.order_by(func.char_length(SDPrefixSufix.hodnota).desc()).all():
        data.append(v.exportuj())

    return data


def je_spoluhlaska(hlaska):
    #                 ---------- tvrde ---------------------
    return hlaska in ("h", "ch", "k", "g", "d", "t", "n", "l",
    #                 -------------------- makke ----------------------------------
                      "c", "č", "dz", "dž", "f", "j", "š", "ž", "ť", "ď", "ň", "ľ",
    #                  ------------obojake ----------
                      "v", "m", "r", "b", "p", "s", "f", "z")


# ----------------------------- METODY PRE PODSTATNE MENA --------------------------------
# ----------------------------- METODY PRE PODSTATNE MENA --------------------------------
# ----------------------------- METODY PRE PODSTATNE MENA --------------------------------

def daj_anotaciu_pm(paradigma, rod, podrod, cislo, pad):

    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_pad = daj_anotaciu_padu(pad)

    if not paradigma or paradigma == "":
        paradigma = "?"

    anotacia = f"S{paradigma}{anot_rod}{anot_cislo}{anot_pad}"

    return anotacia


def daj_tvar_pm(koren, deklinacia, alternacia, paradigma, rod, podrod, cislo, pad):
    d = {"Nom": "", 'Gen': "", 'Dat': "", 'Aku': "", 'Lok': "", 'Ins': ""}

    splitted = deklinacia.split(",")

    if cislo == "J":
        d["Nom"] = splitted[0]
        d["Gen"] = splitted[1]
        d["Dat"] = splitted[2]
        d["Aku"] = splitted[3]
        d["Lok"] = splitted[4]
        d["Ins"] = splitted[5]
    else:
        d["Nom"] = splitted[6]
        d["Gen"] = splitted[7]
        d["Dat"] = splitted[8]
        d["Aku"] = splitted[9]
        d["Lok"] = splitted[10]
        d["Ins"] = splitted[11]

    return f"{koren}{d[pad]}", rod, podrod, pad, cislo, daj_anotaciu_pm(paradigma, rod, podrod, cislo, pad)


def generuj_morfo_pm(filter_obj, deklinacia, alternacia, paradigma, rod, podrod):

    podm = PodstatneMeno.query.get(filter_obj.sd_id)

    vysledok = []

    if filter_obj.cislo == "" or filter_obj.cislo == "J":
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Ins")
            vysledok.append(morfo_res_obj)

    if filter_obj.cislo == "" or filter_obj.cislo in ("M", "P"):
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Ins")
            vysledok.append(morfo_res_obj)

    return vysledok


def najdi_slovo_z_exportu(sd_id, slovo_export):
    slova = Slovo.query.filter(Slovo.sd_id == sd_id)

    if slovo_export.rod:
        slova = slova.filter(Slovo.rod == slovo_export.rod)

    if slovo_export.podrod:
        slova = slova.filter(Slovo.podrod == slovo_export.podrod)

    if slovo_export.pad:
        slova = slova.filter(Slovo.pad == slovo_export.pad)

    if slovo_export.cislo:
        slova = slova.filter(Slovo.cislo == slovo_export.cislo)

    if slovo_export.cas:
        slova = slova.filter(Slovo.cas == slovo_export.cas)

    if slovo_export.sposob:
        slova = slova.filter(Slovo.sposob == slovo_export.sposob)

    if slovo_export.stupen:
        slova = slova.filter(Slovo.stupen == slovo_export.stupen)

    if slovo_export.pricastie:
        slova = slova.filter(Slovo.pricastie == slovo_export.pricastie)

    if slovo_export.osoba:
        slova = slova.filter(Slovo.osoba == slovo_export.osoba)

    if slova.count() > 1:

        slova1 = slova.filter(Slovo.tvar == slovo_export.tvar)

        if slova1.count() > 0:
            slova = slova1

    if slova.count() > 1:

        slova2 = slova.filter(Slovo.anotacia == slovo_export.anotacia)

        if slova2.count() > 0:
            slova = slova2

    return slova.first()


# ----------------------------- METODY PRE CISLOVKY  --------------------------------
# ----------------------------- METODY PRE CISLOVKY --------------------------------
# ----------------------------- METODY PRE CISLOVKY --------------------------------

def daj_anotaciu_cislovky(paradigma, rod, podrod, cislo, pad):
    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_pad = daj_anotaciu_padu(pad)

    if not paradigma or paradigma == "":
        paradigma = "?"

    anotacia = f"N{paradigma}{anot_rod}{anot_cislo}{anot_pad}"

    return anotacia


def daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, pad):
    sklon_vzor = SDVzor.query.filter(SDVzor.typ == "CISLOVKA").filter(SDVzor.vzor == vzor)

    sklon_vzor = sklon_vzor.filter(SDVzor.rod == rod)

    if podrod:
        sklon_vzor = sklon_vzor.filter(SDVzor.podrod == podrod)

    sklon_vzor = sklon_vzor.first()

    if sklon_vzor:
        deklinacia = sklon_vzor.deklinacia

        d = {"Nom": "", 'Gen': "", 'Dat': "", 'Aku': "", 'Lok': "", 'Ins': ""}

        splitted = deklinacia.split(",")

        if cislo == "J":
            d["Nom"] = splitted[0]
            d["Gen"] = splitted[1]
            d["Dat"] = splitted[2]
            d["Aku"] = splitted[3]
            d["Lok"] = splitted[4]
            d["Ins"] = splitted[5]
        else:
            d["Nom"] = splitted[6]
            d["Gen"] = splitted[7]
            d["Dat"] = splitted[8]
            d["Aku"] = splitted[9]
            d["Lok"] = splitted[10]
            d["Ins"] = splitted[11]

        if not koren:
            koren = ""

        if d[pad] == "x":
            return None, None, None, None, None, None
        else:
            return f"{koren}{d[pad]}", rod, podrod, cislo, pad, daj_anotaciu_cislovky(paradigma, rod, podrod,
                                                                                      cislo, pad)
    else:
        return None, None, None, None, None, None


def daj_tvar_cislovka(vzor, paradigma, koren, rod, podrod, cislo, pad):
    vysledok = []

    if pad == "" or pad == "Nom":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.anotacia = daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, "Nom")
        if morfo_res_obj.tvar:
            vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Gen":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.anotacia = daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, "Gen")
        if morfo_res_obj.tvar:
            vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Dat":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.anotacia = daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, "Dat")
        if morfo_res_obj.tvar:
            vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Aku":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.anotacia = daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, "Aku")
        if morfo_res_obj.tvar:
            vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Lok":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.anotacia = daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, "Lok")
        if morfo_res_obj.tvar:
            vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Ins":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.anotacia = daj_tvar_cislovka_pre_pad(vzor, paradigma, koren, rod, podrod, cislo, "Ins")
        if morfo_res_obj.tvar:
            vysledok.append(morfo_res_obj)

    return vysledok


def generuj_morfo_cislovka(filter_obj, cislovka):

    vysledok = []

    if filter_obj.rod == "" or filter_obj.rod == "M":
        rod = "M"
        if filter_obj.podrod == "" or filter_obj.podrod == "Z":
            podrod = "Z"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                                                  filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                                                  filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

        if filter_obj.podrod == "" or filter_obj.podrod == "N":
            podrod = "N"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                                                  filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                                                  filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

    if filter_obj.rod == "" or filter_obj.rod == "Z":
        rod = "Z"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                                              filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

    if filter_obj.cislo == "" or filter_obj.cislo != "J":
        cislo = "M"
        vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                        filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

    if filter_obj.rod == "" or filter_obj.rod == "S":
        rod = "S"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                            filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            vysledok.extend(daj_tvar_cislovka(filter_obj.vzor, filter_obj.paradigma,
                            filter_obj.koren, rod, podrod, cislo, filter_obj.pad))

    return vysledok


# ----------------------------- METODY PRE PRISLOVKY  --------------------------------
# ----------------------------- METODY PRE PRISLOVKY --------------------------------
# ----------------------------- METODY PRE PRISLOVKY --------------------------------

def daj_anotaciu_prislovky(stupen):

    anot_stupen = "x"

    if stupen == "2":
        anot_stupen = "y"
    elif stupen == "3":
        anot_stupen = "z"

    if not stupen or stupen =="":
        anot_stupen = ""

    anotacia = f"D{anot_stupen}"

    return anotacia


def daj_tvar_prislovka(vzor, koren, stupen):

    stupen_prefix = ""
    stupen_sufix = ""

    if stupen != "1":
        stupen_sufix = "jšie"

    if stupen == "3":
        stupen_prefix = "naj"

    return f"{stupen_prefix}{koren}{stupen_sufix}", stupen, daj_anotaciu_prislovky(stupen)


def generuj_morfo_prislovka(filter_obj):

    vysledok = []

    morfo_res_obj1 = SlovoFilterExport()
    morfo_res_obj1.tvar, morfo_res_obj1.stupen, morfo_res_obj1.anotacia = daj_tvar_prislovka(filter_obj.vzor_stup, filter_obj.koren, "1")
    vysledok.append(morfo_res_obj1)

    morfo_res_obj2 = SlovoFilterExport()
    morfo_res_obj2.tvar, morfo_res_obj2.stupen, morfo_res_obj2.anotacia = daj_tvar_prislovka(filter_obj.vzor_stup, filter_obj.koren, "2")
    vysledok.append(morfo_res_obj2)

    morfo_res_obj3 = SlovoFilterExport()
    morfo_res_obj3.tvar, morfo_res_obj3.stupen, morfo_res_obj3.anotacia = daj_tvar_prislovka(filter_obj.vzor_stup, filter_obj.koren, "3")
    vysledok.append(morfo_res_obj3)

    return vysledok


# ----------------------------- METODY PRE ZAMENA  --------------------------------
# ----------------------------- METODY PRE ZAMENA --------------------------------
# ----------------------------- METODY PRE ZAMENA --------------------------------


def daj_anotaciu_zamena(paradigma, rod, podrod, cislo, pad):
    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_pad = daj_anotaciu_padu(pad)

    if not paradigma or paradigma=="":
        paradigma = "?"

    anotacia = f"P{paradigma}{anot_rod}{anot_cislo}{anot_pad}"

    return anotacia


def daj_tvar_zamena(koren, paradigma, rod, podrod, cislo, pad):
    return koren, rod, podrod, pad, cislo, daj_anotaciu_zamena(paradigma, rod, podrod, cislo, pad)


def generuj_morfo_zamena_rod_podrod(filter_obj, paradigma, rod, podrod):

    vysledok = []

    if filter_obj.cislo == "" or filter_obj.cislo == "J":
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "J", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "J", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "J", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "J", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "J", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "J", "Ins")
            vysledok.append(morfo_res_obj)

    if filter_obj.cislo == "" or filter_obj.cislo in ("M", "P"):
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "M", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "M", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "M", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "M", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "M", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = SlovoFilterExport()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad,\
                morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_zamena(filter_obj.koren, paradigma, rod, podrod, "M", "Ins")
            vysledok.append(morfo_res_obj)

    return vysledok


def generuj_morfo_zamena(filter_obj, paradigma):
    vysledok = []

    vysledok.extend(generuj_morfo_zamena_rod_podrod(filter_obj, paradigma, "M", "Z"))
    vysledok.extend(generuj_morfo_zamena_rod_podrod(filter_obj, paradigma, "M", "N"))
    vysledok.extend(generuj_morfo_zamena_rod_podrod(filter_obj, paradigma, "Z", ""))
    vysledok.extend(generuj_morfo_zamena_rod_podrod(filter_obj, paradigma, "S", ""))

    return vysledok

