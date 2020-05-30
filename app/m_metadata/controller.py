from flask import Blueprint
from flask import render_template
from flask import request
from app.c_service import *
from datatables import DataTable
from app.main_helper import *
from app.sd_service import *
import jsonpickle

metadata_blueprint = Blueprint("metadata", __name__)


@metadata_blueprint.route("/sem_priznak_strom/")
def sem_priznak_strom():
    loguj(request)
    return render_template("m_metadata/sem_priznak_strom.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/slova_sem_priz/")
def slova_sem_priz():
    loguj(request)
    return render_template("m_metadata/slova_sem_priz.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/sem_priznaky_typ/")
def sem_priznaky_typ():
    loguj(request)
    return render_template("m_metadata/sem_priznaky_typ.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/sem_priznaky/")
def sem_priznaky():
    loguj(request)
    return render_template("m_metadata/sem_priznaky.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/vzory/")
def vzory():
    loguj(request)
    return render_template("m_metadata/vzory.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


def obstaraj_null_string_sem(s):
    if s:
        return s.kod
    return ""


@metadata_blueprint.route("/daj_sem_priznaky/", methods=["GET"])
def daj_sem_priznaky():
    loguj(request)

    t = request.args.get("typ", "")
    sem_priznak = request.args.get("sem_priznak", "")
    rodic_priznak = request.args.get("rodic_priznak", "")

    filtered = db.session.query(SemHierarchiaView).filter(SemHierarchiaView.typ == t)

    if sem_priznak:
        filtered = filtered.filter(SemHierarchiaView.kod.like(sem_priznak))

    if rodic_priznak:
        filtered = filtered.filter(SemHierarchiaView.rodic_kod.like(rodic_priznak))

    table = DataTable(request.args, SemHierarchiaView, filtered, [
            "sem_priznak_id",
            "kod",
            "nazov",
            "rodic_kod",
            "rodic_nazov",
            "pocet_slov"
        ])

    return json.dumps(table.json())


@metadata_blueprint.route("/daj_slova_sem_priz/", methods=["GET"])
def daj_slova_sem_priz():
    loguj(request)

    t = request.args.get("typ", "")

    sem_priznak = request.args.get("sem_priznak", "")

    filtered = db.session.query(SlovnyDruh).join(SlovnyDruhSemantika).filter(SlovnyDruhSemantika.sem_priznak_id ==
                                                                             int(sem_priznak))

    table = DataTable(request.args, SlovnyDruh, filtered, [
            "typ",
            "zak_tvar",
    ])

    return json.dumps(table.json())


@metadata_blueprint.route("/daj_sem_strom/", methods=["GET"])
def daj_sem_strom():
    loguj(request)

    smer = request.args.get("smer", "")
    sem_priznak = request.args.get("sem_priznak", "")

    data = vrat_data_sem_stromu(sem_priznak, smer)

    return jsonpickle.encode(data)


@metadata_blueprint.route("/daj_vzory/", methods=["GET"])
def daj_vzory():
    loguj(request)

    filtered = db.session.query(SDVzor)

    typ = request.args.get("typ", "")
    vzor = request.args.get("vzor", "")
    deklinacia = request.args.get("deklinacia", "")
    alternacia = request.args.get("alternacia", "")
    sklon_stup = request.args.get("SklonStupCas", "")

    if typ:
        filtered = filtered.filter(SDVzor.typ == typ)

    if vzor:
        filtered = filtered.filter(SDVzor.vzor.like(vzor))

    if deklinacia:
        filtered = filtered.filter(SDVzor.deklinacia.like(deklinacia))

    if alternacia:
        filtered = filtered.filter(SDVzor.alternacia.like(alternacia))

    if sklon_stup:
        filtered = filtered.filter(SDVzor.sklon_stup == sklon_stup)

    table = DataTable(request.args, SDVzor, filtered, [
            "id",
            "vzor",
            "typ",
            "rod",
            "podrod",
            "sklon_stup",
            "deklinacia",
            "alternacia",
            "popis"
    ])

    return json.dumps(table.json())


