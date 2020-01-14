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
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Ins")
            vysledok.append(morfo_res_obj)

    if filter_obj.cislo == "" or filter_obj.cislo in ("M", "P"):
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod,\
                morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Ins")
            vysledok.append(morfo_res_obj)

    return vysledok


# ----------------------------- METODY PRE PRIDAVNE MENA --------------------------------
# ----------------------------- METODY PRE PRIDAVNE MENA --------------------------------
# ----------------------------- METODY PRE PRIDAVNE MENA --------------------------------


def daj_anotaciu_prid_m(paradigma, rod, podrod, cislo, pad, stupen):
    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_pad = daj_anotaciu_padu(pad)

    anot_typ = "A"

    if paradigma in ('A', 'F', 'U'):
        anot_typ = "A"
    else:
        anot_typ = "G"

    anot_stupen = daj_anotaciu_stupna(stupen)

    anotacia = f"{anot_typ}{paradigma}{anot_rod}{anot_cislo}{anot_pad}{anot_stupen}"

    return anotacia


def daj_druhy_stupen_prid_m(vzor_stup, koren):
    if vzor_stup == "belasý":
        return f"{koren}ejš"
    elif vzor_stup == "biely":
        koren_pole_znakov = daj_pole_znakov(koren)
        parsam = daj_parhlaska(koren_pole_znakov[1])
        return f"{koren_pole_znakov[0]}{parsam}{zretaz_pole_znakov(koren_pole_znakov[2:])}š"
    elif vzor_stup == "suplet":
        if koren[0:4] == "dobr":
            return "lepš"
        elif koren[0:4] == "pekn":
            return "krajš"
        elif koren[0:2] == "zl":
            return "horš"
        elif koren[0:4] == "veľk":
            return "väčš"
        elif koren[0:3] == "mal":
            return "menš"
        elif koren[0:5] == "vysok":
            return "vyšš"
        elif koren[0:5] == "krátk":
            return "kratš"
        else:
            return ""
    elif vzor_stup == "sladký":
        koren_pole_znakov = daj_pole_znakov(koren)
        return zretaz_pole_znakov(koren_pole_znakov[:-1])+"š"
    elif vzor_stup == "nový":
        return koren+"š"


def daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma, koren, rod, podrod, cislo, pad, stupen):
    sklon_vzor = SDVzor.query.filter(SDVzor.typ == "PRID_M").filter(SDVzor.vzor == vzor)

    if rod == "M":
        sklon_vzor = sklon_vzor.filter(SDVzor.rod == "M").filter(SDVzor.podrod == podrod).first()
    else:
        sklon_vzor = sklon_vzor.filter(SDVzor.rod == rod).first()

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

    if stupen != "1":
        koren = daj_druhy_stupen_prid_m(vzor_stup, koren)

    if not koren:
        koren = ""

    if stupen == "3":
        koren = "naj" + koren

    if stupen != "1":
        k_cudzi, r_cudzi, podrod_cudzi, cislo_cudzi, pad_cudzi, stupen_cudzi, anotacia_cudzi = \
            daj_tvar_prid_m_pre_pad("cudzí", "", paradigma, koren, rod, podrod, cislo, pad, "1")
        return k_cudzi, r_cudzi, podrod_cudzi, cislo_cudzi, pad_cudzi, stupen, \
            daj_anotaciu_prid_m(paradigma, rod, podrod, cislo, pad, stupen)

    return f"{koren}{d[pad]}", rod, podrod, cislo, pad, stupen, daj_anotaciu_prid_m(paradigma, rod, podrod,
                                                                                    cislo, pad, stupen)


def daj_tvar_prid_m(vzor, vzor_stup, paradigma, koren, rod, podrod, cislo, pad, stupen):
    vysledok = []

    if pad == "" or pad == "Nom":
        morfo_res_obj = MorfoFilter()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Nom", stupen)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Gen":
        morfo_res_obj = MorfoFilter()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Gen", stupen)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Dat":
        morfo_res_obj = MorfoFilter()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Dat", stupen)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Aku":
        morfo_res_obj = MorfoFilter()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Aku", stupen)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Lok":
        morfo_res_obj = MorfoFilter()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Lok", stupen)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Ins":
        morfo_res_obj = MorfoFilter()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Ins", stupen)
        vysledok.append(morfo_res_obj)

    return vysledok


def generuj_morfo_prid_m(filter_obj):

    vysledok = []

    if filter_obj.rod == "" or filter_obj.rod == "M":
        rod = "M"
        if filter_obj.podrod == "" or filter_obj.podrod == "Z":
            podrod = "Z"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))

            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))

                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
        if filter_obj.podrod == "" or filter_obj.podrod == "N":
            podrod = "N"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))

    if filter_obj.rod == "" or filter_obj.rod == "Z":
        rod = "Z"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))

    if filter_obj.rod == "" or filter_obj.rod == "S":
        rod = "S"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))

    return vysledok

