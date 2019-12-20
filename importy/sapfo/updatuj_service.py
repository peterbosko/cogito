from importy.sapfo.service import *


def daj_sem_priznak(typ, sem_priznak):
    res = None
    with flask_app.app_context():
        res = Semantika.query.filter(Semantika.kod == sem_priznak).filter(Semantika.typ == typ).first()

    return res


def daj_sem_pad2(kod):
    res = None
    with flask_app.app_context():
        res = SemantickyPad.query.filter(SemantickyPad.kod == kod).first()

    return res


def daj_intencny_ramec(kod):
    res = None
    with flask_app.app_context():
        res = IntencnyRamec.query.filter(IntencnyRamec.kod == kod).first()

    return res


def zaloz_hierarchiu_sd(slovo, rodic):
    with flask_app.app_context():
        h = HierarchiaSD.query.filter(HierarchiaSD.sd_id == slovo).filter(HierarchiaSD.parent_sd_id == rodic).first()

        if h:
            pass
        else:
            h = HierarchiaSD()
            h.sd_id = slovo
            h.parent_sd_id = rodic
            db.session.add(h)
            db.session.commit()


def updatuj_pod_m(koren, slovo_id, rodic_id, s_priznak, prefix, sufix, vzor, poc):
    with flask_app.app_context():
        pm = PodstatneMeno.query.get(slovo_id)

        s = daj_sem_priznak("POD_M", s_priznak)

        s_id = None

        if s:
            s_id = s.id

        pm.sem_priznak_id = s_id
        pm.prefix = prefix
        pm.sufix = sufix
        pm.vzor = vzor
        pm.pocitatelnost = poc
        pm.koren = koren

        if rodic_id and rodic_id > 0:
            if slovo_id != rodic_id:
                zaloz_hierarchiu_sd(slovo_id, rodic_id)

        db.session.add(pm)
        db.session.commit()


def updatuj_prid_m(koren, slovo_id, rodic_id, s_priznak_pod_m, prefix, sufix, vzor, s_priznak_prid_m, vzor2):
    with flask_app.app_context():
        pm = PridavneMeno.query.get(slovo_id)

        s = daj_sem_priznak("POD_M", s_priznak_pod_m)

        s_id = None

        if s:
            s_id = s.id

        pm.sem_priznak_id = s_id

        s2 = daj_sem_priznak("PRID_M", s_priznak_prid_m)

        s_id2 = None

        if s2:
            s_id2 = s2.id

        pm.sem_priznak_prid_m_id = s_id2

        pm.prefix = prefix
        pm.sufix = sufix
        pm.vzor = vzor
        pm.vzor2 = vzor2
        pm.koren = koren

        if rodic_id and rodic_id > 0:
            if slovo_id != rodic_id:
                zaloz_hierarchiu_sd(slovo_id, rodic_id)

        db.session.add(pm)
        db.session.commit()


def updatuj_sl(koren, slovo_id, rodic_id, intencny_ramec, prefix, sufix, vzor, vid, pzkmen):
    with flask_app.app_context():
        sl = Sloveso.query.get(slovo_id)

        i = daj_intencny_ramec(intencny_ramec)

        i_id = None

        if i:
            i_id = i.id

        sl.int_ramec_id = i_id

        sl.prefix = prefix
        sl.sufix = sufix
        sl.vzor = vzor
        sl.vid = vid
        sl.pzkmen = pzkmen
        sl.koren = koren

        db.session.add(sl)
        db.session.commit()


def updatuj_prislovku(koren, slovo_id, rodic_id, sem_pad, vzor, prefix, sufix, koncovka):
    with flask_app.app_context():
        adv = Prislovka.query.get(slovo_id)

        s = daj_sem_pad2(sem_pad)

        s_id = None

        if s:
            s_id = s.id

        adv.sp = s_id
        adv.prefix = prefix
        adv.sufix = sufix
        adv.vzor = vzor
        adv.koncovka = koncovka
        adv.koren = koren

        if rodic_id and rodic_id > 0:
            if slovo_id != rodic_id:
                zaloz_hierarchiu_sd(slovo_id, rodic_id)

        db.session.add(adv)
        db.session.commit()


def updatuj_cislovku(koren, slovo_id, rodic_id, sem_priznak, vzor, prefix, sufix, hodnota):
    with flask_app.app_context():
        cis = Cislovka.query.get(slovo_id)

        s = daj_sem_priznak("CISLOVKA", sem_priznak)

        s_id = None

        if s:
            s_id = s.id

        cis.sem_priznak_id = s_id
        cis.prefix = prefix
        cis.sufix = sufix
        cis.vzor = vzor
        cis.hodnota = hodnota
        cis.koren = koren

        if rodic_id and rodic_id > 0:
            if slovo_id != rodic_id:
                zaloz_hierarchiu_sd(slovo_id, rodic_id)

        db.session.add(cis)
        db.session.commit()


def zaloz_vzor(druh, vz, rod, deklinacia, alter):
    with flask_app.app_context():
        v = SDVzory.query.filter(SDVzory.vzor == vz).filter(SDVzory.typ == druh).first()

        r = "M"

        if rod == "zen":
            r = "Z"
        elif rod == "str":
            r = "S"

        if not v:
            v = SDVzory()

        v.typ = druh
        v.rod = r
        v.vzor = vz
        v.deklinacia = deklinacia
        v.alternacia = alter

        db.session.add(v)
        db.session.commit()


