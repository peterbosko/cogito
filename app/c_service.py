from app.db_models import *
from sqlalchemy import or_
from pyquery import PyQuery as pq
from app.c_helper import *
from app.kt_models import *
import re
import json
import jsonpickle
import html
import datetime


def daj_popis_usera(id_usera):
    if id_usera:
        u = User.query.get(id_usera)
        return "{0} {1}".format(u.meno, u.priezvisko)
    return ""


def nahrad_bodky_v_cislach(kontext):
    bodky = []
    for i, m in enumerate(re.finditer('\\.', kontext)):
        if len(kontext) > m.start()+1 and kontext[m.start()+1].isdigit():
            bodky.append(m.start())

    start_index = 0

    vysledok = ""

    for bodka in bodky:
        vysledok += kontext[start_index:bodka]+"_bodka_"
        start_index = bodka+1

    vysledok += kontext[start_index:len(kontext)]

    return vysledok


def vyrob_porovnatelny_string(string):
    return html.unescape(string).replace("<p>", "").replace("</p>", "").replace("\n", "")


def loguj(request):
    usr_id = None

    if 'logged' in session.keys():
        usr_id = int(session["logged"])

    url = request.url

    if len(url) > 2000:
        url = url[:2000]

    ua = request.user_agent

    if ua:
        ua_string = ""

        if ua.platform:
            ua_string += "Platform:"+ua.platform
        if ua.browser:
            ua_string += " Browser:"+ua.browser
        if ua.version:
            ua_string += " Version:"+ua.version
    else:
        ua_string = "unknown-unknown-unknown"

    log_zaznam = Log(IP=request.remote_addr, url=url, user_id=usr_id, cas=datetime.datetime.now(),
                     user_agent=ua_string)
    db.session.add(log_zaznam)
    db.session.commit()


def vrat_slovo(slovo, ids=None):

    vysledok_slovo = SlovoVKontexte()

    if slovo and obsahuje_cisla(slovo):
        vysledok_slovo.neprekl_vyraz = daj_cislo(slovo)
        vysledok_slovo.je_cislo = True
        vysledok_slovo.tvar = slovo
        return vysledok_slovo

    je_upper = slovo[0] == slovo[0].upper()

    lower_sl = slovo[0].lower()

    if len(slovo) > 1:
        lower_sl += slovo[1:]

    if je_upper:
        if ids:
            sl = Slovo.query.filter(Slovo.id == ids).filter(Slovo.tvar == slovo).filter(Slovo.anotacia.isnot(None)).\
                filter(Slovo.anotacia != "")
        else:
            sl = Slovo.query.filter(Slovo.tvar == slovo).filter(Slovo.anotacia.isnot(None)).filter(Slovo.anotacia != "")
        if sl.count() == 0:
            if ids:
                sl = Slovo.query.filter(Slovo.id == ids).filter(Slovo.tvar == lower_sl)\
                    .filter(Slovo.anotacia.isnot(None)).filter(Slovo.anotacia != "")
            else:
                sl = Slovo.query.filter(Slovo.tvar == lower_sl).filter(Slovo.anotacia.isnot(None)).\
                    filter(Slovo.anotacia != "")
    else:
        if ids:
            sl = Slovo.query.filter(Slovo.id == ids).filter(Slovo.tvar == slovo).filter(Slovo.anotacia.isnot(None)).\
                filter(Slovo.anotacia != "")
        else:
            sl = Slovo.query.filter(Slovo.tvar == slovo).filter(Slovo.anotacia.isnot(None)).filter(Slovo.anotacia != "")

    if sl.count() == 0:
        vysledok_slovo.id_slova = None
        vysledok_slovo.je_v_slovniku = False
        vysledok_slovo.je_viacej_v_slovniku = False
        vysledok_slovo.slovo = None
        vysledok_slovo.tvar = slovo
        vysledok_slovo.popis = None
        vysledok_slovo.cely_popis_slova = None
        vysledok_slovo.anotacia = "???????"
    elif sl.count() == 1:
        vysledok_slovo.id_slova = sl.first().id
        vysledok_slovo.je_v_slovniku = True
        vysledok_slovo.je_viacej_v_slovniku = False
        vysledok_slovo.slovo = sl.first().exportuj(je_upper)
        vysledok_slovo.tvar = slovo
        vysledok_slovo.zak_tvar = vysledok_slovo.slovo.zak_tvar
        vysledok_slovo.popis = vysledok_slovo.slovo.daj_popis()
        vysledok_slovo.cely_popis_slova = jsonpickle.encode(vysledok_slovo.slovo)
        vysledok_slovo.anotacia = vysledok_slovo.slovo.anotacia
    else:
        vysledok_slovo.id_slova = sl.first().id
        vysledok_slovo.je_v_slovniku = True
        vysledok_slovo.je_viacej_v_slovniku = True
        vysledok_slovo.slovo = sl.first().exportuj(je_upper)
        vysledok_slovo.tvar = slovo
        vysledok_slovo.popis = vysledok_slovo.slovo.daj_popis()
        vysledok_slovo.zak_tvar = vysledok_slovo.slovo.zak_tvar
        vysledok_slovo.cely_popis_slova = jsonpickle.encode(vysledok_slovo.slovo)
        vysledok_slovo.anotacia = vysledok_slovo.slovo.anotacia

    return vysledok_slovo
