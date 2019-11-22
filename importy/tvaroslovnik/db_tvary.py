from app.app import flask_app
from app.db_models import *

import pymysql.cursors
from pyquery import PyQuery as pq
import requests as req
import sys

T_USER = 'tvary'
T_PASSWORD = 'tvary'
T_HOST = 'localhost'
T_DB_NAME = 'tvary'

C_USER = 'cogito'
C_PASSWORD = 'cogito'
C_HOST = 'localhost'
C_DB_NAME = 'cogito'

db.init_app(flask_app)


def uloz_tvar(cursor, idt, zaklad_id, tvar, ztvar, dtvaru):
    sql = "INSERT INTO `tvary`.`tvary`(`id`,`id_zakladneho_tvaru`,`tvar`,`data_zakladneho_tvaru`,`data_tvaru`) " \
          "VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (idt, zaklad_id, tvar, ztvar, dtvaru))


def spusti_download(fromr, tor):
    connection = pymysql.connect(host=T_HOST,
                                 user=T_USER,
                                 password=T_PASSWORD,
                                 db=T_DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            for j in range(fromr, tor+1):
                sql = "SELECT count(1) cnt FROM `tvary`.`tvary` WHERE `id`=%s"
                cursor.execute(sql, (j))
                result = cursor.fetchone()

                if (j % 50000) == 0:
                    print("ide j:"+str(j))

                if result['cnt'] == 0:
                    append = ""

                    if j % 5 == 0:
                        append = "........................"

                    url = "http://tvaroslovnik.ics.upjs.sk/servlet/id/{}".format(j)

                    print("downloading:"+url+append)

                    resp = req.get(url)
                    doc = pq(resp.text)

                    slovo = doc("#wordPanel").html()
                    zakladny_popis = ""
                    horny_popis = doc(".word-info-block")
                    for my_div in horny_popis.items():
                        if "<span class=\"greyed\">Slovný druh: </span><span>" in my_div.html():
                            zakladny_popis=my_div.html().replace("<span class=\"greyed\">Slovný druh: </span><span>",
                                                                 "").replace("</span>", "").replace("&#13;", "").\
                                replace("\n", "")
                        if "<span class=\"greyed\">Opis: </span><span>" in my_div.html():
                            zakladny_popis += "|"+my_div.html().replace("<span class=\"greyed\">Opis: </span><span>",
                                                                        "").replace("</span>", "").replace("&#13;", "")\
                                                                        .replace("\n", "")

                    slova = doc(".word")

                    for wdiv in slova.items():
                        anchor = wdiv.find('a').attr("href")
                        aktualny_tvar_slova = wdiv.find('a').html()
                        idslova = anchor.replace("/servlet/id/", "")
                        popisslova = wdiv.find("em").text()
                        uloz_tvar(cursor, idslova, j, aktualny_tvar_slova, zakladny_popis, popisslova)

                    connection.commit()

    finally:
        connection.close()


def zaloz_podstatne_meno(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        sloveso_id = None
        je_negacia = None
        id_pm = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        zvratnost = None

        if 'pád: nominatív' in data_tvaru:
            pad = 'Nom'
        elif 'pád: genitív' in data_tvaru:
            pad = 'Gen'
        elif 'pád: datív' in data_tvaru:
            pad = 'Dat'
        elif 'pád: akuzatív' in data_tvaru:
            pad = 'Aku'
        elif 'pád: vokatív' in data_tvaru:
            pad = 'Vok'
        elif 'pád: lokál' in data_tvaru:
            pad = 'Lok'
        elif 'pád: inštrumentál' in data_tvaru:
            pad = 'Ins'

        if 'zvratnosť: sa' in data_tvaru:
            zvratnost = "sa"
        elif 'zvratnosť: si' in data_tvaru:
            zvratnost = "si"

        cislo = "J"

        if "číslo: množ" in data_tvaru:
            cislo = "M"
        elif "číslo: pomno" in data_tvaru:
            cislo = "P"

        if 'podstatné meno' in data_zakladneho_tvaru:
            if 'rod: stredný' in data_tvaru:
                rod = "S"
            elif 'rod: mužský' in data_tvaru:
                rod = "M"
                if 'podrod: život' in data_tvaru:
                    podrod = "Z"
                else:
                    podrod = "N"
            elif 'rod: žens' in data_tvaru:
                rod = "Z"
            id_pm = id_zak_sd
        elif 'slovesné podstatné meno' in data_tvaru:
            sloveso_id = id_zak_sd
            je_negacia = "N"
            rod = "S"

            if 'negácia: ' in data_tvaru:
                je_negacia = "A"

            pm_objekt = PodstatneMeno.query.filter(PodstatneMeno.sloveso_id == sloveso_id).\
                filter(PodstatneMeno.je_negacia == je_negacia). \
                filter(PodstatneMeno.rod == rod). \
                filter(PodstatneMeno.zvratnost == zvratnost). \
                filter(PodstatneMeno.podrod == podrod).first()

            if pm_objekt:
                id_pm = pm_objekt.id

        if id_pm:
            pm = PodstatneMeno.query.get(id_pm)
        else:
            pm = PodstatneMeno.query.filter(PodstatneMeno.zak_tvar == tvar).\
                filter(PodstatneMeno.je_negacia == je_negacia). \
                filter(PodstatneMeno.rod == rod). \
                filter(PodstatneMeno.zvratnost == zvratnost). \
                filter(PodstatneMeno.podrod == podrod).first()

        if not pm:
            pm = PodstatneMeno(zak_tvar=tvar, rod=rod, podrod=podrod,
                               sloveso_id=sloveso_id, je_negacia=je_negacia,
                               zvratnost=zvratnost)
            db.session.add(pm)

        sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == pm.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=pm.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_pridavne_meno(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        sloveso_id = None
        je_negacia = None
        id_pm = None
        stupen = None
        sposob = None
        cas = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        pricastie = None
        je_privlastnovacie = "N"
        zvratnost = None

        if 'pád: nominatív' in data_tvaru:
            pad = 'Nom'
        elif 'pád: genitív' in data_tvaru:
            pad = 'Gen'
        elif 'pád: datív' in data_tvaru:
            pad = 'Dat'
        elif 'pád: akuzatív' in data_tvaru:
            pad = 'Aku'
        elif 'pád: vokatív' in data_tvaru:
            pad = 'Vok'
        elif 'pád: lokál' in data_tvaru:
            pad = 'Lok'
        elif 'pád: inštrumentál' in data_tvaru:
            pad = 'Ins'

        cislo = "J"

        if "číslo: množ" in data_tvaru:
            cislo = "M"
        elif "číslo: pomno" in data_tvaru:
            cislo = "P"

        if 'rod: stredný' in data_tvaru:
            rod = "S"
        elif 'rod: mužský' in data_tvaru:
            rod = "M"
            if 'podrod: život' in data_tvaru:
                podrod = "Z"
            else:
                podrod = "N"
        elif 'rod: žens' in data_tvaru:
            rod = "Z"
        elif 'rod: žitný' in data_tvaru:
                rod = "I"

        if 'zvratnosť: sa' in data_tvaru:
            zvratnost = "sa"
        elif 'zvratnosť: si' in data_tvaru:
            zvratnost = "si"

        if 'stupeň: prvý' in data_tvaru:
            stupen = "1"
        elif 'stupeň: druhý' in data_tvaru:
            stupen = "2"
        elif 'stupeň: tretí' in data_tvaru:
            stupen = "3"

        if 'príčastie' in data_tvaru:
            sloveso_id = id_zak_sd
            je_negacia = "N"

            if 'negácia: ' in data_tvaru:
                je_negacia = "A"

            prid_meno_obj = PridavneMeno.query.filter(PridavneMeno.sloveso_id == sloveso_id).\
                filter(PridavneMeno.je_negacia == je_negacia).\
                filter(PridavneMeno.je_privlastnovacie == je_privlastnovacie). \
                filter(PridavneMeno.zvratnost == zvratnost). \
                first()

            if prid_meno_obj:
                id_pm = prid_meno_obj.id

            if 'činné príčastie' in data_tvaru:
                pricastie = "C"
            elif 'trpné príčastie' in data_tvaru:
                pricastie = "T"
            elif 'minulé príčastie' in data_tvaru:
                pricastie = "M"
        else:
            id_pm = id_zak_sd

        if id_pm:
            pm = PridavneMeno.query.get(id_pm)
        else:
            pm = PridavneMeno.query.filter(PridavneMeno.zak_tvar == tvar).\
                filter(PridavneMeno.je_negacia == je_negacia).\
                filter(PridavneMeno.je_privlastnovacie == je_privlastnovacie). \
                filter(PridavneMeno.zvratnost == zvratnost). \
                first()

        if 'prídavné meno privlastňovacie' in data_zakladneho_tvaru:
            je_privlastnovacie = "A"

        if not pm:
            pm = PridavneMeno(zak_tvar=tvar, sloveso_id=sloveso_id, je_negacia=je_negacia,
                              je_privlastnovacie=je_privlastnovacie, zvratnost=zvratnost)
            db.session.add(pm)

        sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == pm.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=pm.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_sloveso(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        sloveso = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_neurcitok = "N"
        je_prechodnik = "N"
        osoba = None
        pozitivne_sloveso_id = None
        zvratnost = None

        if 'pád: nominatív' in data_tvaru:
            pad = 'Nom'
        elif 'pád: genitív' in data_tvaru:
            pad = 'Gen'
        elif 'pád: datív' in data_tvaru:
            pad = 'Dat'
        elif 'pád: akuzatív' in data_tvaru:
            pad = 'Aku'
        elif 'pád: vokatív' in data_tvaru:
            pad = 'Vok'
        elif 'pád: lokál' in data_tvaru:
            pad = 'Lok'
        elif 'pád: inštrumentál' in data_tvaru:
            pad = 'Ins'

        je_negacia = "N"

        if 'negácia: ne-' in data_tvaru:
            je_negacia = "A"

        cislo = None

        if "číslo: množ" in data_tvaru:
            cislo = "M"
        elif "číslo: pomno" in data_tvaru:
            cislo = "P"

        if 'rod: stredný' in data_tvaru:
            rod = "S"
        elif 'rod: mužský' in data_tvaru:
            rod = "M"
            if 'podrod: život' in data_tvaru:
                podrod = "Z"
            else:
                podrod = "N"
        elif 'rod: žens' in data_tvaru:
            rod = "Z"
        elif 'rod: žitný' in data_tvaru:
                rod = "I"

        if 'osoba: prvá' in data_tvaru:
            osoba = "1"
        elif 'osoba: druhá' in data_tvaru:
            osoba = "2"
        elif 'osoba: tretia' in data_tvaru:
            osoba = "3"

        if 'čas: prítomný' in data_tvaru:
            cas = "P"
        elif 'čas: minulý' in data_tvaru:
            cas = "M"
        elif 'čas: budúci' in data_tvaru:
            cas = "B"

        if 'forma: neurčitok' in data_tvaru:
            je_neurcitok = "A"

        if 'spôsob: rozkazovací' in data_tvaru:
            sposob = "R"
        elif 'spôsob: oznamovací' in data_tvaru:
            sposob = "O"

        if 'forma: prechodník' in data_tvaru:
            je_prechodnik = "A"

        if 'zvratnosť: sa' in data_tvaru:
            zvratnost = "sa"
        elif 'zvratnosť: si' in data_tvaru:
            zvratnost = "si"

        if id_zak_sd:
            materske_sloveso = Sloveso.query.get(id_zak_sd)
            if je_negacia == "A":
                pozitivne_sloveso_id = materske_sloveso.id
                sloveso = Sloveso.query.filter(Sloveso.zak_tvar == "ne"+materske_sloveso.zak_tvar).\
                    filter(Sloveso.je_negacia == je_negacia).\
                    filter(Sloveso.zvratnost == zvratnost).\
                    first()
            else:
                sloveso = Sloveso.query.get(id_zak_sd)
        else:
            sloveso = Sloveso.query.filter(Sloveso.zak_tvar == tvar). \
                filter(Sloveso.je_negacia == je_negacia). \
                filter(Sloveso.zvratnost == zvratnost). \
                first()

        if not sloveso:
            sloveso = Sloveso(zak_tvar=tvar, je_negacia=je_negacia, pozitivne_sloveso_id=pozitivne_sloveso_id,
                              zvratnost=zvratnost)
            db.session.add(sloveso)

        sl = Slovo.query.filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == sloveso.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=sloveso.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_spojku(tvar):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None
        zvratnost = None

        spojka = Spojka.query.filter(Spojka.zak_tvar == tvar).first()

        if not spojka:
            spojka = Spojka(zak_tvar=tvar)
            db.session.add(spojka)

        sl = Slovo.query. \
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod). \
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob). \
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia). \
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik). \
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost). \
            filter(Slovo.sd_id == spojka.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=spojka.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_citoslovce(tvar):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None
        zvratnost = None

        cit = Citoslovce.query.filter(Spojka.zak_tvar == tvar).first()

        if not cit:
            cit = Citoslovce(zak_tvar=tvar)
            db.session.add(cit)

        sl = Slovo.query.\
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == cit.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=cit.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_predlozku(tvar, data_tvaru):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None
        zvratnost = None

        pady = ""

        if 'nominatív' in data_tvaru:
            pady += 'Nom;'

        if 'genitív' in data_tvaru:
            pady += 'Gen;'

        if 'datív' in data_tvaru:
            pady += 'Dat;'

        if 'akuzatív' in data_tvaru:
            pady += 'Aku;'

        if 'vokatív' in data_tvaru:
            pady += 'Vok;'

        if 'lokál' in data_tvaru:
            pady += 'Lok;'

        if 'inštrumentál' in data_tvaru:
            pady += 'Ins;'

        pred = Predlozka.query.filter(Predlozka.zak_tvar == tvar).first()

        if not pred:
            pred = Predlozka(zak_tvar=tvar, pady=pady)
            db.session.add(pred)
        else:
            pred.pady = pady
            db.session.add(pred)

        sl = Slovo.query.\
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == pred.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=pred.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_cislovku(tvar, data_tvaru, id_zak_sd):
    with flask_app.app_context():
        rod = None
        podrod = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None

        pad = None
        zvratnost = None

        if 'nominatív' in data_tvaru:
            pad = 'Nom'
        elif 'genitív' in data_tvaru:
            pad = 'Gen'
        elif 'datív' in data_tvaru:
            pad = 'Dat'
        elif 'akuzatív' in data_tvaru:
            pad = 'Aku'
        elif 'vokatív' in data_tvaru:
            pad = 'Vok'
        elif 'lokál' in data_tvaru:
            pad = 'Lok'
        elif 'inštrumentál' in data_tvaru:
            pad = 'Ins'

        if "číslo: množ" in data_tvaru:
            cislo = "M"
        elif "číslo: pomno" in data_tvaru:
            cislo = "P"
        elif "číslo: jednotn" in data_tvaru:
            cislo = "J"

        if 'rod: stredný' in data_tvaru:
            rod = "S"
        elif 'rod: mužský' in data_tvaru:
            rod = "M"
            if 'podrod: život' in data_tvaru:
                podrod = "Z"
            else:
                podrod = "N"
        elif 'rod: žens' in data_tvaru:
            rod = "Z"

        if id_zak_sd:
            cislovka = Cislovka.query.get(id_zak_sd)
        else:
            cislovka = Cislovka.query.filter(Cislovka.zak_tvar == tvar).\
                filter(Cislovka.rod == rod).filter(Cislovka.podrod == podrod).\
                filter(Cislovka.cislo == cislo).first()

            if not cislovka:
                cislovka = Cislovka(zak_tvar=tvar, rod=rod, podrod=podrod, cislo=cislo)
                db.session.add(cislovka)

        sl = Slovo.query.\
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == cislovka.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=cislovka.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_prislovku(tvar, data_tvaru, id_zak_sd):
    with flask_app.app_context():
        rod = None
        podrod = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None

        pad = None
        zvratnost = None

        if 'stupeň: prvý' in data_tvaru:
            stupen = "1"
        elif 'stupeň: druhý' in data_tvaru:
            stupen = "2"
        elif 'stupeň: tretí' in data_tvaru:
            stupen = "3"

        if id_zak_sd:
            prislovka = Prislovka.query.get(id_zak_sd)
        else:
            prislovka = Prislovka.query.filter(Prislovka.zak_tvar == tvar).first()

            if not prislovka:
                prislovka = Prislovka(zak_tvar=tvar)
                db.session.add(prislovka)

        sl = Slovo.query.\
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == prislovka.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=prislovka.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_zameno(tvar, data_tvaru, id_zak_sd):
    with flask_app.app_context():
        rod = None
        podrod = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None

        pad = None
        zvratnost = None

        if 'nominatív' in data_tvaru:
            pad = 'Nom'
        elif 'genitív' in data_tvaru:
            pad = 'Gen'
        elif 'datív' in data_tvaru:
            pad = 'Dat'
        elif 'akuzatív' in data_tvaru:
            pad = 'Aku'
        elif 'vokatív' in data_tvaru:
            pad = 'Vok'
        elif 'lokál' in data_tvaru:
            pad = 'Lok'
        elif 'inštrumentál' in data_tvaru:
            pad = 'Ins'

        if "číslo: množ" in data_tvaru:
            cislo = "M"
        elif "číslo: pomno" in data_tvaru:
            cislo = "P"
        elif "číslo: jednotn" in data_tvaru:
            cislo = "J"

        if 'rod: stredný' in data_tvaru:
            rod = "S"
        elif 'rod: mužský' in data_tvaru:
            rod = "M"
            if 'podrod: život' in data_tvaru:
                podrod = "Z"
            else:
                podrod = "N"
        elif 'rod: žens' in data_tvaru:
            rod = "Z"

        if id_zak_sd:
            zameno = Zameno.query.get(id_zak_sd)
        else:
            zameno = Zameno.query.filter(Zameno.zak_tvar == tvar).\
                filter(Zameno.rod == rod).\
                filter(Zameno.podrod == podrod).\
                filter(Zameno.cislo == cislo).\
                first()

            if not zameno:
                zameno = Zameno(zak_tvar=tvar, rod=rod, podrod=podrod, cislo=cislo)
                db.session.add(zameno)

        sl = Slovo.query.\
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == zameno.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=zameno.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_casticu(tvar):
    with flask_app.app_context():
        rod = None
        podrod = None
        pad = None
        stupen = None
        sposob = None
        cas = None
        pricastie = None
        je_negacia = None
        je_neurcitok = None
        je_prechodnik = None
        osoba = None
        cislo = None

        cast = Castica.query.filter(Castica.zak_tvar == tvar).first()

        zvratnost = None
        if not cast:
            cast = Castica(zak_tvar=tvar)
            db.session.add(cast)

        sl = Slovo.query.\
            filter(Slovo.tvar == tvar).filter(Slovo.pad == pad).filter(Slovo.rod == rod).\
            filter(Slovo.podrod == podrod).filter(Slovo.stupen == stupen).filter(Slovo.sposob == sposob).\
            filter(Slovo.cas == cas).filter(Slovo.pricastie == pricastie).filter(Slovo.je_negacia == je_negacia).\
            filter(Slovo.je_neurcitok == je_neurcitok).filter(Slovo.je_prechodnik == je_prechodnik).\
            filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).filter(Slovo.zvratnost == zvratnost).\
            filter(Slovo.sd_id == cast.id).first()

        if not sl:
            sl = Slovo(tvar=tvar, pad=pad, rod=rod, podrod=podrod, stupen=stupen, sposob=sposob, osoba=osoba, cas=cas,
                       pricastie=pricastie, je_negacia=je_negacia, zvratnost=zvratnost,
                       je_neurcitok=je_neurcitok, je_prechodnik=je_prechodnik, cislo=cislo, sd_id=cast.id)
            db.session.add(sl)

        db.session.commit()

        return sl.id


def zaloz_slovo(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd):
    if 'podstatné meno' in data_zakladneho_tvaru or 'podstatné meno' in data_tvaru:
        return zaloz_podstatne_meno(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd)
    elif 'prídavné meno' in data_zakladneho_tvaru or 'príčastie' in data_tvaru:
        return zaloz_pridavne_meno(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd)
    elif 'sloveso' in data_zakladneho_tvaru:
        return zaloz_sloveso(tvar, data_zakladneho_tvaru, data_tvaru, id_zak_sd)
    elif 'spojka' in data_zakladneho_tvaru:
        return zaloz_spojku(tvar)
    elif 'citoslovce' in data_zakladneho_tvaru:
        return zaloz_citoslovce(tvar)
    elif 'predložka' in data_zakladneho_tvaru:
        return zaloz_predlozku(tvar, data_tvaru)
    elif 'častica' in data_zakladneho_tvaru:
        return zaloz_casticu(tvar)
    elif 'číslovka' in data_zakladneho_tvaru:
        return zaloz_cislovku(tvar, data_tvaru, id_zak_sd)
    elif 'príslovka' in data_zakladneho_tvaru:
        return zaloz_prislovku(tvar, data_tvaru, id_zak_sd)
    elif 'zámeno' in data_zakladneho_tvaru:
        return zaloz_zameno(tvar, data_tvaru, id_zak_sd)


def transform_db(app, fromr, tor):
    tvary_connection = pymysql.connect(host=T_HOST,
                                       user=T_USER,
                                       password=T_PASSWORD,
                                       db=T_DB_NAME,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with tvary_connection.cursor() as cursor:
            for j in range(fromr, tor+1):
                sql = "SELECT t1.*, sl.sd_id parent_sd_id FROM `tvary`.`tvary` t1 " \
                      "LEFT OUTER JOIN tvary.tvary t2 ON t1.id_zakladneho_tvaru=t2.id " \
                      "LEFT OUTER JOIN cogito.sl ON sl.id=t2.slovo_id " \
                      "WHERE t1.`id`=%s AND ISNULL(t1.slovo_id)=1"
                cursor.execute(sql, j)
                result = cursor.fetchone()

                if result:
                    vypis = "Ide slovo s id:"+str(j)

                    if j % 5 == 0:
                        vypis += "*****************************"

                    print(vypis)
                    slovo_id = zaloz_slovo(result['tvar'], result['data_zakladneho_tvaru'], result['data_tvaru'], result['parent_sd_id'])
                    sql = "UPDATE tvary.tvary SET slovo_id=%s WHERE id=%s"
                    cursor.execute(sql, (slovo_id, result['id']))
                else:
                    print("No records found execute update slovo_id=null")

                tvary_connection.commit()
    finally:
        tvary_connection.close()


def update_predlozky(app):
    tvary_connection = pymysql.connect(host=T_HOST,
                                       user=T_USER,
                                       password=T_PASSWORD,
                                       db=T_DB_NAME,
                                       charset='utf8mb4',
                                       cursorclass=pymysql.cursors.DictCursor)
    try:
        with tvary_connection.cursor() as cursor:
            sql = "SELECT t1.*, sl.sd_id parent_sd_id FROM `tvary`.`tvary` t1 " \
                  "LEFT OUTER JOIN tvary.tvary t2 ON t1.id_zakladneho_tvaru=t2.id " \
                  "LEFT OUTER JOIN cogito.sl ON sl.id=t2.slovo_id " \
                  "JOIN cogito.sd_predlozka p ON sl.sd_id=p.id "
            cursor.execute(sql)

            while True:
                row = cursor.fetchone()
                if row:
                    i = zaloz_predlozku(row['tvar'], row['data_zakladneho_tvaru'])
                    print(str(i))

                if row == None:
                    break

            tvary_connection.commit()
    finally:
        tvary_connection.close()


def zmaz_pridavne_meno_okrem(zak_tvar, okrem_sd):
    cogito_connection = pymysql.connect(host=C_HOST,
                                        user=C_USER,
                                        password=C_PASSWORD,
                                        db=C_DB_NAME,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
    try:
        file = open("sqlResult.txt", "a")

        with cogito_connection.cursor() as cursor:
            sql = "SELECT s0.id id FROM sd s0 JOIN sd_prid_m p0 on s0.id=p0.id " +\
                  "WHERE s0.zak_tvar=%s and s0.id!=%s"
            cursor.execute(sql, (zak_tvar, okrem_sd))

            while True:
                row = cursor.fetchone()
                if row:
                    file.write("DELETE FROM sl WHERE sd_id="+str(row['id'])+";\n")
                    file.write("DELETE FROM sd_prid_m WHERE id="+str(row['id'])+";\n")
                    file.write("DELETE FROM sd WHERE id="+str(row['id'])+";\n")

                if row == None:
                    break

        file.close()

    finally:
        cogito_connection.close()


def zmaz_duplicitne_prid_m():
    cogito_connection = pymysql.connect(host=C_HOST,
                                        user=C_USER,
                                        password=C_PASSWORD,
                                        db=C_DB_NAME,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)
    try:
        with cogito_connection.cursor() as cursor:
            sql = "SELECT sd0.zak_tvar, p0.sloveso_id, p0.je_privlastnovacie, p0.je_negacia, p0.zvratnost, " +\
                  "min(sd0.id) min_id " +\
                  "FROM sd_prid_m p0 join sd sd0 on sd0.id=p0.id " +\
                  "WHERE (sd0.zak_tvar, IFNULL(p0.sloveso_id,-1), IFNULL(p0.je_privlastnovacie,''), " +\
                  "IFNULL(p0.je_negacia,''), IFNULL(p0.zvratnost,'')) in (" +\
                        "SELECT sd1.zak_tvar, IFNULL(p1.sloveso_id,-1), IFNULL(p1.je_privlastnovacie,''), " +\
                  "IFNULL(p1.je_negacia,''), IFNULL(p1.zvratnost,'') FROM sd_prid_m p1 join sd sd1 on sd1.id=p1.id " +\
                    "GROUP BY sd1.zak_tvar, p1.sloveso_id, p1.je_privlastnovacie, p1.je_negacia, p1.zvratnost " +\
                    "HAVING count(1)>1 ) " +\
                    "GROUP BY sd0.zak_tvar, p0.sloveso_id, p0.je_privlastnovacie, p0.je_negacia, p0.zvratnost "
            cursor.execute(sql)

            while True:
                row = cursor.fetchone()
                if row:
                    zmaz_pridavne_meno_okrem(row['zak_tvar'], row['min_id'])

                if row == None:
                    break

            cogito_connection.commit()
    finally:
        cogito_connection.close()


def zmaz_duplicitne_slova():
    zmaz_duplicitne_prid_m()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "spusti_download":
            fr = int(sys.argv[2])
            tr = int(sys.argv[3])
            print("running from :" + str(fr) + " to:" + str(tr))
            spusti_download(fr, tr)
        elif command == "transform_db":
            fr = int(sys.argv[2])
            tr = int(sys.argv[3])
            transform_db(flask_app, fr, tr)
        elif command == "zmaz_duplicitne_slova":
            zmaz_duplicitne_slova()
    else:
        print("usage:\n\n\tdb_tvary.py [ spusti_download | transform_db ]")
