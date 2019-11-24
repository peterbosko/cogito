from app.db_models import *
from sqlalchemy import or_
from pyquery import PyQuery as pq
from app.c_helper import *
import re
from app.c_service import *
import json
import jsonpickle
import html
import datetime


def vrat_slova_zacinajuce_na(vyraz, presna_zhoda):
    if len(vyraz) > 0:
        prvy_znak = vyraz[0]

        prvy_znak_upper = False

        if prvy_znak == prvy_znak.upper():
            prvy_znak_upper = True

        if prvy_znak_upper:
            pole_slov = Slovo.query.filter(or_(Slovo.tvar == vyraz, Slovo.tvar == vyraz.lower()))
        else:
            pole_slov = Slovo.query.filter(Slovo.tvar == vyraz)

        pole_slov = pole_slov.filter(Slovo.anotacia.isnot(None))

        if pole_slov.count() == 0:
            if prvy_znak_upper:
                pole_slov = Slovo.query.filter(or_(Slovo.tvar.like(vyraz + "%"), Slovo.tvar.like(vyraz.lower()+"%")))\
                    .filter(Slovo.anotacia.isnot(None))\
                    .paginate(1, 15, False).items
            else:
                pole_slov = Slovo.query.filter(Slovo.tvar.like(vyraz + "%")).filter(Slovo.anotacia.isnot(None))\
                    .paginate(1, 15, False).items

        return [{key: value for (key, value) in row.exportuj(prvy_znak_upper).__dict__.items()} for row in pole_slov]
    else:
        return None


def vrat_pole_slov_z_textu(html, parent_slovo_id=None):
    pole = []

    celkom_slov = 0
    jednoznacnych_slov = 0

    # html = vyrob_korektne_html_z_editora(html)

    obsah_p = pq(html).contents()

    for content in obsah_p.items():
        # print("ide horny loop:"+content.outerHtml())
        if content.is_("span"):
            # print("Kontent je span:" + str(content.hasClass("slovnik"))+"|")
            s_id = None

            if content.hasClass("s"):
                s_id = int(content.attr('sid'))

            s, u, p = vrat_pole_slov_z_textu(content.outerHtml(), s_id)
            celkom_slov += s
            jednoznacnych_slov += u
            pole.extend(p)
        else:
            # print("Kontent je text:" + content.text()+"|")
            text = daj_medzery_pred_specialne_znaky(content.text())

            slova_to_check = re.split(r'\s', text)

            for s in slova_to_check:
                if s:

                    if pq(html).is_("span") and pq(html).hasClass("s"):
                        parent_slovo_id = int(pq(html).attr("sid"))

                    v_slovo = vrat_slovo(s, parent_slovo_id)

                    if not v_slovo.neprekl_vyraz:
                        celkom_slov += 1

                    if parent_slovo_id and parent_slovo_id == v_slovo.id_slova:
                        v_slovo.bolo_vybrate = True

                    if ((not v_slovo.je_viacej_v_slovniku) and v_slovo.je_v_slovniku
                            and not v_slovo.neprekl_vyraz) or v_slovo.bolo_vybrate:
                        jednoznacnych_slov += 1

                    pole.append(v_slovo)

    return celkom_slov, jednoznacnych_slov, pole


def serializuj_pole_slov(pole):

    vysledok = ""

    i = 0

    for slovo in pole:
        cl = "s"

        if not slovo.je_v_slovniku:
            cl = "n"

        if slovo.je_viacej_v_slovniku and not slovo.bolo_vybrate:
            cl = "m"

        if slovo.neprekl_vyraz:
            prilep = ""

            if len(pole) > i + 1:
                prilep = "&nbsp;"

            if slovo.je_cislo:
                vysledok += str(slovo.neprekl_vyraz) + prilep
            else:
                vysledok += slovo.neprekl_vyraz+prilep
        else:
            prilep = ""

            if len(pole) > i+1:
                if not pole[i+1].neprekl_vyraz or pole[i+1].je_cislo:
                    prilep = "&nbsp;"

            vysledok += "<span class='{cl}' sid='{id}'>{slovo}</span>".format(
                slovo=slovo.tvar, id=slovo.id_slova, cl=cl)+prilep

        i += 1

    return vysledok


def serializuj_pole_slov_do_anotacie(pole):
    vysledok = ""

    i = 0
    for slovo in pole:
        prilep = ""

        if len(pole) > i + 1:
            prilep = " "

        if slovo.neprekl_vyraz:
            if slovo.je_cislo:
                vysledok += str(slovo.neprekl_vyraz) + prilep
            else:
                vysledok += slovo.neprekl_vyraz + prilep
        else:
            anot = ""

            if slovo.anotacia:
                anot = slovo.anotacia

            vysledok += "{id}>{zak_tvar}>{slovo}/{anotacia}".format(slovo=slovo.tvar, anotacia=anot, id=i,
                                                                    zak_tvar=slovo.zak_tvar)+prilep

        i += 1
    return vysledok


def kontrola_slov_v_kontexte(data):

    result = KontrolaSlovResponse()

    doc = pq(data)

    celkom_slov = 0

    jednoznacnych_slov = 0

    result.data = ""

    for p in doc("p"):

        pole_slov = []

        obsah_p = pq(p).html()

        slov, jednoznacnych, pole = vrat_pole_slov_z_textu(obsah_p)

        celkom_slov += slov

        jednoznacnych_slov += jednoznacnych

        pole_slov.extend(pole)

        result.data += "<p>" + serializuj_pole_slov(pole_slov) + "</p>"

    result.uspesnost = round(jednoznacnych_slov/celkom_slov * 100, 2)

    return result


def vrat_ciste_slova_s_anotaciou(data):

    vysledok = ""

    doc = pq(data)

    for p in doc("p"):

        obsah_p = pq(p).html()

        slov, jednoznacnych, pole = vrat_pole_slov_z_textu(obsah_p)

        vysledok += serializuj_pole_slov_do_anotacie(pole)+"\n"

    return vysledok


def serializuj_pole_slov(pole):

    vysledok = ""

    i = 0

    for slovo in pole:
        cl = "s"

        if not slovo.je_v_slovniku:
            cl = "n"

        if slovo.je_viacej_v_slovniku and not slovo.bolo_vybrate:
            cl = "m"

        if slovo.neprekl_vyraz:
            prilep = ""

            if len(pole) > i + 1:
                prilep = "&nbsp;"

            if slovo.je_cislo:
                vysledok += str(slovo.neprekl_vyraz) + prilep
            else:
                vysledok += slovo.neprekl_vyraz+prilep
        else:
            prilep = ""

            if len(pole) > i+1:
                if not pole[i+1].neprekl_vyraz or pole[i+1].je_cislo:
                    prilep = "&nbsp;"

            vysledok += "<span class='{cl}' sid='{id}'>{slovo}</span>".format(
                slovo=slovo.tvar, id=slovo.id_slova, cl=cl)+prilep

        i += 1

    return vysledok


def serializuj_pole_slov_do_anotacie(pole):
    vysledok = ""

    i = 0
    for slovo in pole:
        prilep = ""

        if len(pole) > i + 1:
            prilep = " "

        if slovo.neprekl_vyraz:
            if slovo.je_cislo:
                vysledok += str(slovo.neprekl_vyraz) + prilep
            else:
                vysledok += slovo.neprekl_vyraz + prilep
        else:
            anot = ""

            if slovo.anotacia:
                anot = slovo.anotacia

            vysledok += "{id}>{zak_tvar}>{slovo}/{anotacia}".format(slovo=slovo.tvar, anotacia=anot, id=i,
                                                                    zak_tvar=slovo.zak_tvar)+prilep

        i += 1
    return vysledok


