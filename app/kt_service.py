from app.db import *
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
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize


def vrat_slovo_komplet(sid, vyraz):
    start_time = time.time()
    prvy_znak_upper = False

    if sid or vyraz:
        if sid and je_cislo(sid):
            data = Slovo.query.filter(Slovo.id == sid)
        elif len(vyraz) > 0:
            prvy_znak = vyraz[0]

            if prvy_znak != prvy_znak.lower():
                prvy_znak_upper = True

            data = Slovo.query.filter(Slovo.tvar_lower == vyraz.lower())

        slovo_data = CommonObj()
        for row in data:
            slovo_data.data = {key: value for (key, value) in row.exportuj_komplet(prvy_znak_upper).__dict__.items()}

        if slovo_data.data:

            slova = Slovo.query.filter(Slovo.tvar_lower == vyraz.lower())

            slovo_data.vsetky_slova = [{key: value for (key, value) in
                                        row.exportuj_komplet(prvy_znak_upper).__dict__.items()} for row in
                                       slova]

            odvodene_slova = HierarchiaSD.query.filter(HierarchiaSD.sd_id == slovo_data.data['sd_id'])
            slovo_data.odvodene = [{key: value for (key, value) in row.exportuj().__dict__.items()} for row in
                                       odvodene_slova]

        print("--- %s seconds ---" % (time.time() - start_time)) # KONTROLA RYCHLOSTI SKRIPTU
        return slovo_data
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


def vrat_sem_priznak(sem_id):
    if sem_id:
        sem = Semantika.query.get(sem_id)
        
        return sem
    else:
        return None


def vyrob_slovo_pole(slovo, s_id, bolo_vybrate):
    vysledok = []

    slovoVK = SlovoVKontexte()

    slovoVK.tvar = slovo

    slovoVK.tvar_lower = slovo.lower()

    slovoVK.id_slova = s_id

    slovoVK.je_prve_upper = slovo[0] == slovo[0].upper() and slovo[0].lower() != slovo[0].upper()

    slovoVK.bolo_vybrate = bolo_vybrate

    vysledok.append(slovoVK)

    return vysledok


def parsuj_zoznam_slov_z_html(html, parent_slovo_id=None):
    obsah_p = pq(html).contents()

    vysledok = []
    for content in obsah_p.items():
        if len(content.children()) > 0:
            s_id = None

            html_spanu = content.outerHtml()

            if content.hasClass("s") and content.attr('sid').isdigit():
                s_id = int(content.attr('sid'))

            vysledok.extend(parsuj_zoznam_slov_z_html(html_spanu, s_id))

        else:
            if len(obsah_p) == 1:
                content = pq(html)

            text = content.text()
            slova = re.split(r'\s', text)
            bolo_vybrate = False

            i = 0
            if len(slova) > 1:
                for s in slova:
                    if s:
                        if i > 0:
                            bolo_vybrate = False
                            parent_slovo_id = None
                        else:
                            if content.is_("span") and content.attr('sid'):
                                if content.attr('sid').isdigit() and content.hasClass("s"):
                                    bolo_vybrate = True

                                if content.attr('sid').isdigit():
                                    parent_slovo_id = int(content.attr('sid'))

                        tokeny_slova = word_tokenize(s)

                        for token in tokeny_slova:
                            vysledok.extend(vyrob_slovo_pole(token, parent_slovo_id, bolo_vybrate))
                        i += 1
            else:
                if content.is_("span") and content.attr('sid'):
                    if content.attr('sid').isdigit() and content.hasClass("s"):
                        bolo_vybrate = True

                    if content.attr('sid').isdigit():
                        parent_slovo_id = int(content.attr('sid'))

                tokeny_slova = word_tokenize(slova[0])

                for token in tokeny_slova:
                    vysledok.extend(vyrob_slovo_pole(token, parent_slovo_id, bolo_vybrate))

    return vysledok


def nacitaj_naparsovane_slova(naparsovane):
    vysledok = []

    slova = [slovo.tvar_lower for slovo in naparsovane]

    for sl in Slovo.query.filter(Slovo.tvar_lower.in_(slova)):
        vysledok.append(sl.exportuj(False))

    return vysledok


def vrat_pole_slov_z_textu(html, zoznam_nacitanych_slov):
    pole = []

    celkom_slov = 0
    jednoznacnych_slov = 0

    vyparsovane_slova = parsuj_zoznam_slov_z_html(html)

    for p_slovo in vyparsovane_slova:

        v_slovo = vrat_slovo2(p_slovo.bolo_vybrate, p_slovo.je_prve_upper, p_slovo.tvar, zoznam_nacitanych_slov,
                              p_slovo. id_slova)

        if not v_slovo.je_cislo:
            celkom_slov += 1

        if ((not v_slovo.je_viacej_v_slovniku) and v_slovo.je_v_slovniku and not v_slovo.je_cislo) \
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

        if slovo.je_cislo:
            prilep = ""

            if len(pole) > i + 1:
                prilep = "&nbsp;"

            vysledok += str(slovo.tvar) + prilep

        else:
            prilep = ""

            if len(pole) > i+1:
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

        if slovo.je_cislo:
            vysledok += str(slovo.tvar) + prilep
        else:
            anot = ""

            if slovo.anotacia:
                anot = slovo.anotacia

            koncept_nazov = slovo.koncept

            if not koncept_nazov:
                koncept_nazov = ""

            vysledok += "{id}>{slovny_druh}>{sid}>{koncept}>{zak_tvar}>{slovo}/{anotacia}".\
                        format(slovo=slovo.tvar,
                               koncept=koncept_nazov,
                               anotacia=anot, id=i,
                               zak_tvar=slovo.zak_tvar,
                               slovny_druh=slovo.slovny_druh,
                               sid=slovo.id_slova) + prilep

        i += 1
    return vysledok


def kontrola_slov_v_kontexte(data):

    result = KontrolaSlovResponse()

    if not data:
        return result

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


def vyrob_kontext_vety(html):
    text = ""

    vyparsovane_slova = parsuj_zoznam_slov_z_html(html)

    for slovo in vyparsovane_slova:
        if text:
            text += " "
        text += slovo.tvar

    kontext_vety = []

    i = 0

    for sentence in sent_tokenize(text):
        veta_obj = Veta()
        veta_obj.text_celej_vety = ""
        for word in word_tokenize(sentence):
            if word != vyparsovane_slova[i].tvar:
                raise Exception(f"Nesedi tokenizacia!!! {word}->{vyparsovane_slova[i].tvar}")
            if veta_obj.text_celej_vety:
                veta_obj.text_celej_vety += " "
            veta_obj.text_celej_vety += word
            veta_obj.slova_vety.append(vyparsovane_slova[i])
            i += 1
        kontext_vety.append(veta_obj)

    return kontext_vety


def vyrob_strom_z_conllu(text_vety, poradie_vety, conllu):

    strom = []

    root = StromVety()
    root.text = text_vety
    root.parent = "#"
    root.id = f"veta_{poradie_vety}"

    strom.append(root)

    rows = conllu.split("\n")

    for r in rows:
        if not r or r.startswith("#"):
            continue

        columns = r.split("\t")

        vetva = StromVety()

        vetva.text = columns[1]
        vetva.id = f"veta_{poradie_vety}_{columns[0]}"

        if columns[6] == "0":
            vetva.parent = f"veta_{poradie_vety}"
        else:
            vetva.parent = f"veta_{poradie_vety}_{columns[6]}"

        strom.append(vetva)

    return strom

