from flask import Blueprint
from flask import request
from flask import render_template
from datatables import DataTable
from sqlalchemy import alias
from app.c_service import *
from app.main_helper import *
import jsonpickle
from app.sd_service import *

sd_blueprint = Blueprint("sd", __name__)


@sd_blueprint.route("/daj_slova/", methods=["GET"])
def daj_slova():
    loguj(request)

    tvar = request.args.get("hladaj_tvar", "")
    ztvar = request.args.get("hladaj_zak_tvar", "")
    druh = request.args.get("hladaj_druh", "")
    iba_anotovane = request.args.get("hladaj_iba_anotovane", "")
    anotacia = request.args.get("hladaj_anotaciu", "")
    id = request.args.get("hladaj_slovo_id", "")
    sd_id = request.args.get("hladaj_sd_id", "")

    filtered = db.session.query(Slovo)

    if id:
        filtered = filtered.filter(Slovo.id == id)

    if sd_id:
        filtered = filtered.filter(Slovo.sd_id == sd_id)

    if tvar:
        filtered = filtered.filter(Slovo.tvar.like(tvar))

    if ztvar:
        sd_a = alias(SlovnyDruh, name="slov_d")
        filtered = filtered.join(sd_a).filter(SlovnyDruh.zak_tvar.like(ztvar))

    if druh:
        sd_al = alias(SlovnyDruh, name="slov_d_al")
        filtered = filtered.join(sd_al).filter(Slovo.sd_id == SlovnyDruh.id).filter(SlovnyDruh.typ == druh)

    if iba_anotovane.lower() == "true":
        filtered = filtered.filter(Slovo.anotacia.isnot(None)).filter(Slovo.anotacia != '')

    if anotacia:
        filtered = filtered.filter(Slovo.anotacia.like(anotacia))

    table = DataTable(request.args, Slovo, filtered, [
            "id",
            "id",
            "tvar",
            ("slovny_druh", 'SlovnyDruh.typ'),
            ("zak_tvar", 'SlovnyDruh.zak_tvar'),
            "rod",
            "podrod",
            "pad",
            "cislo",
            "osoba",
            "cas",
            "sposob",
            "stupen",
            "zvratnost",
            "anotacia",
            "sd_id",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/zoznam_slov/", methods=["GET"])
def zoznam_slov():
    loguj(request)
    return render_template("m_sd/zoznam_slov.jinja.html")


@sd_blueprint.route("/zoznam_pm/", methods=["GET"])
def zoznam_pm():
    loguj(request)
    return render_template("m_sd/zoznam_pm.jinja.html")


@sd_blueprint.route("/zoznam_prid_m/", methods=["GET"])
def zoznam_prid_m():
    loguj(request)
    return render_template("m_sd/zoznam_prid_m.jinja.html")


@sd_blueprint.route("/zoznam_zamena/", methods=["GET"])
def zoznam_zamena():
    loguj(request)
    return render_template("m_sd/zoznam_zamena.jinja.html")


@sd_blueprint.route("/zoznam_cislovky/", methods=["GET"])
def zoznam_cislovky():
    loguj(request)
    return render_template("m_sd/zoznam_cislovky.jinja.html")


@sd_blueprint.route("/zoznam_prislovky/", methods=["GET"])
def zoznam_prislovky():
    loguj(request)
    return render_template("m_sd/zoznam_prislovky.jinja.html")


@sd_blueprint.route("/zoznam_slovesa/", methods=["GET"])
def zoznam_slovesa():
    loguj(request)

    ir = IntencnyRamec.query.order_by(IntencnyRamec.kod)

    return render_template("m_sd/zoznam_slovesa.jinja.html", intencne_ramce=ir)


@sd_blueprint.route("/zoznam_spojky/", methods=["GET"])
def zoznam_spojky():
    loguj(request)
    return render_template("m_sd/zoznam_spojky.jinja.html")


@sd_blueprint.route("/zoznam_castice/", methods=["GET"])
def zoznam_castice():
    loguj(request)
    return render_template("m_sd/zoznam_castice.jinja.html")


@sd_blueprint.route("/zoznam_predlozky/", methods=["GET"])
def zoznam_predlozky():
    loguj(request)
    return render_template("m_sd/zoznam_predlozky.jinja.html")


@sd_blueprint.route("/zoznam_citoslovcia/", methods=["GET"])
def zoznam_citoslovcia():
    loguj(request)
    return render_template("m_sd/zoznam_citoslovcia.jinja.html")


@sd_blueprint.route("/zoznam_ostatne/", methods=["GET"])
def zoznam_ostatne():
    loguj(request)
    return render_template("m_sd/zoznam_ostatne.jinja.html")


def daj_zakladny_tvar_sd(idsd):
    if not idsd:
        return ""
    else:
        sd = SlovnyDruh.query.get(idsd)
        return sd.zak_tvar


@sd_blueprint.route("/daj_pm/", methods=["GET"])
def daj_pm():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    rod = request.args.get("hladaj_rod", "")

    filtered = db.session.query(PodstatneMeno)

    if tvar:
        filtered = filtered.filter(PodstatneMeno.zak_tvar.like(tvar))

    if rod:
        filtered = filtered.filter(PodstatneMeno.rod == rod)

    table = DataTable(request.args, PodstatneMeno, filtered, [
            "id",
            "id",
            "zak_tvar",
            "popis",
            "rod",
            "podrod",
            ("sloveso_id", lambda i: daj_zakladny_tvar_sd(i.sloveso_id)),
            "je_negacia",

    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_prid_m/", methods=["GET"])
def daj_prid_m():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(PridavneMeno)

    if tvar:
        filtered = filtered.filter(PridavneMeno.zak_tvar.like(tvar))

    table = DataTable(request.args, PodstatneMeno, filtered, [
            "id",
            "id",
            "zak_tvar",
            "popis",
            ("sloveso_id", lambda i: daj_zakladny_tvar_sd(i.sloveso_id)),
            "je_negacia",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_zamena/", methods=["GET"])
def daj_zamena():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    rod = request.args.get("hladaj_rod", "")

    filtered = db.session.query(Zameno)

    if tvar:
        filtered = filtered.filter(Zameno.zak_tvar.like(tvar))

    if rod:
        filtered = filtered.filter(Zameno.rod == rod)

    table = DataTable(request.args, Zameno, filtered, [
            "id",
            "zak_tvar",
            "popis",
            "cislo",
            "rod",
            "podrod",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_cislovky/", methods=["GET"])
def daj_cislovky():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    rod = request.args.get("hladaj_rod", "")

    cislo = request.args.get("hladaj_cislo", "")

    filtered = db.session.query(Cislovka)

    if tvar:
        filtered = filtered.filter(Cislovka.zak_tvar == tvar)

    if rod:
        filtered = filtered.filter(Cislovka.rod == rod)

    if cislo:
        filtered = filtered.filter(Cislovka.cislo == cislo)

    table = DataTable(request.args, Zameno, filtered, [
            "id",
            "zak_tvar",
            "popis",
            "hodnota",
            "rod",
            "podrod",
            "cislo",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_prislovky/", methods=["GET"])
def daj_prislovky():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(Prislovka)

    if tvar:
        filtered = filtered.filter(Prislovka.zak_tvar.like(tvar))

    table = DataTable(request.args, Zameno, filtered, [
            "id",
            "zak_tvar",
            "popis",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_slovesa/", methods=["GET"])
def daj_slovesa():
    loguj(request)

    tvar = request.args.get("hladaj_tvar", "")
    popis = request.args.get("hladaj_popis", "")
    ir = request.args.get("hladaj_ir", "")

    filtered = db.session.query(SlovesoView)

    if tvar:
        filtered = filtered.filter(SlovesoView.zak_tvar.like(tvar))

    if popis:
        filtered = filtered.filter(SlovesoView.popis.like(popis))

    if ir:
        if ir == "-1":
            filtered = filtered.filter(SlovesoView.int_ramec_id.isnot(None))
        else:
            filtered = filtered.filter(SlovesoView.int_ramec_id == int(ir))

    table = DataTable(request.args, SlovesoView, filtered, [
            "id",
            "zak_tvar",
            "zvratnost",
            "popis",
            "je_negacia",
            "int_ramec_kod",
            "int_ramec_nazov",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_predlozky/", methods=["GET"])
def daj_predlozky():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(Predlozka)

    if tvar:
        filtered = filtered.filter(Predlozka.zak_tvar == tvar)

    table = DataTable(request.args, Predlozka, filtered, [
            "id",
            "zak_tvar",
            "popis",
            "pady",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_spojky/", methods=["GET"])
def daj_spojky():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(Spojka)

    if tvar:
        filtered = filtered.filter(Spojka.zak_tvar == tvar)

    table = DataTable(request.args, Spojka, filtered, [
            "id",
            "zak_tvar",
            "popis",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_castice/", methods=["GET"])
def daj_castice():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(Castica)

    if tvar:
        filtered = filtered.filter(Castica.zak_tvar == tvar)

    table = DataTable(request.args, Castica, filtered, [
            "id",
            "zak_tvar",
            "popis",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_citoslovcia/", methods=["GET"])
def daj_citoslovcia():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(Citoslovce)

    if tvar:
        filtered = filtered.filter(Citoslovce.zak_tvar == tvar)

    table = DataTable(request.args, Citoslovce, filtered, [
            "id",
            "zak_tvar",
            "popis",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/daj_ostatne/", methods=["GET"])
def daj_ostatne():
    loguj(request)
    tvar = request.args.get("hladaj_tvar", "")

    filtered = db.session.query(Ostatne)

    if tvar:
        filtered = filtered.filter(Ostatne.zak_tvar == tvar)

    table = DataTable(request.args, Ostatne, filtered, [
            "id",
            "zak_tvar",
            "popis",
    ])

    return json.dumps(table.json())


@sd_blueprint.route("/pridaj_slovo_vyber_sd/", methods=["GET"])
def pridaj_slovo_vyber_sd():
    loguj(request)
    return render_template("m_sd/pridaj_slovo_vyber_sd.jinja.html")


@sd_blueprint.route("/zmenit_sd/", methods=['POST'])
def zmenit_sd_post():
    loguj(request)
    response = CommonResponse()

    if som_admin_slov():
        js = request.json
        js["py/object"] = ".".join([SDExport.__module__, SDExport.__name__])
        strjson = str(js).replace("'", '"')
        export = jsonpickle.decode(strjson)

        if export.typ == "POD_M":
            if export.id is not None and int(export.id) > 0:
                pm = PodstatneMeno.query.get(export.id)
            else:
                pm = PodstatneMeno()

            if export.tab == "zakladne":

                pm.zak_tvar = export.zak_tvar
                pm.popis = export.popis
                pm.rod = export.rod
                pm.podrod = export.podrod

                if pm.sloveso_id and not export.sloveso_id:
                    pm.sloveso_id = None

                if export.sloveso_id:
                    pm.sloveso_id = export.sloveso_id

                if export.pocitatelnost:
                    pm.pocitatelnost = export.pocitatelnost
                else:
                    pm.pocitatelnost = None

                if export.sem_priznak_id:
                    pm.sem_priznak_id = export.sem_priznak_id
                else:
                    pm.sem_priznak_id = None

            elif export.tab == "slova":
                pm.koren = export.koren
                pm.vzor = export.vzor
                pm.prefix = export.prefix
                pm.sufix = export.sufix
                pm.paradigma = export.paradigma

            db.session.add(pm)
            db.session.commit()

            sd_id = pm.id

        elif export.typ == "PRID_M":
            if export.id is not None and int(export.id) > 0:
                prm = PridavneMeno.query.get(export.id)
            else:
                prm = PridavneMeno()

            if export.tab == "zakladne":
                prm.zak_tvar = export.zak_tvar
                prm.popis = export.popis

                if prm.sloveso_id and not export.sloveso_id:
                    prm.sloveso_id = None

                if export.sloveso_id:
                    prm.sloveso_id = export.sloveso_id

                prm.je_privlastnovacie = export.je_privlastnovacie

            elif export.tab == "slova":
                prm.koren = export.koren
                prm.vzor = export.vzor
                prm.prefix = export.prefix
                prm.sufix = export.sufix
                prm.paradigma = export.paradigma
                prm.vzor_stup = export.vzor_stup

            db.session.add(prm)
            db.session.commit()

            sd_id = prm.id

        elif export.typ == "ZAMENO":
            if export.id is not None and int(export.id) > 0:
                zam = Zameno.query.get(export.id)
            else:
                zam = Zameno()

            zam.zak_tvar = export.zak_tvar
            zam.popis = export.popis

            zam.rod = export.rod
            zam.podrod = export.podrod
            zam.cislo = export.cislo

            db.session.add(zam)
            db.session.commit()

            sd_id = zam.id
        elif export.typ == "SLOVESO":
            if export.id is not None and int(export.id) > 0:
                s = Sloveso.query.get(export.id)
            else:
                s = Sloveso()
            s.zak_tvar = export.zak_tvar
            s.popis = export.popis

            s.zvratnost = export.zvratnost
            s.je_negacia = export.je_negacia

            if s.pozitivne_sloveso_id and not export.sloveso_id:
                s.pozitivne_sloveso_id = None

            if export.sloveso_id:
                s.pozitivne_sloveso_id = export.sloveso_id

            db.session.add(s)
            db.session.commit()

            sd_id = s.id

        elif export.typ == "PREDLOZKA":
            if export.id is not None and int(export.id) > 0:
                pr = Predlozka.query.get(export.id)
            else:
                pr = Predlozka()

            pr.zak_tvar = export.zak_tvar
            pr.popis = export.popis

            pr.pady = export.pady

            db.session.add(pr)
            db.session.commit()

            sd_id = pr.id
        elif export.typ == "CISLOVKA":
            if export.id is not None and int(export.id) > 0:
                cis = Cislovka.query.get(export.id)
            else:
                cis = Cislovka()
            cis.zak_tvar = export.zak_tvar
            cis.popis = export.popis

            cis.rod = export.rod
            cis.podrod = export.podrod
            cis.cislo = export.cislo
            cis.hodnota = export.hodnota

            db.session.add(cis)
            db.session.commit()

            sd_id = cis.id
        elif export.typ == "CITOSLOVCE":
            if export.id is not None and int(export.id) > 0:
                cit = Citoslovce.query.get(export.id)
            else:
                cit = Citoslovce()
            cit.zak_tvar = export.zak_tvar
            cit.popis = export.popis
            db.session.add(cit)
            db.session.commit()
            sd_id = cit.id
        elif export.typ == "CASTICA":
            if export.id is not None and int(export.id) > 0:
                castica = Castica.query.get(export.id)
            else:
                castica = Castica()
            castica.zak_tvar = export.zak_tvar
            castica.popis = export.popis
            db.session.add(castica)
            db.session.commit()
            sd_id = castica.id
        elif export.typ == "OSTATNE":
            if export.id is not None and int(export.id) > 0:
                ostatne = Ostatne.query.get(export.id)
            else:
                ostatne = Ostatne()
            ostatne.zak_tvar = export.zak_tvar
            ostatne.popis = export.popis

            db.session.add(ostatne)
            db.session.commit()
            sd_id = ostatne.id
        elif export.typ == "PRISLOVKA":
            if export.id is not None and int(export.id) > 0:
                prislovka = Prislovka.query.get(export.id)
            else:
                prislovka = Prislovka()
            prislovka.zak_tvar = export.zak_tvar
            prislovka.popis = export.popis

            db.session.add(prislovka)
            db.session.commit()
            sd_id = prislovka.id
        elif export.typ == "SPOJKA":
            if export.id is not None and int(export.id) > 0:
                spojka = Spojka.query.get(export.id)
            else:
                spojka = Spojka()
            spojka.zak_tvar = export.zak_tvar
            spojka.popis = export.popis

            db.session.add(spojka)
            db.session.commit()
            sd_id = spojka.id

        if export.tab == "slova":

            for sl in export.slova:
                if sl['id']:
                    slovo = Slovo.query.get(sl['id'])
                else:
                    slovo = Slovo()

                slovo.tvar = sl['tvar']
                slovo.rod = sl['rod'][0]

                if '/' in sl['rod']:
                    slovo.podrod = sl['rod'][2]
                else:
                    slovo.podrod = ""

                slovo.stupen = sl['stupen']
                slovo.pad = sl['pad']
                slovo.sposob = sl['sposob']
                slovo.osoba = sl['osoba']
                slovo.cas = sl['cas']
                slovo.pricastie = sl['pricastie']
                slovo.cislo = sl['cislo']
                slovo.zvratnost = sl["zvratnost"]
                slovo.anotacia = sl['anotacia']
                slovo.sd_id = sd_id

                if export.typ == "SLOVESO":
                    if 'I' in sl['anotacia']:
                        slovo.je_neurcitok = 'A'
                    else:
                        slovo.je_neurcitok = 'N'
                    if '-' in sl['anotacia']:
                        slovo.je_negacia = 'A'
                    elif '+' in sl['anotacia']:
                        slovo.je_negacia = 'N'
                    if 'H' in sl['anotacia']:
                        slovo.je_prechodnik= 'A'
                    else:
                        slovo.je_prechodnik = 'N'

                slovo.user_id = int(session["logged"])
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)
                db.session.commit()

            for slovo in export.zmazaneSlova:
                slovo_id = int(slovo)
                if slovo_id > 0:
                    db.session.delete(Slovo.query.get(slovo_id))

        db.session.commit()

        response.data = sd_id

    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return json.dumps(response.__dict__)


@sd_blueprint.route("/zmenit_sd/", methods=["GET"])
def zmenit_sd():
    loguj(request)
    return render_template("m_sd/zmenit_sd2.jinja.html")


@sd_blueprint.route("/sd_zakladne_info/", methods=["GET"])
def sd_zakladne_info():
    loguj(request)
    kts = Kontext.query.order_by(Kontext.nazov)

    sem_priz_pod_m = Semantika.query.filter(Semantika.typ == "POD_M").all()

    sem_priz_prid_m = Semantika.query.filter(Semantika.typ == "PRID_M").all()

    sem_priz_cislovka = Semantika.query.filter(Semantika.typ == "CISLOVKA").all()

    return render_template("m_sd/sd_zakladne_info.jinja.html", sem_priz_pod_m=sem_priz_pod_m,
                           sem_priz_prid_m=sem_priz_prid_m, sem_priz_cislovka=sem_priz_cislovka)


@sd_blueprint.route("/sd_slova_zmen/", methods=["GET"])
def sd_slova_zmen():
    loguj(request)
    return render_template("m_sd/sd_slova_zmen.jinja.html")


@sd_blueprint.route("/sd_rodicia/", methods=["GET"])
def sd_rodicia():
    loguj(request)
    return render_template("m_sd/sd_rodicia.jinja.html")


@sd_blueprint.route("/sd_slova/", methods=["GET"])
def sd_slova():
    loguj(request)
    return render_template("m_sd/sd_slova.jinja.html")


@sd_blueprint.route("/daj_autocomplete_slovies/", methods=["GET"])
def daj_autocomplete_slovies():
    loguj(request)
    term = request.args.get("term", "")

    filtered = Sloveso.query.filter(Sloveso.zak_tvar == term). \
        join(Slovo).filter(Slovo.anotacia.isnot(None)).filter(Slovo.anotacia != "")

    if filtered.count() == 0:
        filtered = Sloveso.query.filter(Sloveso.zak_tvar.like(term + "%")).\
            join(Slovo).filter(Slovo.anotacia.isnot(None)).filter(Slovo.anotacia != "")

    autoc = []

    for sloveso in filtered:
        rr = AutocompleteSingleResponse()
        rr.id = sloveso.id
        rr.text = sloveso.zak_tvar
        if sloveso.zvratnost:
            rr.text += " " + sloveso.zvratnost

        autoc.append(rr)

    response = CommonResponse()

    response.status = ResponseStatus.OK

    response.data = autoc

    return jsonpickle.encode(response)


@sd_blueprint.route("/vrat_sd_id/", methods=["GET"])
def vrat_sd_id():
    sd_id = request.args.get("sd_id", "")
    slovo = request.args.get("slovo", "")
    sdruh = request.args.get("slovnyDruh", "")

    if sd_id and sd_id != "None":
        pass
    else:
        if slovo and slovo != "None":
            sd_al = alias(SlovnyDruh, name="slov_d_al")
            sl = db.session.query(Slovo).filter(Slovo.tvar == slovo)
            sl = sl.join(sd_al).filter(Slovo.sd_id == SlovnyDruh.id).filter(SlovnyDruh.typ == sdruh)

            if sl.count() >= 1:
                sd_id = sl.first().sd_id
            else:
                sd_id = -1

    response = CommonResponse()

    if sd_id and sd_id != "None":
        response.status = ResponseStatus.OK

        response.data = sd_id

    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Zlé parametre !"

    return jsonpickle.encode(response)


@sd_blueprint.route("/vrat_cely_slovny_druh/", methods=["GET"])
def vrat_cely_slovny_druh():
    loguj(request)
    sd_id = request.args.get("sd_id", "")

    response = CommonResponse()

    slovny_druh = SlovnyDruh.query.get(sd_id)

    sd_export = slovny_druh.exportujPlnySD()

    response.status = ResponseStatus.OK

    response.data = sd_export

    response.data.vzory = daj_vsetky_vzory()

    response.data.prefix_sufix = daj_vsetky_prefix_sufix()

    return jsonpickle.encode(response)


@sd_blueprint.route("/zmaz_cely_slovny_druh/", methods=["GET"])
def zmaz_cely_slovny_druh():
    loguj(request)
    sd_id = request.args.get("sd_id", "")

    response = CommonResponse()
    response.status = ResponseStatus.OK

    if som_admin_slov():

        Slovo.query.filter(Slovo.sd_id == sd_id).delete()

        sd = SlovnyDruh.query.get(sd_id)

        if sd.typ == "POD_M":
            pm = PodstatneMeno.query.get(sd_id)
            db.session.delete(pm)
        elif sd.typ == "PRID_M":
            prm = PridavneMeno.query.get(sd_id)
            db.session.delete(prm)
        elif sd.typ == "ZAMENO":
            zam = Zameno.query.get(sd_id)
            db.session.delete(zam)
        elif sd.typ == "CISLOVKA":
            cislovka = Cislovka.query.get(sd_id)
            db.session.delete(cislovka)
        elif sd.typ == "SPOJKA":
            sp = Spojka.query.get(sd_id)
            db.session.delete(sp)
        elif sd.typ == "PREDLOZKA":
            predlo = Predlozka.query.get(sd_id)
            db.session.delete(predlo)
        elif sd.typ == "OSTATNE":
            os = Ostatne.query.get(sd_id)
            db.session.delete(os)
        elif sd.typ == "CITOSLOVCE":
            cit = Citoslovce.query.get(sd_id)
            db.session.delete(cit)
        elif sd.typ == "CASTICA":
            c = Castica.query.get(sd_id)
            db.session.delete(c)
        elif sd.typ == "PRISLOVKA":
            prisl = Prislovka.query.get(sd_id)
            db.session.delete(prisl)
        elif sd.typ == "SLOVESO":
            sloveso = Sloveso.query.get(sd_id)
            db.session.delete(sloveso)

        db.session.commit()
    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Nedostatočné práva pre operáciu"

    return jsonpickle.encode(response)


@sd_blueprint.route("/generuj_morfo/", methods=["POST"])
def generuj_morfo():
    loguj(request)
    response = CommonResponse()

    js = request.json
    js["py/object"] = ".".join([MorfoFilter.__module__, MorfoFilter.__name__])
    strjson = str(js).replace("'", '"')
    morfo = jsonpickle.decode(strjson)

    sd = SlovnyDruh.query.get(morfo.sd_id)

    vysledok = []

    if sd.typ == "POD_M":

        podm = PodstatneMeno.query.get(morfo.sd_id)

        vzor_obj = SDVzor.query.filter(SDVzor.vzor == morfo.vzor).filter(SDVzor.rod == podm.rod).first()

        if not vzor_obj:
            response.error_text = f"Nenašiel sa vzor: {morfo.vzor} rod:{podm.rod}"
            response.status = ResponseStatus.ERROR
        else:
            vysledok = generuj_morfo_pm(morfo, vzor_obj.deklinacia, vzor_obj.alternacia, morfo.paradigma, podm.rod,
                                        podm.podrod)
    elif sd.typ == "PRID_M":

        pridm = PridavneMeno.query.get(morfo.sd_id)

        if not morfo.vzor or not morfo.vzor_stup:
            response.error_text = f"Nie je nastavený skloňovací alebo stupňovací vzor !"
            response.status = ResponseStatus.ERROR
        else:
            vysledok = generuj_morfo_prid_m(morfo)

    response.data = vysledok

    return jsonpickle.encode(response)

