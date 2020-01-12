from app.db_models import *
from sqlalchemy import and_
from sqlalchemy.sql.expression import func


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


