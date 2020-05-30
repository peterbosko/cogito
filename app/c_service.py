from app.db import *
from sqlalchemy import or_
from pyquery import PyQuery as pq
from app.c_helper import *
from app.kt_models import *
from app.db.user import *
from app.db.slovny_druh import *
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

    if slovo and je_cislo(slovo):
        vysledok_slovo.je_cislo = True
        vysledok_slovo.tvar = slovo
        return vysledok_slovo

    je_upper = slovo[0] != slovo[0].lower()

    lower_sl = slovo.lower()

    if ids:
        sl = Slovo.query.filter(Slovo.id == ids).filter(Slovo.tvar_lower == lower_sl)
    else:
        sl = Slovo.query.filter(Slovo.tvar_lower == lower_sl)

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


def vrat_slovo2(bolo_vybrate, je_prve_upper, slovo, zoznam_nacitanych_slov, ids=None):

    vysledok_slovo = SlovoVKontexte()

    if slovo and je_cislo(slovo):
        vysledok_slovo.je_cislo = True
        vysledok_slovo.tvar = slovo
        return vysledok_slovo

    lower_sl = slovo.lower()

    sl = []
    sid = None
    vybrate_slovo = None

    for s in zoznam_nacitanych_slov:
        if s.tvar_lower == lower_sl:
            sl.append(s)
            if s.id == ids:
                vybrate_slovo = s

    if len(sl) == 0:
        vysledok_slovo.id_slova = None
        vysledok_slovo.je_v_slovniku = False
        vysledok_slovo.je_viacej_v_slovniku = False
        vysledok_slovo.slovo = None
        vysledok_slovo.tvar = slovo
        vysledok_slovo.popis = None
        vysledok_slovo.cely_popis_slova = None
        vysledok_slovo.anotacia = "???????"
        vysledok_slovo.slovny_druh = None
        vysledok_slovo.koncept = None
    elif len(sl) == 1:
        if vybrate_slovo:
            sid = vybrate_slovo.id
            tvar = vybrate_slovo.tvar
            zak_tvar = vybrate_slovo.zak_tvar
            anotacia = vybrate_slovo.anotacia
            slovny_druh = vybrate_slovo.slovny_druh
            koncept = vybrate_slovo.koncept
        else:
            sid = sl[0].id
            tvar = sl[0].tvar
            zak_tvar = sl[0].zak_tvar
            anotacia = sl[0].anotacia
            slovny_druh = sl[0].slovny_druh
            koncept = sl[0].koncept

        vysledok_slovo.id_slova = sid
        vysledok_slovo.je_v_slovniku = True
        vysledok_slovo.je_viacej_v_slovniku = False
        vysledok_slovo.slovo = tvar
        vysledok_slovo.tvar = slovo
        vysledok_slovo.zak_tvar = zak_tvar
        vysledok_slovo.popis = ""
        vysledok_slovo.cely_popis_slova = ""
        vysledok_slovo.anotacia = anotacia
        vysledok_slovo.bolo_vybrate = bolo_vybrate
        vysledok_slovo.slovny_druh = slovny_druh
        vysledok_slovo.koncept = koncept
    else:
        if vybrate_slovo:
            sid = vybrate_slovo.id
            tvar = vybrate_slovo.tvar
            zak_tvar = vybrate_slovo.zak_tvar
            anotacia = vybrate_slovo.anotacia
            slovny_druh = vybrate_slovo.slovny_druh
            koncept = vybrate_slovo.koncept
        else:
            sid = sl[0].id
            tvar = sl[0].tvar
            zak_tvar = sl[0].zak_tvar
            anotacia = sl[0].anotacia
            slovny_druh = sl[0].slovny_druh
            koncept = sl[0].koncept

        vysledok_slovo.id_slova = sid
        vysledok_slovo.je_v_slovniku = True
        vysledok_slovo.je_viacej_v_slovniku = True
        vysledok_slovo.slovo = tvar
        vysledok_slovo.tvar = slovo
        vysledok_slovo.zak_tvar = zak_tvar
        vysledok_slovo.popis = ""
        vysledok_slovo.cely_popis_slova = ""
        vysledok_slovo.anotacia = anotacia
        vysledok_slovo.bolo_vybrate = bolo_vybrate
        vysledok_slovo.slovny_druh = slovny_druh
        vysledok_slovo.koncept = koncept

    return vysledok_slovo


