from app.app import flask_app
from app.db_models import *

import pymysql.cursors
import sys
import csv
import datetime

T_USER = 'tvary'
T_PASSWORD = 'tvary'
T_HOST = 'localhost'
T_DB_NAME = 'tvary'

db.init_app(flask_app)


def zaloz_updatuj_podstatne_meno(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        a_rod = anotacia[2]
        a_cislo = anotacia[3]
        a_pad = anotacia[4]

        rod = "M"
        podrod = "Z"
        cislo = "J"
        pad = "Nom"

        if "m" in anotacia:
            rod = "M"
            podrod = "Z"
        elif "i" in anotacia:
            rod = "M"
            podrod = "N"
        elif "f" in anotacia:
            rod = "Z"
            podrod = None
        elif "n" in anotacia:
            rod = "S"
            podrod = None

        if "s" in anotacia:
            cislo = "J"
        elif "p" in anotacia:
            cislo = "M"

        if "1" in anotacia:
            pad = "Nom"
        elif "2" in anotacia:
            pad = "Gen"
        elif "3" in anotacia:
            pad = "Dat"
        elif "4" in anotacia:
            pad = "Aku"
        elif "5" in anotacia:
            pad = "Vok"
        elif "6" in anotacia:
            pad = "Lok"
        elif "7" in anotacia:
            pad = "Ins"

        pm_objekty = PodstatneMeno.query.filter(PodstatneMeno.rod == rod).\
            filter(PodstatneMeno.zak_tvar == zak_tvar).\
            filter(PodstatneMeno.podrod == podrod)

        if pm_objekty.count() == 1:
            pass
        elif pm_objekty.count() == 0:
            pm = PodstatneMeno(zak_tvar=zak_tvar, rod=rod, podrod=podrod)
            db.session.add(pm)
            pm_objekty = []
            pm_objekty.append(pm)

        for pm in pm_objekty:
            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == pm.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=pm.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.rod = rod
                sl.podrod = podrod
                sl.cislo = cislo
                sl.pad = pad
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_pridavne_meno(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        a_rod = anotacia[2]
        a_cislo = anotacia[3]
        a_pad = anotacia[4]
        a_stupen = anotacia[5]

        rod = "M"
        podrod = "Z"
        cislo = "J"
        pad = "Nom"

        if "m" in anotacia:
            rod = "M"
            podrod = "Z"
        elif "i" in anotacia:
            rod = "M"
            podrod = "N"
        elif "f" in anotacia:
            rod = "Z"
            podrod = None
        elif "n" in anotacia:
            rod = "S"
            podrod = None

        if "s" in anotacia:
            cislo = "J"
        elif "p" in anotacia:
            cislo = "M"

        if "1" in anotacia:
            pad = "Nom"
        elif "2" in anotacia:
            pad = "Gen"
        elif "3" in anotacia:
            pad = "Dat"
        elif "4" in anotacia:
            pad = "Aku"
        elif "5" in anotacia:
            pad = "Vok"
        elif "6" in anotacia:
            pad = "Lok"
        elif "7" in anotacia:
            pad = "Ins"

        stupen = 1

        if "x" in anotacia:
            stupen = 1
        elif "y" in anotacia:
            stupen = 2
        elif "z" in anotacia:
            stupen = 3

        pm_objekty = PridavneMeno.query.filter(PridavneMeno.zak_tvar == zak_tvar)

        if pm_objekty.count() == 0:
            pm = PridavneMeno(zak_tvar=zak_tvar, je_privlastnovacie="?")
            db.session.add(pm)
            pm_objekty = []
            pm_objekty.append(pm)

        for pm in pm_objekty:
            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == pm.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=pm.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.rod = rod
                sl.podrod = podrod
                sl.cislo = cislo
                sl.pad = pad
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.stupen = stupen
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_sloveso(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = "N"
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = "N"
        je_prechodnik = "N"
        osoba = None
        zvratnost = None
        pad = None

        if "M" in anotacia:
            sposob = "R"

        if "I" in anotacia:
            je_neurcitok = "A"
        elif "H" in anotacia:
            je_prechodnik = "A"

        if "K" in anotacia:
            cas = "P"
        elif "L" in anotacia:
            cas = "M"
        elif "B" in anotacia:
            cas = "B"

        if "a" in anotacia:
            osoba = "1"
        elif "b" in anotacia:
            osoba = "2"
        elif "c" in anotacia:
            osoba = "3"

        if "-" in anotacia:
            je_negacia = "A"
        elif "+" in anotacia:
            je_negacia = "N"

        rod = None
        podrod = None
        cislo = None

        if "m" in anotacia:
            rod = "M"
            podrod = "Z"
        elif "i" in anotacia:
            rod = "M"
            podrod = "N"
        elif "f" in anotacia:
            rod = "Z"
            podrod = None
        elif "n" in anotacia:
            rod = "S"
            podrod = None
        elif "h" in anotacia:
            rod = "h"
            podrod = None
        elif "o" in anotacia:
            rod = "o"
            podrod = None

        if "s" in anotacia:
            cislo = "J"
        elif "p" in anotacia:
            cislo = "M"

        slo_objekty = Sloveso.query.filter(Sloveso.zak_tvar == zak_tvar)

        if slo_objekty.count() == 0:
            sloveso = Sloveso(zak_tvar=zak_tvar)
            db.session.add(sloveso)
            slo_objekty = []
            slo_objekty.append(sloveso)
        elif slo_objekty.count() > 1:
            print("viac zaznamov slovies:"+zak_tvar)

        for sloveso_p in slo_objekty:

            zvratnost = None

            if sloveso_p.zvratnost:
                zvratnost = sloveso_p.zvratnost

            cnt = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).\
                filter(Slovo.je_negacia == je_negacia).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.zvratnost == zvratnost). \
                filter(Slovo.cas == cas). \
                filter(Slovo.cislo == cislo). \
                filter(Slovo.sd_id == sloveso_p.id)

            sl = cnt.first()

            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=sloveso_p.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.rod = rod
                sl.podrod = podrod
                sl.cislo = cislo
                sl.tvar = tvar

                if sposob is not None:
                    sl.sposob = sposob

                sl.anotacia = anotacia
                sl.je_negacia = je_negacia
                sl.je_neurcitok = je_neurcitok
                sl.osoba = osoba
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_zameno(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        if "m" in anotacia:
            rod = "M"
            podrod = "Z"
        elif "i" in anotacia:
            rod = "M"
            podrod = "N"
        elif "f" in anotacia:
            rod = "Z"
            podrod = None
        elif "n" in anotacia:
            rod = "S"
            podrod = None
        elif "h" in anotacia:
            rod = "h"
            podrod = None
        elif "o" in anotacia:
            rod = "o"
            podrod = None

        if "s" in anotacia:
            cislo = "J"
        elif "p" in anotacia:
            cislo = "M"

        if "1" in anotacia:
            pad = "Nom"
        elif "2" in anotacia:
            pad = "Gen"
        elif "3" in anotacia:
            pad = "Dat"
        elif "4" in anotacia:
            pad = "Aku"
        elif "5" in anotacia:
            pad = "Vok"
        elif "6" in anotacia:
            pad = "Lok"
        elif "7" in anotacia:
            pad = "Ins"

        z_objekty = Zameno.query.filter(Zameno.rod == rod).\
            filter(Zameno.zak_tvar == zak_tvar).\
            filter(Zameno.podrod == podrod)

        if z_objekty.count() == 1:
            pass
        elif z_objekty.count() == 0:
            zam = Zameno(zak_tvar=zak_tvar, rod=rod, podrod=podrod)
            db.session.add(zam)
            z_objekty = []
            z_objekty.append(zam)

        for z in z_objekty:
            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == z.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=z.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.rod = rod
                sl.podrod = podrod
                sl.cislo = cislo
                sl.pad = pad
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_cislovku(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        if "m" in anotacia:
            rod = "M"
            podrod = "Z"
        elif "i" in anotacia:
            rod = "M"
            podrod = "N"
        elif "f" in anotacia:
            rod = "Z"
            podrod = None
        elif "n" in anotacia:
            rod = "S"
            podrod = None
        elif "h" in anotacia:
            rod = "h"
            podrod = None
        elif "o" in anotacia:
            rod = "o"
            podrod = None

        if "s" in anotacia:
            cislo = "J"
        elif "p" in anotacia:
            cislo = "M"

        if "1" in anotacia:
            pad = "Nom"
        elif "2" in anotacia:
            pad = "Gen"
        elif "3" in anotacia:
            pad = "Dat"
        elif "4" in anotacia:
            pad = "Aku"
        elif "5" in anotacia:
            pad = "Vok"
        elif "6" in anotacia:
            pad = "Lok"
        elif "7" in anotacia:
            pad = "Ins"

        c_objekty = Cislovka.query.filter(Cislovka.rod == rod).\
            filter(Cislovka.podrod == podrod).\
            filter(Cislovka.zak_tvar == zak_tvar)

        if c_objekty.count() == 0:
            cis = Cislovka(zak_tvar=zak_tvar, rod=rod, podrod=podrod)
            db.session.add(cis)
            c_objekty = []
            c_objekty.append(cis)

        for c in c_objekty:
            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == c.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=c.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.rod = rod
                sl.podrod = podrod
                sl.cislo = cislo
                sl.pad = pad
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_casticu(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        c_objekty = Castica.query.filter(Castica.zak_tvar == zak_tvar)

        if c_objekty.count() == 0:
            castica = Castica(zak_tvar=zak_tvar)
            db.session.add(castica)
            c_objekty = []
            c_objekty.append(castica)

        for c in c_objekty:
            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == c.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=c.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_spojku(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        s_objekty = Spojka.query.filter(Spojka.zak_tvar == zak_tvar)

        if s_objekty.count() == 0:
            spojka = Spojka(zak_tvar=zak_tvar)
            db.session.add(spojka)
            s_objekty = []
            s_objekty.append(spojka)

        for s in s_objekty:
            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == s.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=s.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_predlozku(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        predlozkovy_pad = None

        if "2" in anotacia:
            predlozkovy_pad = "Gen"
        elif "3" in anotacia:
            predlozkovy_pad = "Dat"
        elif "4" in anotacia:
            predlozkovy_pad = "Aku"
        elif "5" in anotacia:
            predlozkovy_pad = "Vok"
        elif "6" in anotacia:
            predlozkovy_pad = "Lok"
        elif "7" in anotacia:
            predlozkovy_pad = "Ins"

        p_objekty = Predlozka.query.filter(Predlozka.zak_tvar == zak_tvar)

        if p_objekty.count() == 0:
            predlozka = Predlozka(zak_tvar=zak_tvar, pady="")
            db.session.add(predlozka)
            p_objekty = []
            p_objekty.append(predlozka)

        for p in p_objekty:

            if predlozkovy_pad not in p.pady:
                p.pady += predlozkovy_pad+";"
                db.session.add(p)

            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == p.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=p.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_prislovku(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        if "x" in anotacia:
            stupen = 1
        elif "y" in anotacia:
            stupen = 2
        elif "z" in anotacia:
            stupen = 3

        p_objekty = Prislovka.query.filter(Prislovka.zak_tvar == zak_tvar)

        if p_objekty.count() == 0:
            prislovka = Prislovka(zak_tvar=zak_tvar)
            db.session.add(prislovka)
            p_objekty = []
            p_objekty.append(prislovka)

        for p in p_objekty:

            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == p.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=p.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.tvar = tvar
                sl.stupen = stupen
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_citoslovce(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        c_objekty = Citoslovce.query.filter(Citoslovce.zak_tvar == zak_tvar)

        if c_objekty.count() == 0:
            citoslovce = Citoslovce(zak_tvar=zak_tvar)
            db.session.add(citoslovce)
            c_objekty = []
            c_objekty.append(citoslovce)

        for c in c_objekty:

            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == c.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=c.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def zaloz_updatuj_ostatne(zak_tvar, tvar, anotacia):
    with flask_app.app_context():

        if zak_tvar[0] == "*":
            zak_tvar = zak_tvar[1:]

        pole_updatnutych_slov = []
        je_negacia = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        rod = None
        podrod = None
        cislo = None
        pad = None

        o_objekty = Ostatne.query.filter(Ostatne.zak_tvar == zak_tvar)

        if o_objekty.count() == 0:
            ostatne = Ostatne(zak_tvar=zak_tvar)
            db.session.add(ostatne)
            o_objekty = []
            o_objekty.append(ostatne)

        for o in o_objekty:

            sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
                filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
                filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).\
                filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
                filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
                filter(Slovo.sd_id == o.id).first()
            if not sl:
                sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba,
                           cas=cas, pricastie=pricastie, je_negacia=je_negacia, je_neurcitok=je_neurcitok,
                           je_prechodnik=je_prechodnik, cislo=cislo, sd_id=o.id, anotacia=anotacia,
                           zmenene=datetime.datetime.now())
            else:
                sl.tvar = tvar
                sl.anotacia = anotacia
                sl.zmenene = datetime.datetime.now()

            db.session.add(sl)

            db.session.commit()

            pole_updatnutych_slov.append(sl.id)

        return pole_updatnutych_slov


def insert_morfo_db(nazov_suboru):
    tvary_connection = pymysql.connect(host=T_HOST,
                                       user=T_USER,
                                       password=T_PASSWORD,
                                       db=T_DB_NAME,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with tvary_connection.cursor() as cursor:
            with open(nazov_suboru, newline='', encoding="utf-8") as morfo:
                morfo_reader = csv.reader(morfo, delimiter='\t')
                for m in morfo_reader:
                    print(m)
                    sql = "INSERT INTO tvary.morfo_db (zak_tvar, slovo_tvar, morfo_anotacia) VALUES(%s, %s, %s)"
                    cursor.execute(sql, (m[0], m[1], m[2]))
                    tvary_connection.commit()
    finally:
        tvary_connection.close()


def update_morfo_db():
    tvary_connection = pymysql.connect(host=T_HOST,
                                       user=T_USER,
                                       password=T_PASSWORD,
                                       db=T_DB_NAME,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
    morfo_connection = pymysql.connect(host=T_HOST,
                                       user=T_USER,
                                       password=T_PASSWORD,
                                       db=T_DB_NAME,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with morfo_connection.cursor() as mcursor:
            try:
                with tvary_connection.cursor() as cursor:
                    sql = "SELECT m.* FROM `tvary`.`morfo_db` m " +\
                     "WHERE " \
                     "ISNULL(m.slovo_id)=1"
                    # SUBSTRING(morfo_anotacia,1,1) in "('G'/*'G','J','D','E','O','T','N','P','S','A','V'*/) " \
                    cursor.execute(sql)
                    while True:
                        row = cursor.fetchone()
                        if row:
                            slovny_druh = row['morfo_anotacia'][0]

                            if slovny_druh == "S":
                                pole = zaloz_updatuj_podstatne_meno(row['zak_tvar'], row['slovo_tvar'],
                                                                    row['morfo_anotacia'])
                            elif slovny_druh in ("A", "G"):
                                pole = zaloz_updatuj_pridavne_meno(row['zak_tvar'], row['slovo_tvar'],
                                                                   row['morfo_anotacia'])
                            elif slovny_druh == "V":
                                pole = zaloz_updatuj_sloveso(row['zak_tvar'], row['slovo_tvar'],
                                                             row['morfo_anotacia'])
                            elif slovny_druh == "P":
                                pole = zaloz_updatuj_zameno(row['zak_tvar'], row['slovo_tvar'],
                                                            row['morfo_anotacia'])
                            elif slovny_druh == "N":
                                pole = zaloz_updatuj_cislovku(row['zak_tvar'], row['slovo_tvar'],
                                                              row['morfo_anotacia'])
                            elif slovny_druh == "T":
                                pole = zaloz_updatuj_casticu(row['zak_tvar'], row['slovo_tvar'],
                                                             row['morfo_anotacia'])
                            elif slovny_druh == "O":
                                pole = zaloz_updatuj_spojku(row['zak_tvar'], row['slovo_tvar'],
                                                            row['morfo_anotacia'])
                            elif slovny_druh == "E":
                                pole = zaloz_updatuj_predlozku(row['zak_tvar'], row['slovo_tvar'],
                                                               row['morfo_anotacia'])
                            elif slovny_druh == "D":
                                pole = zaloz_updatuj_prislovku(row['zak_tvar'], row['slovo_tvar'],
                                                               row['morfo_anotacia'])
                            elif slovny_druh == "J":
                                pole = zaloz_updatuj_citoslovce(row['zak_tvar'], row['slovo_tvar'],
                                                                row['morfo_anotacia'])
                            else:
                                pole = zaloz_updatuj_ostatne(row['zak_tvar'], row['slovo_tvar'],
                                                             row['morfo_anotacia'])

                            sql = "UPDATE tvary.morfo_db SET slovo_id=%s, zoznam_zmenenych_slov=%s WHERE id=%s"

                            if pole is None:
                                mcursor.execute("UPDATE tvary.morfo_db SET error_type='R' WHERE id=%s", row['id'])
                            else:
                                mcursor.execute(sql, (pole[-1], ",".join(str(x) for x in pole), row['id']))

                        morfo_connection.commit()

                        if row is None:
                            break
            finally:
                tvary_connection.close()
    finally:
        morfo_connection.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "insert_morfo_db":
            subor = sys.argv[2]
            insert_morfo_db(subor)
        elif command == "update_morfo_db":
            update_morfo_db()
    else:
        print("usage:\n\n\tdb_morfo.py [ insert_morfo_db | update_morfo_db ]")
