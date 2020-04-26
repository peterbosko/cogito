from flask import Blueprint
from flask import render_template
from flask import request
from datatables import DataTable
from app.kt_service import *
import json
from app.sd_service import *

koncept_blueprint = Blueprint("koncept", __name__)


@koncept_blueprint.route("/daj_autocomplete_konceptov/", methods=["GET"])
def daj_autocomplete_konceptov():
    loguj(request)
    term = request.args.get("term", "")

    filtered = Koncept.query.filter(Koncept.nazov == term)

    if filtered.count() == 0:
        filtered = Koncept.query.filter(Koncept.nazov.like(term + "%"))

    autoc = []

    for koncept in filtered:
        rr = AutocompleteSingleResponse()
        rr.id = koncept.id
        rr.text = koncept.nazov
        autoc.append(rr)

    response = CommonResponse()

    response.status = ResponseStatus.OK

    response.data = autoc

    return jsonpickle.encode(response)


@koncept_blueprint.route("/kc_zakladne_info/", methods=["GET"])
def kc_zakladne_info():
    loguj(request)

    return render_template("m_koncept/zakladne_info.jinja.html")


@koncept_blueprint.route("/kc_rodicia_konceptu/", methods=["GET"])
def kc_rodicia_konceptu():
    loguj(request)

    return render_template("m_koncept/rodicia_konceptu.jinja.html")


@koncept_blueprint.route("/kc_atributy/", methods=["GET"])
def kc_atributy():
    loguj(request)

    return render_template("m_koncept/atributy.jinja.html")


@koncept_blueprint.route("/koncepty/", methods=["GET"])
def koncepty():
    loguj(request)
    return render_template("m_koncept/koncepty.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@koncept_blueprint.route("/zmenit_koncept/", methods=["GET"])
def zmenit_koncept():
    loguj(request)
    return render_template("m_koncept/zmenit_koncept.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@koncept_blueprint.route("/daj_koncepty/", methods=["GET"])
def daj_koncepty():
    loguj(request)

    koncept = request.args.get("koncept", "")

    filtered = db.session.query(Koncept)

    if koncept:
        filtered = filtered.filter(Koncept.nazov.like(koncept))

    table = DataTable(request.args, Koncept, filtered, [
            "id",
            "nazov",
    ])

    return json.dumps(table.json())
