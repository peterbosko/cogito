from app.db_models import *
from sqlalchemy import or_
from pyquery import PyQuery as pq
from app.helper import *
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


def sl_vrat_slova_zacinajuce_na(vyraz, presna_zhoda):
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


def vrat_slovo(slovo, ids=None):

    vysledok_slovo = SlovoVKontexte()

    if slovo and je_cislo(slovo):
        vysledok_slovo.neprekl_vyraz = daj_cislo(slovo)
        vysledok_slovo.je_cislo = True
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

"""
def vrat_pole_slov_z_textu(html, parent_slovo_id=None):
    pole = []

    celkom_slov = 0
    jednoznacnych_slov = 0

    html = vyrob_korektne_html_z_editora(html)

    obsah_p = pq(html).contents()

    for content in obsah_p.items():
        print("ide horny loop:"+content.outerHtml())
        if content.is_("span"):
            s_id = int(content.attr('sid'))
            v_slovo = vrat_slovo(content.outerHtml(), s_id)
            if content.hasClass("s"):
                jednoznacnych_slov += 1
            celkom_slov += 1
            pole.append(v_slovo)
        else:
            # print("Kontent je text:" + content.text()+"|")
            text = daj_medzery_pred_specialne_znaky(content.text())

            slova_to_check = re.split(r'\s', text)

            for s in slova_to_check:
                if s:
                    v_slovo = vrat_slovo(s, None)

                    if not v_slovo.neprekl_vyraz:
                        celkom_slov += 1

                    if ((not v_slovo.je_viacej_v_slovniku) and v_slovo.je_v_slovniku
                            and not v_slovo.neprekl_vyraz) or v_slovo.bolo_vybrate:
                        jednoznacnych_slov += 1

                    pole.append(v_slovo)

    return celkom_slov, jednoznacnych_slov, pole

"""


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


def kt_kontrola_slov_v_kontexte(data):

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


def kt_vrat_ciste_slova_s_anotaciou(data):

    vysledok = ""

    doc = pq(data)

    for p in doc("p"):

        obsah_p = pq(p).html()

        slov, jednoznacnych, pole = vrat_pole_slov_z_textu(obsah_p)

        vysledok += serializuj_pole_slov_do_anotacie(pole)+"\n"

    return vysledok


def vrat_obohatene_slova_z_vety(veta):
    doc = pq(veta)

    slova = []

    index_slova = 0

    indexy_pouzitych_slov = []

    vysledok = []

    slovesa_indexy = []

    podmety = []

    def moze_byt_prisudok(slovo_id):
        for p in podmety:
            if slova[p].cislo == slova[slovo_id].cislo and (slova[p].rod == slova[slovo_id].rod
                                                            or slova[slovo_id].rod is None):
                return True

        return False

    def moze_byt_podmet(idx):
        if slova[idx].pad == "Nom":
            if idx-1 >= 0:
                if slova[idx-1].tvar == 'pojmu':
                    return False
            return True

        return False

    for span in doc("span"):
        sl = Slovo.query.get(pq(span).attr('sid'))
        prvy_znak_upper = pq(span).text()[0] != pq(span).text()[0].lower()
        slova.append(sl.exportuj(prvy_znak_upper))

        if sl.SlovnyDruh.typ == "POD_M":
            obohatene_pm = RozvitelneSlovo()
            obohatene_pm.index = index_slova
            obohatene_pm.rozvijajuce_privlastky = []
            obohatene_pm.rozvijajuce_slova = []
            obohatene_pm.tvar = slova[index_slova].tvar
            obohatene_pm.index_pociatku_rozvoja = index_slova
            obohatene_pm.je_podmet = moze_byt_podmet(index_slova)
            obohatene_pm.sid = sl.id
            obohatene_pm.sd_id = sl.sd_id
            indexy_pouzitych_slov.append(index_slova)

            if obohatene_pm.je_podmet:
                podmety.append(index_slova)

            for i in reversed(range(index_slova)):
                if slova[i].slovny_druh != "POD_M":
                    if (slova[i].slovny_druh == "PRID_M" and slova[i].pad == slova[obohatene_pm.index].pad)\
                            or (slova[i].slovny_druh == "PREDLOZKA" and slova[obohatene_pm.index].pad
                                in slova[i].zoznam_padov) \
                            or (slova[i].pad == slova[obohatene_pm.index].pad)\
                            or (slova[i].slovny_druh == "PRISLOVKA") \
                            or (slova[i].slovny_druh == "ZAMENO") \
                            or (slova[i].tvar.lower() == "sa" or slova[i].tvar.lower() == "si"):
                        rs = RozvijajuceSlovo()
                        rs.index = i
                        rs.slovo = slova[i].tvar
                        rs.sid = slova[i].id
                        indexy_pouzitych_slov.append(i)
                        obohatene_pm.index_pociatku_rozvoja = i
                        obohatene_pm.rozvijajuce_privlastky.append(rs)

                    else:
                        break
                else:
                    break

            vysledok.append(obohatene_pm)

        elif sl.SlovnyDruh.typ == "SLOVESO":
            slovesa_indexy.append(index_slova)

        index_slova += 1

    prisudky = []

    for sloveso in slovesa_indexy:
        if moze_byt_prisudok(sloveso):
            prisudky.append(sloveso)

    lslova = range(len(slova))

    slova_slovesa = list(set(lslova)-set(indexy_pouzitych_slov))

    v_i = 0
    for s in slova_slovesa:
        while v_i < len(vysledok) and vysledok[v_i].index_pociatku_rozvoja < s:
            v_i += 1

        obohatene_sloveso = RozvitelneSlovo()
        obohatene_sloveso.index = s
        obohatene_sloveso.rozvijajuce_privlastky = []
        obohatene_sloveso.rozvijajuce_slova = []
        obohatene_sloveso.tvar = slova[s].tvar
        obohatene_sloveso.index_pociatku_rozvoja = s
        obohatene_sloveso.je_zo_slovesa = True
        obohatene_sloveso.sid = slova[s].id
        obohatene_sloveso.sd_id = slova[s].sd_id

        vysledok.insert(v_i, obohatene_sloveso)

    return slova, vysledok, podmety, prisudky


def vrat_obohatenu_rozobranu_vetu(veta):

    slova = []

    obohatene_pm = []

    slovesa_indexy = []

    podmety = []

    prisudky = []

    def zacina_predlozkou(ind):
        if len(obohatene_pm[ind].rozvijajuce_privlastky) > 0:
            if slova[obohatene_pm[ind].rozvijajuce_privlastky[-1].index].slovny_druh == "PREDLOZKA":
                return True

        return False

    def pm_rozvija_pm(zaklad_index, rozvoj_index):
        if obohatene_pm[zaklad_index].index+1 == obohatene_pm[rozvoj_index].index_pociatku_rozvoja \
                and ((slova[obohatene_pm[zaklad_index].index].pad == slova[obohatene_pm[rozvoj_index].index].pad
                      or slova[obohatene_pm[zaklad_index].index].pad == "Nom"
                      or slova[obohatene_pm[rozvoj_index].index].pad == "Nom")
                     or zacina_predlozkou(rozvoj_index)):
            return True

        bola_iteracie = False
        rozvija = True

        ind = rozvoj_index-1

        while rozvija and ind > zaklad_index:
            rozvija = pm_rozvija_pm(zaklad_index, ind)
            bola_iteracie = True
            ind -= 1

        return bola_iteracie and rozvija and slova[obohatene_pm[zaklad_index].index].pad == \
            slova[obohatene_pm[rozvoj_index].index].pad

    def slovo_rozvija_sloveso(zaklad_index, rozvoj_index):
        if obohatene_pm[zaklad_index].index+1 == obohatene_pm[rozvoj_index].index_pociatku_rozvoja:
            return True

        bola_iteracie = False
        rozvija = True

        ind = rozvoj_index-1

        while rozvija and ind > zaklad_index:
            rozvija = slovo_rozvija_sloveso(zaklad_index, ind)
            bola_iteracie = True
            ind -= 1

        return bola_iteracie and rozvija

    slova, obohatene_pm, podmety, prisudky = vrat_obohatene_slova_z_vety(veta)

    for i in reversed(range(0, len(obohatene_pm))):
        obohatene_pm[i].priradit_k = i
        for j in reversed(range(0, i)):
            if not obohatene_pm[i].je_zo_slovesa and not obohatene_pm[j].je_zo_slovesa:
                if pm_rozvija_pm(j, i):
                    obohatene_pm[i].priradit_k = j
                    break
            else:
                if slovo_rozvija_sloveso(j, i):
                    obohatene_pm[i].priradit_k = j
                    break

    for i in reversed(range(0, len(obohatene_pm))):
        if obohatene_pm[i].priradit_k and obohatene_pm[i].priradit_k != i or (obohatene_pm[i].priradit_k == 0
                                                                              and i != 0):
            roz_s = RozvitelneSlovo()
            roz_s.index_pociatku_rozvoja = obohatene_pm[i].index_pociatku_rozvoja
            roz_s.tvar = obohatene_pm[i].tvar
            roz_s.index = obohatene_pm[i].index
            roz_s.rozvijajuce_privlastky = obohatene_pm[i].rozvijajuce_privlastky
            roz_s.rozvijajuce_slova = obohatene_pm[i].rozvijajuce_slova
            roz_s.otec = obohatene_pm[obohatene_pm[i].priradit_k]
            roz_s.sid = obohatene_pm[i].sid
            roz_s.sd_id = obohatene_pm[i].sd_id
            obohatene_pm[obohatene_pm[i].priradit_k].rozvijajuce_slova.append(roz_s)
            del obohatene_pm[i]

    v = ObohatenaVeta()
    v.slova = slova
    v.podmety = podmety
    v.prisudky = prisudky
    v.strom_vety = obohatene_pm

    return v


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


def rozdel_kontext_na_vety(kontext):
    novy_kontext = nahrad_bodky_v_cislach(kontext)
    pole = novy_kontext.split('.')

    i = 0

    for p in pole:
        pole[i] = p.replace("_bodka_", ".")
        i += 1

    return pole


def vyrob_porovnatelny_string(string):
    return html.unescape(string).replace("<p>", "").replace("</p>", "").replace("\n", "")


def vrat_pole_obohatenych_viet(obsah):
    vety = rozdel_kontext_na_vety(obsah)

    result = []

    for veta in vety:
        if vyrob_porovnatelny_string(veta) == "":
            continue
        v = vrat_obohatenu_rozobranu_vetu(veta)
        result.append(v)

    return result


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

