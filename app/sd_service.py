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

    return f"{koren}{d[pad]}", pad, cislo, daj_anotaciu_pm(paradigma, rod, podrod, cislo, pad)


def generuj_morfo_pm(filter_obj, deklinacia, alternacia, paradigma, rod, podrod):

    podm = PodstatneMeno.query.get(filter_obj.sd_id)

    vysledok = []

    if filter_obj.cislo == "" or filter_obj.cislo == "J":
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "J", "Ins")
            vysledok.append(morfo_res_obj)

    if filter_obj.cislo == "" or filter_obj.cislo in ("M","P"):
        if filter_obj.pad == "" or filter_obj.pad == "Nom":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Nom")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Gen":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Gen")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Dat":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Dat")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Aku":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Aku")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Lok":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Lok")
            vysledok.append(morfo_res_obj)

        if filter_obj.pad == "" or filter_obj.pad == "Ins":
            morfo_res_obj = MorfoFilter()
            morfo_res_obj.tvar, morfo_res_obj.pad, morfo_res_obj.cislo, morfo_res_obj.anotacia = \
                daj_tvar_pm(filter_obj.koren, deklinacia, alternacia, paradigma, rod, podrod, "M", "Ins")
            vysledok.append(morfo_res_obj)

    return vysledok

