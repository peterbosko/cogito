from sqlalchemy import exc
from sqlalchemy import and_
from sqlalchemy.sql.expression import func
import operator
from sqlalchemy import or_
from app.db_models.metadata import *
from app.db_models.slovny_druh import *


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


def vrat_polozku_sem_stromu_nadol(id, parent):
    leaf = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.id == id).first()

    if leaf:
        data = SemStrom()
        data.id = id
        data.sem_priznak_id = leaf.sem_priznak_id

        data.parent = parent

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


def daj_zakladny_tvar_sd(idsd):
    if not idsd:
        return ""
    else:
        sd = SlovnyDruh.query.get(idsd)

        zvrat = ""

        if sd.typ == "SLOVESO":
            sloveso = Sloveso.query.get(idsd)
            if sloveso.zvratnost:
                zvrat = " " + sloveso.zvratnost

        return sd.zak_tvar + zvrat


def daj_nazov_konceptu(idkonceptu):
    if not idkonceptu:
        return ""
    else:
        k = Koncept.query.get(idkonceptu)

        return k.nazov


def daj_slovesne_vzory():
    vysledok = []

    nenastavene = None

    for gr in db.session.query(SDVzor.vzor, func.count(Sloveso.vzor)).filter(SDVzor.typ == "SLOVESO").\
            outerjoin(Sloveso, SDVzor.vzor == Sloveso.vzor).\
            group_by(SDVzor.vzor).\
            order_by(func.count(Sloveso.vzor).desc()).all():

        stat = VzorSoStatistikou()

        v = gr[0]

        if v:
            stat.vzor = v
            stat.hodnota = v
            stat.pocet = gr[1]
            vobj = SDVzor.query.filter(SDVzor.typ == "SLOVESO").filter(SDVzor.vzor == v).first()

            if vobj:
                stat.popis = vobj.popis

            if not stat.popis:
                stat.popis = ""

            vysledok.append(stat)
        else:

            stat.pocet = gr[1]
            stat.vzor = "nenastavený"
            stat.hodnota = "-1"
            stat.popis = ""

            if not nenastavene:
                stat.pocet = db.session.query(Sloveso).filter(or_(Sloveso.vzor.is_(None), Sloveso.vzor == "")).count()
                nenastavene = stat
                vysledok.append(stat)
            else:
                pass

    return vysledok


def daj_pm_vzory(rod=None):
    vysledok = []

    nenastavene = None

    vzory = db.session.query(SDVzor.vzor, func.count(PodstatneMeno.vzor)).filter(SDVzor.typ == "POD_M").\
        outerjoin(PodstatneMeno, SDVzor.vzor == PodstatneMeno.vzor).\
        group_by(PodstatneMeno.vzor).\
        order_by(func.count(PodstatneMeno.vzor).desc())

    if rod:
        vzory = vzory.filter(SDVzor.rod == rod)

    for gr in vzory.all():
        stat = VzorSoStatistikou()

        v = gr[0]

        if v:
            stat.vzor = v
            stat.hodnota = v
            stat.pocet = gr[1]
            vobj = SDVzor.query.filter(SDVzor.typ == "POD_M").filter(SDVzor.vzor == v).first()

            if vobj:
                stat.popis = vobj.popis

            if not stat.popis:
                stat.popis = ""

            vysledok.append(stat)
        else:

            stat.pocet = gr[1]
            stat.vzor = "nenastavený"
            stat.hodnota = "-1"
            stat.popis = ""

            if not nenastavene:
                stat.pocet = db.session.query(PodstatneMeno).filter(or_(PodstatneMeno.vzor.is_(None),
                                                                        PodstatneMeno.vzor == "")).count()
                nenastavene = stat
                vysledok.append(stat)
            else:
                pass

    return vysledok


def daj_prid_m_vzory():
    vysledok = []

    nenastavene = None

    for gr in db.session.query(SDVzor.vzor, func.count(PridavneMeno.vzor)).filter(SDVzor.typ == "PRID_M").\
            filter(SDVzor.sklon_stup == "sklon").\
            outerjoin(PridavneMeno, SDVzor.vzor == PridavneMeno.vzor).\
            group_by(SDVzor.vzor).\
            order_by(func.count(PridavneMeno.vzor).desc()).all():

        stat = VzorSoStatistikou()

        v = gr[0]

        if v:
            stat.vzor = v
            stat.hodnota = v
            stat.pocet = gr[1]
            vobj = SDVzor.query.filter(SDVzor.typ == "PRID_M").filter(SDVzor.sklon_stup == "sklon").\
                filter(SDVzor.vzor == v).first()

            if vobj:
                stat.popis = vobj.popis

            if not stat.popis:
                stat.popis = ""

            vysledok.append(stat)
        else:

            stat.pocet = gr[1]
            stat.vzor = "nenastavený"
            stat.hodnota = "-1"
            stat.popis = ""

            if not nenastavene:
                stat.pocet = db.session.query(PridavneMeno).filter(or_(PridavneMeno.vzor.is_(None),
                                                                       PridavneMeno.vzor == "")).count()
                nenastavene = stat
                vysledok.append(stat)
            else:
                pass

    return vysledok


def daj_prid_m_stup_vzory():
    vysledok = []

    nenastavene = None

    for gr in db.session.query(SDVzor.vzor, func.count(PridavneMeno.vzor_stup)).filter(SDVzor.typ == "PRID_M").\
            filter(SDVzor.sklon_stup == "stup").\
            outerjoin(PridavneMeno, SDVzor.vzor == PridavneMeno.vzor_stup).\
            group_by(SDVzor.vzor).\
            order_by(func.count(PridavneMeno.vzor_stup).desc()).all():

        stat = VzorSoStatistikou()

        v = gr[0]

        if v:
            stat.vzor = v
            stat.hodnota = v
            stat.pocet = gr[1]
            vobj = SDVzor.query.filter(SDVzor.typ == "PRID_M").filter(SDVzor.sklon_stup == "stup").\
                filter(SDVzor.vzor == v).first()

            if vobj:
                stat.popis = vobj.popis

            if not stat.popis:
                stat.popis = ""

            vysledok.append(stat)
        else:

            stat.pocet = gr[1]
            stat.vzor = "nenastavený"
            stat.hodnota = "-1"
            stat.popis = ""

            if not nenastavene:
                stat.pocet = db.session.query(PridavneMeno).filter(or_(PridavneMeno.vzor_stup.is_(None),
                                                                       PridavneMeno.vzor_stup == "")).count()
                nenastavene = stat
                vysledok.append(stat)
            else:
                pass

    return vysledok


def daj_prislovka_stup_vzory():
    vysledok = []

    nenastavene = None

    for gr in db.session.query(SDVzor.vzor, func.count(PridavneMeno.vzor_stup)).filter(SDVzor.typ == "PRISLOVKA").\
            filter(SDVzor.sklon_stup == "stup").\
            outerjoin(Prislovka, SDVzor.vzor == Prislovka.vzor_stup).\
            group_by(SDVzor.vzor).\
            order_by(func.count(SDVzor.vzor).desc()).all():

        stat = VzorSoStatistikou()

        v = gr[0]

        if v:
            stat.vzor = v
            stat.hodnota = v
            stat.pocet = gr[1]
            vobj = SDVzor.query.filter(SDVzor.typ == "PRISLOVKA").filter(SDVzor.sklon_stup == "stup").\
                filter(SDVzor.vzor == v).first()

            if vobj:
                stat.popis = vobj.popis

            if not stat.popis:
                stat.popis = ""

            vysledok.append(stat)
        else:

            stat.pocet = gr[1]
            stat.vzor = "nenastavený"
            stat.hodnota = "-1"
            stat.popis = ""

            if not nenastavene:
                stat.pocet = db.session.query(Prislovka).filter(or_(Prislovka.vzor_stup.is_(None),
                                                                    Prislovka.vzor_stup == "")).count()
                nenastavene = stat
                vysledok.append(stat)
            else:
                pass

    return vysledok


def daj_cislovka_vzory():
    vysledok = []

    nenastavene = None

    vzory = db.session.query(SDVzor.vzor, func.count(Cislovka.vzor)).filter(SDVzor.typ == "CISLOVKA").\
        outerjoin(Cislovka, SDVzor.vzor == Cislovka.vzor).\
        group_by(SDVzor.vzor).\
        order_by(func.count(SDVzor.vzor).desc())

    for gr in vzory.all():
        stat = VzorSoStatistikou()

        v = gr[0]

        if v:
            stat.vzor = v
            stat.hodnota = v
            stat.pocet = gr[1]
            vobj = SDVzor.query.filter(SDVzor.typ == "CISLOVKA").filter(SDVzor.vzor == v).first()

            if vobj:
                stat.popis = vobj.popis

            if not stat.popis:
                stat.popis = ""

            vysledok.append(stat)
        else:

            stat.pocet = gr[1]
            stat.vzor = "nenastavený"
            stat.hodnota = "-1"
            stat.popis = ""

            if not nenastavene:
                stat.pocet = db.session.query(Cislovka).filter(or_(Cislovka.vzor.is_(None),
                                                                   Cislovka.vzor == "")).count()
                nenastavene = stat
                vysledok.append(stat)
            else:
                pass

    return vysledok


def daj_prefixy_sufixy(sld, pref_suf):
    vysledok = []

    for ps in db.session.query(SDPrefixSufix).filter(SDPrefixSufix.typ == sld).\
            filter(SDPrefixSufix.prefix_sufix == pref_suf).all():
        stat = VzorSoStatistikou()
        stat.hodnota = ps.hodnota
        vysledok.append(stat)

    return vysledok


def daj_pridavne_meno_k_slovesu(sloveso, je_negacia):
    prm = db.session.query(PridavneMeno).filter(PridavneMeno.sloveso_id == sloveso).\
        filter(PridavneMeno.je_negacia == je_negacia).first()

    return prm


def daj_pocty_sd_a_sl():
    q = db.session.query(SlovnyDruhStat).all()

    return q


def prepocitaj_sd_stat():
    SlovnyDruhStat.query.delete()
    for r in db.session.query(SlovnyDruh.typ, func.count(SlovnyDruh.typ)).group_by(SlovnyDruh.typ).all():
        s = SlovnyDruhStat()
        s.typ = r[0]
        s.pocet = r[1]
        db.session.add(s)
        db.session.commit()

    s2 = SlovnyDruhStat()
    s2.typ = "SL"
    s2.pocet = Slovo.query.count()
    db.session.add(s2)
    db.session.commit()


def zmaz_sem_priznaky(sd_id):
    SlovnyDruhSemantika.query.filter(SlovnyDruhSemantika.sd_id == sd_id).delete()


def zaloz_sem_priznaky(slov_druh, priznaky):
    for p in priznaky.split(";"):
        sem = SlovnyDruhSemantika()
        sem.SlovnyDruh = slov_druh
        sem.sem_priznak = Semantika.query.get(int(p))
        db.session.add(sem)


def zmaz_cely_s_druh(sd_id):

    chyba = ""

    Slovo.query.filter(Slovo.sd_id == sd_id).delete()

    zmaz_sem_priznaky(sd_id)

    sd = SlovnyDruh.query.get(sd_id)

    if sd.typ == "POD_M":
        pm = PodstatneMeno.query.get(sd_id)
        db.session.delete(pm)
    elif sd.typ == "PRID_M":
        prm = PridavneMeno.query.get(sd_id)
        db.session.delete(prm)
    elif sd.typ == "ZAMENO":
        zam = Zameno.query.get(sd_id)
        db.session.delete(zam)
    elif sd.typ == "CISLOVKA":
        cislovka = Cislovka.query.get(sd_id)
        db.session.delete(cislovka)
    elif sd.typ == "SPOJKA":
        sp = Spojka.query.get(sd_id)
        db.session.delete(sp)
    elif sd.typ == "PREDLOZKA":
        predlo = Predlozka.query.get(sd_id)
        db.session.delete(predlo)
    elif sd.typ == "OSTATNE":
        os = Ostatne.query.get(sd_id)
        db.session.delete(os)
    elif sd.typ == "CITOSLOVCE":
        cit = Citoslovce.query.get(sd_id)
        db.session.delete(cit)
    elif sd.typ == "CASTICA":
        c = Castica.query.get(sd_id)
        db.session.delete(c)
    elif sd.typ == "PRISLOVKA":
        prisl = Prislovka.query.get(sd_id)
        db.session.delete(prisl)
    elif sd.typ == "SLOVESO":
        sloveso = Sloveso.query.get(sd_id)
        db.session.delete(sloveso)

    try:
        db.session.commit()
    except exc.IntegrityError as e:
        chyba = "Chyba integrity. Na slovo existuje cudzí kľúč ! " \
                "V prípade slovesa " \
                "skontroluje prídavné, podstatné mená a slovesá !"

    return chyba


