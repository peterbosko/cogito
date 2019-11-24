from flask import Blueprint
from flask import render_template
from flask import request
from datatables import DataTable
from app.c_service import *
from app.kt_service import vrat_slovo as vs
from app.kt_service import *
from app.ut_service import spusti_unit_test as sut
from app.ut_service import spusti_unit_testy_kontextu as sutk
from sqlalchemy.exc import *
import json

kontext_blueprint = Blueprint("kontext", __name__)


@kontext_blueprint.route("/pridat_kontext/", methods=["GET"])
def pridat_kontext():
    loguj(request)
    return render_template("m_kontext/pridat_kontext.jinja.html")


@kontext_blueprint.route("/kontexty/", methods=["GET"])
def kontexty():
    loguj(request)
    search_term = request.args.get("search_term", "")
    page = request.args.get("page", 1, type=int)
    paginate = Kontext.query.filter(or_(Kontext.nazov.like('%' + search_term + '%'),
                                        Kontext.text.like('%' + search_term + '%'))).paginate(page, 5, False)
    return render_template("m_kontext/kontexty.jinja.html", kontexty=paginate.items, paginate=paginate,
                           search_term=search_term)


@kontext_blueprint.route("/moje_kontexty/", methods=["GET"])
def moje_kontexty():
    loguj(request)
    user = 0
    if 'logged' in session.keys():
        user = int(session["logged"])
    page = request.args.get("page", 1, type=int)
    paginate = Kontext.query.filter(Kontext.autor_id == user).paginate(page, 5, False)
    return render_template("m_kontext/moje_kontexty.jinja.html", kontexty=paginate.items, paginate=paginate)


@kontext_blueprint.route("/kontexty/<int:kt_id>/")
def zobraz_kontext(kt_id):
    loguj(request)
    kt = Kontext.query.filter_by(id=kt_id).first()
    if kt:
        return render_template("m_kontext/pridat_kontext.jinja.html", kontext=kt)
    return render_template("m_kontext/kontext_sa_nenasiel.jinja.html", kontext=kt_id)


@kontext_blueprint.route("/pridat_kontext/", methods=["POST"])
def pridat_zmenit_kontext():
    loguj(request)
    kt_id = int(request.json["id"])

    response = CommonResponse()

    if kt_id == 0 and 'logged' in session.keys():
        kt = Kontext()
        kt.status = "N"
        kt.autor_id = int(session["logged"])
        kt.nazov = request.json["nazov"]
        kt.obsah = request.json["obsah"]
        kt.text = request.json["text"]
        db.session.add(kt)
        db.session.commit()
        response.data = kt.id
    elif 'logged' in session.keys():
        kt = Kontext.query.filter_by(id=kt_id).first()

        if kt.mam_prava():
            kt.nazov = request.json["nazov"]
            kt.obsah = request.json["obsah"]
            kt.text = request.json["text"]
            db.session.add(kt)
            db.session.commit()
            response.data = kt.id
        else:
            response.status = ResponseStatus.ERROR
            response.error_text = "Nedostatočné práva pre operáciu"
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/kontexty/<int:kt_id>/", methods=["POST"])
def zmenit_kontext(kt_id):
    loguj(request)
    return pridat_zmenit_kontext()


@kontext_blueprint.route("/zmaz_kontext/<int:kt_id>/", methods=["GET"])
def zmaz_kontext(kt_id):
    loguj(request)
    response = CommonResponse()

    if 'logged' in session.keys():
        kt = Kontext.query.get(kt_id)

        if kt.mam_prava():
            try:
                db.session.delete(kt)
                db.session.commit()
            except IntegrityError as e:
                response.status = ResponseStatus.ERROR
                response.error_text = "Kontext má definované unit testy. Zmažte najskôr tie"

        else:
            response.status = ResponseStatus.ERROR
            response.error_text = "Nedostatočné práva pre operáciu"
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/daj_tvary_slova/", methods=["GET"])
def daj_tvary_slova():
    loguj(request)
    vyraz = request.args.get("vyraz", "")

    presna_zhoda = request.args.get("presna_zhoda", "N")

    response = CommonResponse()

    response.data = vrat_slova_zacinajuce_na(vyraz, presna_zhoda)

    return jsonpickle.encode(response)


@kontext_blueprint.route("/kontrola_slov/", methods=["POST"])
def kontroluj_slova():
    loguj(request)
    data = request.json["data"]

    response = CommonResponse()

    response.data = kontrola_slov_v_kontexte(data)

    return jsonpickle.encode(response)


@kontext_blueprint.route("/dopln_anotaciu/", methods=["POST"])
def dopln_anotaciu():
    loguj(request)
    data = request.json["data"]

    response = CommonResponse()

    response.data = vrat_ciste_slova_s_anotaciou(data)

    return jsonpickle.encode(response)


@kontext_blueprint.route("/vrat_slovo/", methods=["GET"])
def vrat_slovo():
    loguj(request)
    sid = request.args.get("sid", "")
    slovo = request.args.get("slovo", "")

    response = CommonResponse()

    if sid:
        slovo = vs(slovo, sid)
        response.data = slovo.cely_popis_slova

    return jsonpickle.encode(response)


@kontext_blueprint.route("/dopytuj_kontext/", methods=["GET"])
def dopytuj_kontext():
    loguj(request)
    kt_id = request.args.get("kontext_id", "")
    kt = Kontext.query.filter_by(id=kt_id).first()
    if kt:
        return render_template("m_kontext/dopytovat_kontext.jinja.html", kontext=kt)
    return render_template("m_kontext/kontext_sa_nenasiel.jinja.html", kontext=kt_id)


@kontext_blueprint.route("/daj_unit_testy/", methods=["GET"])
def daj_unit_testy():
    loguj(request)
    kontext_id = request.args.get("kontext_id", "")

    filtered = db.session.query(UnitTest).filter(UnitTest.kontext_id == kontext_id)

    table = DataTable(request.args, UnitTest, filtered, [
            "id",
            "status",
            "nazov",
            "funkcia",
            "poradie",
            ("datum_posledneho_behu", "datum_posledneho_behu", lambda i: formatuj_datum(i.datum_posledneho_behu)),
            ("spustac_posledneho_behu", lambda j: daj_popis_usera(j.spustac_posledneho_behu)),
    ])

    return json.dumps(table.json())


@kontext_blueprint.route("/zoznam_ut/", methods=["GET"])
def zoznam_ut():
    loguj(request)

    kt_id = request.args.get("kontext_id", "")

    return render_template("m_kontext/zoznam_ut.jinja.html", kontext_id=kt_id)


@kontext_blueprint.route("/pridat_zmenit_unit_test/", methods=["GET"])
def pridat_zmenit_unit_test():
    loguj(request)

    ut_id = request.args.get("ut_id", "")

    ut = UnitTest.query.get(ut_id)

    kontext = request.args.get("kontext_id", "")

    spustil = ""

    datum_spustenia = ""

    if ut:
        kontext = ut.kontext_id
        if ut.spustac_posledneho_behu:
            spustil = daj_popis_usera(ut.spustac_posledneho_behu)
        if ut.datum_posledneho_behu:
            datum_spustenia = formatuj_datum(ut.datum_posledneho_behu)

    kts = Kontext.query.order_by(Kontext.nazov)

    if not kontext:
        kontext = kts.first().id

    return render_template("m_kontext/pridat_unit_test.jinja.html", unit_test=ut, kontexty=kts, kontext_id=kontext,
                           spustil=spustil, datum_spustenia=datum_spustenia)


@kontext_blueprint.route("/pridat_zmenit_unit_test/", methods=["POST"])
def pridat_zmenit_unit_test_post():
    loguj(request)
    kt_id = int(request.json["kt_id"])
    ut_id = int(request.json["id"])

    response = CommonResponse()

    if ut_id == 0 and 'logged' in session.keys():
        ut = UnitTest()
        ut.status = "N"
        ut.kontext_id = kt_id
        ut.poradie = int(request.json["poradie"])
        ut.nazov = request.json["nazov"]
        ut.funkcia = request.json["funkcia"]
        ut.zadanie = request.json["zadanie"]
        ut.ocakavany_vysledok = request.json["ocakavany_vysledok"]
        ut.skutocny_vysledok = request.json["skutocny_vysledok"]
        ut.autor_id = int(session["logged"])
        db.session.add(ut)
        db.session.commit()
        response.data = ut.id
    elif 'logged' in session.keys():
        ut = UnitTest.query.filter_by(id=ut_id).first()

        kt = Kontext.query.filter_by(id=kt_id).first()

        if kt.mam_prava():
            ut.status = "M"
            ut.poradie = int(request.json["poradie"])
            ut.nazov = request.json["nazov"]
            ut.funkcia = request.json["funkcia"]
            ut.zadanie = request.json["zadanie"]
            ut.ocakavany_vysledok = request.json["ocakavany_vysledok"]
            ut.skutocny_vysledok = None
            ut.datum_posledneho_behu = None
            ut.spustac_posledneho_behu = None
            db.session.add(ut)
            db.session.commit()
            response.data = ut.id
        else:
            response.status = ResponseStatus.ERROR
            response.error_text = "Nedostatočné práva pre operáciu"
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/zmaz_unit_test/<int:ut_id>/", methods=["GET"])
def zmaz_unit_test(ut_id):
    loguj(request)
    response = CommonResponse()

    if 'logged' in session.keys():
        ut = UnitTest.query.get(ut_id)

        if ut.mam_prava():
            db.session.delete(ut)
            db.session.commit()
        else:
            response.status = ResponseStatus.ERROR
            response.error_text = "Nedostatočné práva pre operáciu"
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/spusti_konkretny_unit_test/<int:ut_id>/", methods=["GET"])
def spusti_konkretny_unit_test(ut_id):
    loguj(request)
    response = CommonResponse()

    if 'logged' in session.keys():

        vysledok_ut = sut(ut_id, int(session["logged"]))

        if vysledok_ut:
            response.status = ResponseStatus.OK
            response.message_text = "Unit test skončil úspešne"
        else:
            response.status = ResponseStatus.ERROR
            response.message_text = "Unit test skončil chybou"
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/spusti_unit_test_kontextu/<int:kt_id>/", methods=["GET"])
def spusti_unit_testy_kontextu(kt_id):
    loguj(request)
    response = CommonResponse()

    if 'logged' in session.keys():

        uspesnych, celkom = sutk(kt_id, int(session["logged"]))

        if uspesnych == celkom:
            response.status = ResponseStatus.OK
            response.message_text = "Unit testy kontextu prebehly OK. Úspešných/Celkom : {1}/{0}".\
                format(celkom, uspesnych)
        else:
            response.status = ResponseStatus.ERROR
            response.message_text = "V unit testoch bola chyba. Neúspešných/Celkom : {1}/{0}".\
                format(celkom, celkom-uspesnych)
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/vsetky_unit_testy/", methods=["GET"])
def vsetky_unit_testy():
    loguj(request)
    kts = Kontext.query.order_by(Kontext.nazov)

    funkcie = db.session.query(UnitTest.funkcia).distinct().all()

    return render_template("m_kontext/vsetky_unit_testy.jinja.html", kontexty=kts, funkcie=funkcie)


@kontext_blueprint.route("/daj_vsetky_unit_testy/", methods=["GET"])
def daj_vsetky_unit_testy():
    loguj(request)
    funkcia = request.args.get("funkcia", "")

    kontext_id = request.args.get("kontext", "")

    status = request.args.get("status", "")

    filtered = db.session.query(UnitTest)

    if kontext_id:
        filtered = filtered.filter(UnitTest.kontext_id == kontext_id)

    if funkcia:
        filtered = filtered.filter(UnitTest.funkcia == funkcia)

    if status:
        filtered = filtered.filter(UnitTest.status == status)

    table = DataTable(request.args, UnitTest, filtered, [
            "id",
            ("kontext", "kontext.nazov"),
            "funkcia",
            "nazov",
            "status",
            ("datum_posledneho_behu", "datum_posledneho_behu", lambda i: formatuj_datum(i.datum_posledneho_behu)),
            ("spustac_posledneho_behu", lambda j: daj_popis_usera(j.spustac_posledneho_behu)),
            ("autor_id", lambda j: daj_popis_usera(j.autor_id)),
    ])

    return json.dumps(table.json())


@kontext_blueprint.route("/daj_zoznam_unit_testov_pre_filtre/", methods=["POST"])
def daj_zoznam_unit_testov_pre_filtre():
    loguj(request)
    funkcia = request.json["funkcia"]

    kontext_id = request.json["kontext"]

    status = request.json["status"]

    filtered = db.session.query(UnitTest)

    if kontext_id:
        filtered = filtered.filter(UnitTest.kontext_id == kontext_id)

    if funkcia:
        filtered = filtered.filter(UnitTest.funkcia == funkcia)

    if status:
        filtered = filtered.filter(UnitTest.status == status)

    vysledok = []

    for f in filtered:
        vysledok.append(f.id)

    response = CommonResponse()

    response.data = vysledok

    return json.dumps(response.__dict__)


@kontext_blueprint.route("/vrat_kontext/", methods=["GET"])
def vrat_kontext():
    loguj(request)
    kt_id = request.args.get("id")

    response = CommonResponse()

    response.data = Kontext.query.get(kt_id)

    return jsonpickle.encode(response)


@kontext_blueprint.route("/rozbor_viet_kontextu/", methods=["GET"])
def rozbor_viet_kontextu():
    loguj(request)
    kt_id = request.args.get("kontext_id")

    k = Kontext.query.get(kt_id)

    return render_template("m_kontext/rozbor_viet_kontextu.jinja.html", kontext=k, stromy_body="aaa\nbbb")

