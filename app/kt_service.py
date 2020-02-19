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


def vyrob_slovo_pole(slovo, s_id, bolo_vybrate):
    vysledok = []

    slovoVK = SlovoVKontexte()

    slovoVK.tvar = slovo

    slovoVK.id_slova = s_id

    slovoVK.je_prve_upper = slovo[0] == slovo[0].upper() and slovo[0].lower() != slovo[0].upper()

    slovoVK.bolo_vybrate = bolo_vybrate

    vysledok.append(slovoVK)

    return vysledok


def daj_tokeny_slova(slovo):
    text_slova = ""
    text_cisla = ""

    def ukonci_slovo():
        if text_slova != "":
            vysledok.append(text_slova)
        som_v_slove = False

    def ukonci_cislo():
        if text_cisla != "":
            vysledok.append(text_cisla)
        som_v_cisle = False

    vysledok = []

    som_v_slove = False
    som_v_cisle = False

    i = 0
    for letter in slovo:
        i += 1

        if letter == "." or letter == ",":
            if som_v_cisle:
                if i == len(slovo):
                    ukonci_cislo()
                    text_cisla = ""
                    vysledok.append(letter)
                else:
                    text_cisla += letter
            else:
                ukonci_cislo()
                text_cisla = ""
                ukonci_slovo()
                text_slova = ""
                vysledok.append(letter)
        elif letter in SPEC_ZNAKY:
            ukonci_cislo()
            text_cisla = ""
            ukonci_slovo()
            text_slova = ""
            vysledok.append(letter)
        elif letter in "0123456789":
            som_v_cisle = True
            text_cisla += letter
        else:
            som_v_slove = True
            text_slova += letter

    ukonci_cislo()
    text_cisla = ""
    ukonci_slovo()
    text_slova = ""

    return vysledok


def parsuj_zoznam_slov_z_html(html, parent_slovo_id=None):
    obsah_p = pq(html).contents()

    vysledok = []
    for content in obsah_p.items():
        if len(content.children()) > 0:
            s_id = None

            html_spanu = content.outerHtml()

            text = content.text()
            slova = re.split(r'\s', text)

            if content.hasClass("s") and content.attr('sid').isdigit():
                s_id = int(content.attr('sid'))

            vysledok.extend(parsuj_zoznam_slov_z_html(html_spanu, s_id))

        else:
            text = content.text()
            slova = re.split(r'\s', text)
            bolo_vybrate = False

            if content.is_("span") and content.attr('sid'):
                if content.attr('sid').isdigit() and content.hasClass("s"):
                    bolo_vybrate = True

                if content.attr('sid').isdigit():
                    parent_slovo_id = int(content.attr('sid'))

            i = 0
            if len(slova) > 1:
                for s in slova:
                    if s:
                        if i > 0:
                            bolo_vybrate = False
                            parent_slovo_id = None

                        tokeny_slova = daj_tokeny_slova(s)
                        for token in tokeny_slova:
                            vysledok.extend(vyrob_slovo_pole(token, parent_slovo_id, bolo_vybrate))
                        i += 1
            else:
                tokeny_slova = daj_tokeny_slova(slova[0])
                for token in tokeny_slova:
                    vysledok.extend(vyrob_slovo_pole(token, parent_slovo_id, bolo_vybrate))

    return vysledok


def nacitaj_naparsovane_slova(naparsovane):
    vysledok = []

    slova = [slovo.tvar for slovo in naparsovane]

    for p in naparsovane:
        if p.je_prve_upper:
            lws = p.tvar[0].lower()
            if len(p.tvar) > 1:
                lws += p.tvar[1:]
            slova.append(lws)

    for sl in Slovo.query.filter(Slovo.tvar.in_(slova)):
        vysledok.append(sl.exportuj(False))

    return vysledok


def vrat_pole_slov_z_textu(html, zoznam_nacitanych_slov):
    pole = []

    celkom_slov = 0
    jednoznacnych_slov = 0

    vyparsovane_slova = parsuj_zoznam_slov_z_html(html)

    for p_slovo in vyparsovane_slova:

        v_slovo = vrat_slovo2(p_slovo.bolo_vybrate, p_slovo.je_prve_upper, p_slovo.tvar, zoznam_nacitanych_slov, p_slovo.id_slova)

        if not v_slovo.neprekl_vyraz and not v_slovo.je_cislo:
            celkom_slov += 1

        if ((not v_slovo.je_viacej_v_slovniku) and v_slovo.je_v_slovniku and not v_slovo.neprekl_vyraz) \
                or v_slovo.bolo_vybrate:
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

            vysledok += "<span class='{cl} no-select' sid='{id}'>{slovo}</span>".format(
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

    vyparsovane_slova = parsuj_zoznam_slov_z_html(data)

    zoznam_nacitanych_slov = nacitaj_naparsovane_slova(vyparsovane_slova)

    for p in doc("p"):

        pole_slov = []

        obsah_p = pq(p).html()
        if obsah_p:
            slov, jednoznacnych, pole = vrat_pole_slov_z_textu(obsah_p, zoznam_nacitanych_slov)

        celkom_slov += slov

        jednoznacnych_slov += jednoznacnych
        
        pole_slov.extend(pole)
        
        if pole_slov:

            result.data += "<p>%s</p>" % (serializuj_pole_slov(pole_slov))

    if celkom_slov == 0:
        celkom_slov = 1

    result.uspesnost = round(jednoznacnych_slov/celkom_slov * 100, 2)

    return result


def vrat_ciste_slova_s_anotaciou(data):

    vysledok = ""

    doc = pq(data)

    vyparsovane_slova = parsuj_zoznam_slov_z_html(data)

    zoznam_nacitanych_slov = nacitaj_naparsovane_slova(vyparsovane_slova)

    for p in doc("p"):

        obsah_p = pq(p).html()

        slov, jednoznacnych, pole = vrat_pole_slov_z_textu(obsah_p, zoznam_nacitanych_slov)

        vysledok += serializuj_pole_slov_do_anotacie(pole)+"\n"

    return vysledok

