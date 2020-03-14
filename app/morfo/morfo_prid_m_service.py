from app.morfo.morfo_service import *
# ----------------------------- METODY PRE PRIDAVNE MENA --------------------------------
# ----------------------------- METODY PRE PRIDAVNE MENA --------------------------------
# ----------------------------- METODY PRE PRIDAVNE MENA --------------------------------


def daj_anotaciu_prid_m(paradigma, rod, podrod, cislo, pad, stupen, pricastie):
    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_pad = daj_anotaciu_padu(pad)

    anot_typ = "A"

    if not paradigma or paradigma == "":
        paradigma = "?"

    if paradigma in ('A', 'F', 'U', "?"):
        anot_typ = "A"
    else:
        anot_typ = "G"

    anot_stupen = daj_anotaciu_stupna(stupen)

    if pricastie == "T":
        anot_typ = "G"
        paradigma = "t"
    elif pricastie == "M":
        anot_typ = "G"
        paradigma = "t"
    elif pricastie == "C":
        anot_typ = "G"
        paradigma = "k"

    anotacia = f"{anot_typ}{paradigma}{anot_rod}{anot_cislo}{anot_pad}{anot_stupen}"

    return anotacia


def daj_druhy_stupen_prid_m(vzor_stup, koren):
    if vzor_stup == "belasý":
        return f"{koren}ejš"
    elif vzor_stup == "biely":
        koren_pole_znakov = daj_pole_znakov(koren)
        parsam = daj_parhlaska(koren_pole_znakov[1])
        return f"{koren_pole_znakov[0]}{parsam}{zretaz_pole_znakov(koren_pole_znakov[2:])}š"
    elif vzor_stup == "samovzor":
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
        return zretaz_pole_znakov(koren_pole_znakov[:-1]) + "š"
    elif vzor_stup == "nový":
        return koren + "š"


def daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma, koren, rod, podrod, cislo, pad, stupen, pricastie=None,
                            koren_slovesa=None, pricastie_sufix=None):

    if pricastie == "M":
        koren = f"{koren_slovesa}{pricastie_sufix}š"
    elif pricastie == "T":
        koren = f"{koren_slovesa}{pricastie_sufix}"

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
        k_cudzi, r_cudzi, podrod_cudzi, cislo_cudzi, pad_cudzi, stupen_cudzi, pricastie_cudzi, anotacia_cudzi = \
            daj_tvar_prid_m_pre_pad("cudzí", "", paradigma, koren, rod, podrod, cislo, pad, "1")
        return k_cudzi, r_cudzi, podrod_cudzi, cislo_cudzi, pad_cudzi, stupen, pricastie,\
            daj_anotaciu_prid_m(paradigma, rod, podrod, cislo, pad, stupen, pricastie)

    return f"{koren}{d[pad]}", rod, podrod, cislo, pad, stupen, pricastie, daj_anotaciu_prid_m(paradigma, rod, podrod,
                                                                                               cislo, pad, stupen,
                                                                                               pricastie)


def daj_tvar_prid_m(vzor, vzor_stup, paradigma, koren, rod, podrod, cislo, pad, stupen, pricastie,
                    koren_slovesa=None, pricastie_sufix=None):
    vysledok = []

    if pad == "" or pad == "Nom":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, morfo_res_obj.pricastie, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Nom",
                                                             stupen, pricastie, koren_slovesa, pricastie_sufix)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Gen":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, morfo_res_obj.pricastie, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Gen",
                                                             stupen, pricastie, koren_slovesa, pricastie_sufix)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Dat":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, morfo_res_obj.pricastie, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Dat",
                                                             stupen, pricastie, koren_slovesa, pricastie_sufix)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Aku":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, morfo_res_obj.pricastie, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Aku",
                                                             stupen, pricastie, koren_slovesa, pricastie_sufix)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Lok":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, morfo_res_obj.pricastie, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Lok",
                                                             stupen, pricastie, koren_slovesa, pricastie_sufix)
        vysledok.append(morfo_res_obj)

    if pad == "" or pad == "Ins":
        morfo_res_obj = SlovoFilterExport()
        morfo_res_obj.tvar, morfo_res_obj.rod, morfo_res_obj.podrod, morfo_res_obj.cislo, morfo_res_obj.pad, \
            morfo_res_obj.stupen, morfo_res_obj.pricastie, \
            morfo_res_obj.anotacia = daj_tvar_prid_m_pre_pad(vzor, vzor_stup, paradigma,
                                                             koren, rod, podrod, cislo, "Ins",
                                                             stupen, pricastie, koren_slovesa, pricastie_sufix)
        vysledok.append(morfo_res_obj)

    return vysledok


def generuj_pricastie(filter_obj, pricastie):
    vysledok = []

    if pricastie == "M":
        if filter_obj.stupen == "":
            filter_obj.stupen = "1"

        filter_obj.vzor = "cudzí"
        filter_obj.pricastie_sufix = filter_obj.pricastie_sufix_m

    elif pricastie == "T":
        if filter_obj.stupen == "":
            filter_obj.stupen = "1"

        filter_obj.vzor = "pekný"
        filter_obj.pricastie_sufix = filter_obj.pricastie_sufix_t

    if filter_obj.rod == "" or filter_obj.rod == "M":
        rod = "M"
        if filter_obj.podrod == "" or filter_obj.podrod == "Z":
            podrod = "Z"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))

            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))

                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
        if filter_obj.podrod == "" or filter_obj.podrod == "N":
            podrod = "N"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.stupen == "" or filter_obj.stupen == "1":
                    stupen = "1"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "2":
                    stupen = "2"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
                if filter_obj.stupen == "" or filter_obj.stupen == "3":
                    stupen = "3"
                    vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                    filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                    pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))

    if filter_obj.rod == "" or filter_obj.rod == "Z":
        rod = "Z"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))

    if filter_obj.rod == "" or filter_obj.rod == "S":
        rod = "S"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "2":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))
            if filter_obj.stupen == "" or filter_obj.stupen == "3":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen,
                                                pricastie, filter_obj.koren_slovesa, filter_obj.pricastie_sufix))

    return vysledok


def generuj_morfo_prid_m(filter_obj, sloveso_id):
    vysledok = []

    pricastie = ""

    if not sloveso_id:
        vysledok.extend(generuj_pricastie(filter_obj, pricastie))

    if sloveso_id and sloveso_id > 0:
        if filter_obj.co_generovat == "*" or filter_obj.co_generovat == "C":
            pricastie = "C"
            vysledok.extend(generuj_pricastie(filter_obj, pricastie))

        if filter_obj.co_generovat == "*" or filter_obj.co_generovat == "M":
            pricastie = "M"
            vysledok.extend(generuj_pricastie(filter_obj, pricastie))

        if filter_obj.co_generovat == "*" or filter_obj.co_generovat == "T":
            pricastie = "T"
            vysledok.extend(generuj_pricastie(filter_obj, pricastie))

    return vysledok


def vrat_slovo_prid_m(sd_id, rod, podrod, cislo, pad, pricastie, koncovka=None):

    slovo = Slovo.query.filter(Slovo.sd_id == sd_id).filter(Slovo.rod == rod).filter(Slovo.podrod == podrod).\
        filter(Slovo.cislo == cislo).filter(Slovo.pricastie == pricastie).filter(Slovo.pad == pad)

    if koncovka:
        slovo = slovo.filter(Slovo.tvar_lower.like("%"+koncovka.lower()))

    slovo = slovo.first()

    return slovo


