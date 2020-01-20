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


@metadata_blueprint.route("/intencne_ramce/")
def intencne_ramce():
    loguj(request)
    return render_template("m_metadata/intencne_ramce.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/slovesa_ir/")
def slovesa_ir():
    loguj(request)
    return render_template("m_metadata/slovesa_ir.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/slovesa_sp/")
def slovesa_sp():
    loguj(request)
    return render_template("m_metadata/slovesa_sp.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/intencie_sp/")
def intencie_sp():
    loguj(request)
    return render_template("m_metadata/intencie_sp.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/intencie_ir/")
def intencie_ir():
    loguj(request)
    return render_template("m_metadata/intencie_ir.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/sp/")
def sp():
    loguj(request)
    return render_template("m_metadata/sp.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/vzory/")
def vzory():
    loguj(request)
    return render_template("m_metadata/vzory.jinja.html", pocty_sd=daj_pocty_sd_a_sl())


@metadata_blueprint.route("/daj_sp/", methods=["GET"])
def daj_sp():
    loguj(request)

    nazov = request.args.get("hladaj_nazov", "")
    kod = request.args.get("hladaj_kod", "")

    filtered = db.session.query(SemantickyPadView)

    if nazov:
        filtered = filtered.filter(SemantickyPadView.nazov.like(nazov))

    if kod:
        filtered = filtered.filter(SemantickyPadView.kod.like(kod))

    table = DataTable(request.args, SemantickyPadView, filtered, [
            "id",
            "kod",
            "nazov",
            "pocet_intencii",
            "pocet_slovies",
    ])

    return json.dumps(table.json())


@metadata_blueprint.route("/daj_ir/", methods=["GET"])
def daj_ir():
    loguj(request)

    nazov = request.args.get("hladaj_nazov", "")
    kod = request.args.get("hladaj_kod", "")

    filtered = db.session.query(IntencnyRamecView)

    if nazov:
        filtered = filtered.filter(IntencnyRamecView.nazov.like(nazov))

    if kod:
        filtered = filtered.filter(IntencnyRamecView.kod.like(kod))

    table = DataTable(request.args, IntencnyRamecView, filtered, [
            "id",
            "kod",
            "nazov",
            "pocet_intencii",
            "pocet_slovies",
    ])

    return json.dumps(table.json())


def obstaraj_null_string_sem(s):
    if s:
        return s.kod
    return ""


@metadata_blueprint.route("/daj_intencie_sp/", methods=["GET"])
def daj_intencie_sp():
    loguj(request)

    semp = int(request.args.get("sp", ""))

    filtered = db.session.query(Intencia)

    filtered = filtered.filter(Intencia.sem_pad_id == semp)

    table = DataTable(request.args, Intencia, filtered, [
            "typ",
            ("int_ramec", "int_ramec.nazov"),
            "predlozka",
            "pad",
            ("sem_priznak", "sem_priznak", lambda j: obstaraj_null_string_sem(j.sem_priznak)),
            "fl",
    ])

    return json.dumps(table.json())


@metadata_blueprint.route("/daj_intencie_ramca/", methods=["GET"])
def daj_intencie_ramca():
    loguj(request)

    ir = int(request.args.get("ramec_id", ""))

    filtered = db.session.query(Intencia)

    filtered = filtered.filter(Intencia.int_ramec_id == ir)

    table = DataTable(request.args, Intencia, filtered, [
            "id",
            "typ",
            "predlozka",
            "pad",
            ("sem_priznak", "sem_priznak", lambda j: obstaraj_null_string_sem(j.sem_priznak)),
            ("sem_pad", "sem_pad.nazov"),
            "fl",
    ])

    return json.dumps(table.json())


@metadata_blueprint.route("/daj_slovesa_ir/", methods=["GET"])
def daj_slovesa_ir():
    loguj(request)

    ir = int(request.args.get("ramec_id", ""))

    filtered = db.session.query(IntencieSlovesaView)

    filtered = filtered.filter(IntencieSlovesaView.int_ramec_id == ir)

    sloveso = request.args.get("sloveso", "")

    if sloveso:
        filtered = filtered.filter(IntencieSlovesaView.zak_tvar.like(sloveso))

    predlozka = request.args.get("predlozka", "")

    if predlozka:
        filtered = filtered.filter(IntencieSlovesaView.predlozka.like(predlozka))

    gpad = request.args.get("pad", "")

    if gpad:
        filtered = filtered.filter(IntencieSlovesaView.pad == gpad)

    table = DataTable(request.args, IntencieSlovesaView, filtered, [
            "zak_tvar",
            "zvratnost",
            "vid",
            "popis",
            "typ",
            "predlozka",
            "pad",
            "sem_kod",
            "sp_nazov",
            "fl"
    ])

    return json.dumps(table.json())


@metadata_blueprint.route("/daj_slovesa_sp/", methods=["GET"])
def daj_slovesa_sp():
    loguj(request)

    sp = int(request.args.get("sp", ""))

    filtered = db.session.query(IntencieSlovesaView)

    filtered = filtered.filter(IntencieSlovesaView.sem_pad_id == sp)

    sloveso = request.args.get("sloveso", "")

    if sloveso:
        filtered = filtered.filter(IntencieSlovesaView.zak_tvar.like(sloveso))

    predlozka = request.args.get("predlozka", "")

    if predlozka:
        filtered = filtered.filter(IntencieSlovesaView.predlozka.like(predlozka))

    gpad = request.args.get("pad", "")

    if gpad:
        filtered = filtered.filter(IntencieSlovesaView.pad == gpad)

    table = DataTable(request.args, IntencieSlovesaView, filtered, [
        "zak_tvar",
        "zvratnost",
        "vid",
        "popis",
        "typ",
        "predlozka",
        "pad",
        "sem_kod",
        "ir_nazov",
        "fl"
        ])

    return json.dumps(table.json())


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

    if t == "PRID_M":
        table = DataTable(request.args, SemHierarchiaView, filtered, [
                "sem_priznak_id",
                "kod",
                "nazov",
                "rodic_kod",
                "rodic_nazov",
                ("pocet_slov", "pocet_slov_prid_m"),
        ])
    else:
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

    if t == "PRID_M":
        filtered = db.session.query(PridavneMeno).filter(PridavneMeno.sem_priznak_prid_m_id == sem_priznak)

        table = DataTable(request.args, PridavneMeno, filtered, [
            "typ",
            "zak_tvar",
        ])
    else:
        filtered = db.session.query(SlovnyDruh).filter(SlovnyDruh.sem_priznak_id == sem_priznak)

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


