from app.c_service import *
from app.db_models.unit_test import *


def je_tag(slovo):
    if slovo and slovo[0] == "<" and slovo[len(slovo)-1] == ">":
        return True
    return False


def porovnaj_dva_text_dokumenty(prvy, druhy):
    pole_a = prvy.split()
    pole_b = druhy.split()

    vysledne_pole_a = []

    i = 0
    for a in pole_a:
        if i >= len(pole_b):
            break
        if not je_tag(a):
            if a == pole_b[i]:
                vysledne_pole_a.append(a)
            else:
                vysledne_pole_a.append('<span class="n">'+a+'</span>'+'<span class="m">'+pole_b[i]+'</span>')
        else:
            vysledne_pole_a.append(a)

        i += 1

    i = 0
    for a in pole_b:
        if i >= len(pole_a):
            break
        if not je_tag(a):
            if a == pole_a[i]:
                pass
            else:
                if i < len(vysledne_pole_a):
                    vysledne_pole_a.append('<span class="m">'+a+'</span>'+'<span class="n">'+pole_a[i]+'</span>')
                else:
                    vysledne_pole_a[i]('<span class="m">'+a+"</span>")

        i += 1

    rozdiel = " ".join(vysledne_pole_a)

    return rozdiel


def spusti_unit_test_bodky(kontext, zadanie):
    vysledok = nahrad_bodky_v_cislach(kontext)

    return vysledok


def spusti_unit_test_struktura_vety(obsah):

    pole_viet = vrat_pole_obohatenych_viet(obsah)

    result = ""

    for veta in pole_viet:
        result += "\n" + 'aaa'  # vrat_strom_string_vety(veta)

    return result


def spusti_unit_test_otazka(zadanie, obsah):
    pole_viet = vrat_pole_obohatenych_viet(obsah)
    o = vrat_obohatenu_rozobranu_vetu(zadanie)

    result = 'aaa'  # odpovedz_na_otazku(o, pole_viet)

    return result


def spusti_unit_test(ut_id, user):
    ut = UnitTest.query.get(ut_id)

    kt = Kontext.query.get(ut.kontext_id)

    vysledok_unit_testu = ""

    if ut.funkcia == "BODKY":
        vysledok_unit_testu = spusti_unit_test_bodky(kt.obsah, ut.zadanie)
    elif ut.funkcia == "R_VETY":
        vysledok_unit_testu = spusti_unit_test_struktura_vety(kt.obsah)
    elif ut.funkcia == "OTAZKA":
        vysledok_unit_testu = spusti_unit_test_otazka(ut.zadanie, kt.obsah)

    ut.skutocny_vysledok = vysledok_unit_testu
    ut.datum_posledneho_behu = datetime.datetime.now()
    ut.spustac_posledneho_behu = user

    vysledok = False

    s = vyrob_porovnatelny_string(ut.skutocny_vysledok)
    d = vyrob_porovnatelny_string(ut.ocakavany_vysledok)

    if s == d:
        ut.status = "U"
        ut.rozdiel = ""
        vysledok = True
    else:
        ut.status = "X"
        ut.rozdiel = porovnaj_dva_text_dokumenty(s, d)

    db.session.add(ut)
    db.session.commit()

    return vysledok


def spusti_unit_testy_kontextu(kt_id, user):
    uts = UnitTest.query.filter(UnitTest.kontext_id == kt_id)

    unit_testov = 0
    uspesnych = 0

    for ut in uts:
        success = spusti_unit_test(ut.id, user)
        if success:
            uspesnych += 1
        unit_testov += 1

    return uspesnych, unit_testov


def vrat_cisty_text(html):

    text = ""

    obsah_p = pq(html).contents()

    for content in obsah_p.items():
        text += content.text()

    return text


