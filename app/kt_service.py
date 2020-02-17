from app.db_models import *
from sqlalchemy import or_
from pyquery import PyQuery as pq
from app.c_helper import *
import re
from app.c_service import *
from app.c_models import *
import json
import jsonpickle
import html
import datetime
import time


def vrat_slovo_komplet(sid, vyraz):
    start_time = time.time()
    prvy_znak_upper = False

    if sid or vyraz:
        if sid:
            data = Slovo.query.filter(Slovo.id == sid)
        elif len(vyraz) > 0 and not sid:
            prvy_znak = vyraz[0]

            if prvy_znak == prvy_znak.upper():
                prvy_znak_upper = True

            if prvy_znak_upper:
                data = Slovo.query.filter(or_(Slovo.tvar == vyraz, Slovo.tvar == vyraz.lower()))
            else:
                data = Slovo.query.filter(Slovo.tvar == vyraz)

        slovo_data = CommonObj()
        for row in data:
            slovo_data.data = {key: value for (key, value) in row.exportuj_komplet(prvy_znak_upper).__dict__.items()}

        # VSEOBECNE

        #v_slovne_druhy = SlovnyDruh.query.filter(SlovnyDruh.zak_tvar == slovo_data.data['zak_tvar'])
        #slovo_data.vsetky_slovne_druhy = [{key: value for (key, value) in row.exportuj().__dict__.items()} for row in
        #                                  v_slovne_druhy]

        #pady = Slovo.query.filter(Slovo.sd_id == slovo_data.data['sd_id']).filter(
        #    Slovo.cislo == slovo_data.data['cislo']).filter(Slovo.rod == slovo_data.data['rod']).filter(
        #    Slovo.podrod == slovo_data.data['podrod'])
        #slovo_data.pady = [{key: value for (key, value) in row.exportuj(False).__dict__.items()} for row
        #                                  in pady]

        #cisla = Slovo.query.filter(Slovo.sd_id == slovo_data.data['sd_id']).filter(Slovo.pad == slovo_data.data['pad'])
        #slovo_data.cisla = [{key: value for (key, value) in row.exportuj(False).__dict__.items()} for row in cisla]

        if slovo_data.data:
            slova = Slovo.query.filter(Slovo.tvar == slovo_data.data['tvar']).filter(Slovo.anotacia.isnot(None))
            slovo_data.vsetky_slova = [{key: value for (key, value) in row.exportuj_komplet(prvy_znak_upper).__dict__.items()} for row in
                                       slova]

            odvodene_slova = HierarchiaSD.query.filter(HierarchiaSD.sd_id == slovo_data.data['sd_id'])
            slovo_data.odvodene = [{key: value for (key, value) in row.exportuj().__dict__.items()} for row in
                                       odvodene_slova]

        #if slovo_data.data['slovny_druh'] == "PRID_M":
            # PRID_M
        #    stupne = Slovo.query.filter(Slovo.sd_id == slovo_data.data['sd_id']).group_by(Slovo.stupen).group_by(
        #        Slovo.cislo)
        #    slovo_data.stupne = [{key: value for (key, value) in row.exportuj(False).__dict__.items()} for row in
        #                        stupne]

        #if slovo_data.data['slovny_druh'] == "SLOVESO":
            # SLOVESO
        #    tvary_slovies = Slovo.query.get(slovo_data.data['sd_id'])
        #    slovo_data.tvary_slovies = [{key: value for (key, value) in row.exportuj(False).__dict__.items()} for row in
        #                                tvary_slovies]

        print("--- %s seconds ---" % (time.time() - start_time))
        return slovo_data
    else:
        return None


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


def vrat_slovne_druhy_slova_zacinajuce_na(vyraz):
    if len(vyraz) > 0:
        prvy_znak = vyraz[0]

        prvy_znak_upper = False

        if prvy_znak == prvy_znak.upper():
            prvy_znak_upper = True

        if prvy_znak_upper:
            pole_slov = SlovnyDruh.query.filter(or_(SlovnyDruh.zak_tvar == vyraz, SlovnyDruh.zak_tvar == vyraz.lower()))
        else:
            pole_slov = SlovnyDruh.query.filter(SlovnyDruh.zak_tvar == vyraz)

        #pole_slov = pole_slov.filter(SlovnyDruh.anotacia.isnot(None)) #slovny druh nema anotaciu

        if pole_slov.count() == 0:
            if prvy_znak_upper:
                pole_slov = SlovnyDruh.query.filter(or_(SlovnyDruh.zak_tvar.like(vyraz + "%"), SlovnyDruh.zak_tvar.like(vyraz.lower()+"%")))\
                    .paginate(1, 15, False).items
            else:
                pole_slov = SlovnyDruh.query.filter(SlovnyDruh.zak_tvar.like(vyraz + "%"))\
                    .paginate(1, 15, False).items

        return [{key: value for (key, value) in row.exportuj().__dict__.items()} for row in pole_slov]
    else:
        return None


def vrat_vsetky_slova(vyraz):
    if vyraz:
        pole_slov = Slovo.query.filter(Slovo.tvar == vyraz).filter(Slovo.anotacia.isnot(None))
        
        return [{key: value for (key, value) in row.exportuj(False).__dict__.items()} for row in pole_slov]
    else:
        return None


def vrat_sem_priznak(sem_id):
    if sem_id:
        sem = Semantika.query.get(sem_id)
        
        return sem
    else:
        return None


def vrat_sem_pad(sid):
    if sid:
        druh = Slovo.query.get(sid)
        if druh.sem_id:
            intencia = Intencia.query.filter(Intencia.sem == druh.sem_id)
            sem_pad = intencia.sem_pad
        
        return sem_pad
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

            if content.hasClass("s") and content.attr('sid').isdigit():
                s_id = int(content.attr('sid'))

            s, u, p = vrat_pole_slov_z_textu(content.outerHtml(), s_id)
            celkom_slov += s
            jednoznacnych_slov += u
            pole.extend(p)
        else:
            # print("Kontent je text:" + content.text()+"|")
            # oprava - najprv kontrola cisla potom pridavanie medzery pred spec. znaky
            #text = daj_medzery_pred_specialne_znaky(content.text())
            text = content.text()
            
            slova_to_check = re.split(r'\s', text)

            pocitadlo_v_slova_to_check = 0
            for s in slova_to_check:
                if s:
                    pocitadlo_v_slova_to_check += 1
                    if pq(html).is_("span") and pq(html).hasClass("s") and pq(html).attr('sid').isdigit() and pocitadlo_v_slova_to_check == 1:
                        parent_slovo_id = int(pq(html).attr("sid"))
                    else:
                        parent_slovo_id = None

                    posledny_znak = s[len(s)-1]
                    prvy_znak = s[0]
                    if posledny_znak in SPEC_ZNAKY and len(s) > 1:
                        cslov, js, v_slovo = vrat_slovo_po_kontrole_znakov(s, parent_slovo_id)
                        pole = pole + v_slovo
                        celkom_slov += cslov
                        jednoznacnych_slov += js
                    else:
                        v_slovo = vrat_slovo(s, parent_slovo_id)
                    
                        if not v_slovo.neprekl_vyraz and not v_slovo.je_cislo:
                            celkom_slov += 1

                        if parent_slovo_id and parent_slovo_id == v_slovo.id_slova:
                            v_slovo.bolo_vybrate = True

                        if ((not v_slovo.je_viacej_v_slovniku) and v_slovo.je_v_slovniku
                                and not v_slovo.neprekl_vyraz) or v_slovo.bolo_vybrate:
                            jednoznacnych_slov += 1

                        pole.append(v_slovo)

    return celkom_slov, jednoznacnych_slov, pole


def vrat_slovo_po_kontrole_znakov(slova, parent_slovo_id):
    pole = []
    celkom_slov = 0
    jednoznacnych_slov = 0
    
    slova = daj_medzery_pred_specialne_znaky(slova)
    slova_to_check = re.split(r'\s', slova)
    if len(slova_to_check) > 1:
        for s in slova_to_check:
            if s:
                v_slovo = vrat_slovo(s, parent_slovo_id)
                    
                if not v_slovo.neprekl_vyraz and not v_slovo.je_cislo:
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
            cl = "n ns"

        if slovo.je_viacej_v_slovniku and not slovo.bolo_vybrate:
            cl = "m ns"

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
        if obsah_p:
            slov, jednoznacnych, pole = vrat_pole_slov_z_textu(obsah_p)

        celkom_slov += slov

        jednoznacnych_slov += jednoznacnych
        
        pole_slov.extend(pole)
        
        if pole_slov:

            result.data += "<p>%s</p>" % (serializuj_pole_slov(pole_slov))
        
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