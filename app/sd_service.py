from app.db_models import *
from sqlalchemy import and_


def daj_pocet_intencii_sp(id):
    return db.session.query(Intencia).filter(Intencia.sem_pad_id == id).count()


def daj_pocet_slovies_sp(id):
    zoznam_ir = db.session.query(Intencia.int_ramec_id).filter(Intencia.sem_pad_id == id).distinct()

    q = db.session.query(Sloveso).filter(Sloveso.int_ramec_id.in_(zoznam_ir))

    # q = db.session.query(Sloveso.id).\
    #    join(Intencia, and_(Intencia.sp == id, Sloveso.int_ramec_id == Intencia.int_ramec_id)).\
    #    join(IntencnyRamec, IntencnyRamec.id == Intencia.int_ramec_id).distinct()

    return q.count()


def daj_pocet_intencii_ramca(id):
    return db.session.query(Intencia).filter(Intencia.int_ramec_id == id).count()


def daj_pocet_slovies_ramca(id):
    return db.session.query(Sloveso).filter(Sloveso.int_ramec_id == id).count()


def daj_pocet_slov_sem_priznaku(typ, id):
    if typ == "PRID_M":
        return db.session.query(PridavneMeno).filter(PridavneMeno.sem_priznak_prid_m_id == id).count()
    else:
        return db.session.query(SlovnyDruh).filter(SlovnyDruh.sem_priznak_id == id).count()


def vrat_polozku_sem_stromu_nadol(id, parent):
    leaf = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.id == id).first()

    if leaf:
        data = SemStrom()
        data.id = id
        data.sem_priznak_id = leaf.sem_priznak_id

        data.parent = parent

        pocet_slov = 0

        if leaf.typ == "PRID_M":
            pocet_slov = leaf.pocet_slov_prid_m
        else:
            pocet_slov = leaf.pocet_slov

        data.text = f"({leaf.kod}) - {leaf.nazov} : Počet slov: {pocet_slov}"

        return data

    return None


def vrat_polozku_sem_stromu_nahor(id, parent, rodic_id):

    leaf = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.id == id) \
          .filter(SemHierarchiaView.rodic_id == rodic_id) \
          .first()

    if leaf:
        data = SemStrom()
        data.id = parent + '-' + str(id)
        data.sem_priznak_id = leaf.sem_priznak_id

        data.parent = parent

        pocet_slov = 0

        if leaf.typ == "PRID_M":
            pocet_slov = leaf.pocet_slov_prid_m
        else:
            pocet_slov = leaf.pocet_slov

        data.text = f"({leaf.kod}) - {leaf.nazov} : Počet slov: {pocet_slov}"

        return data

    return None


def daj_sem_strom_rekurzia_nadol(id, parent):
    data = []

    deti = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.rodic_id == id)

    for d in deti:
        data.append(vrat_polozku_sem_stromu_nadol(d.id, parent))
        data.extend(daj_sem_strom_rekurzia_nadol(d.sem_priznak_id, str(d.id)))

    return data


def daj_sem_strom_rekurzia_nahor(id, parent):
    data = []

    rodicia = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.sem_priznak_id == id)

    for d in rodicia:
        data.append(vrat_polozku_sem_stromu_nahor(d.id, parent, d.rodic_id))
        if d.rodic_id:
            data.extend(daj_sem_strom_rekurzia_nahor(d.rodic_id, parent + '-' + str(d.id)))

    return data


def vrat_data_sem_stromu(sem_priznak_id, smer):
    data = []

    polozky = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.sem_priznak_id == sem_priznak_id)

    if smer == "NADOL":
        for p in polozky:
            data.append(vrat_polozku_sem_stromu_nadol(p.id, '#'))
        for p in polozky:
            data.extend(daj_sem_strom_rekurzia_nadol(sem_priznak_id, str(p.id)))
    else:
        for p in polozky:
            data.append(vrat_polozku_sem_stromu_nahor(p.id, '#', p.rodic_id))
        for p in polozky:
            if p.rodic_id:
                data.extend(daj_sem_strom_rekurzia_nahor(p.rodic_id, '#-'+str(p.id)))

    return data


def daj_vsetky_vzory():
    data = []

    for v in SDVzor.query.all():
        data.append(v.exportuj())

    return data


def daj_vsetky_prefix_sufix():
    data = []

    for v in SDPrefixSufix.query.all():
        data.append(v.exportuj())

    return data


def daj_anotaciu_pm(paradigma, rod, podrod, cislo, pad):

    anot_rod = "m"

    if rod == "M" and podrod == "Z":
        anot_rod = "m"
    elif rod == "M" and podrod == "N":
        anot_rod = "i"
    elif rod == "Z":
        anot_rod = "f"
    elif rod == "S":
        anot_rod = "n"

    anot_cislo = "s"

    if cislo == "J":
        anot_cislo = "s"
    else:
        anot_cislo = "p"

    anot_pad = "1"

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

    anotacia = f"S{paradigma}{anot_rod}{anot_cislo}{anot_pad}"

    return anotacia


def daj_anotaciu_prid_m(paradigma, rod, podrod, cislo, pad, stupen):
    anot_rod = "m"

    if rod == "M" and podrod == "Z":
        anot_rod = "m"
    elif rod == "M" and podrod == "N":
        anot_rod = "i"
    elif rod == "Z":
        anot_rod = "f"
    elif rod == "S":
        anot_rod = "n"

    anot_cislo = "s"

    if cislo == "J":
        anot_cislo = "s"
    else:
        anot_cislo = "p"

    anot_pad = "1"

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

    anot_typ = "A"

    if paradigma in ('A', 'F', 'U'):
        anot_typ = "A"
    else:
        anot_typ = "G"

    anot_stupen = "x"

    if stupen == "2":
        anot_stupen = "y"
    elif stupen == "3":
        anot_stupen = "z"

    anotacia = f"{anot_typ}{paradigma}{anot_rod}{anot_cislo}{anot_pad}{anot_stupen}"

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

    if filter_obj.cislo == "" or filter_obj.cislo in ("M","P"):
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


def daj_pole_znakov(string):
    result = []

    index = 0

    prvy_je_upper = string[index].upper() == string[index]

    string = string.lower()

    while index < len(string):
        if string[index] == "d":
            if len(string) >= index+1:
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
            if len(string) >= index+1:
                if string[index+1] == "h":
                    result.append("ch")
                    index += 2
                else:
                    result.append(string[index])
                    index += 1
        elif string[index] == "i":
            if len(string) >= index+1:
                if string[index+1] in ("a", "e", "i"):
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
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
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
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "1"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                stupen = "2"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))
            if filter_obj.stupen == "" or filter_obj.stupen == "1":
                stupen = "3"
                vysledok.extend(daj_tvar_prid_m(filter_obj.vzor, filter_obj.vzor_stup, filter_obj.paradigma,
                                                filter_obj.koren, rod, podrod, cislo, filter_obj.pad, stupen))

    return vysledok

