from importy.sapfo.service import *
from app.db_models import *


def vrat_pod_m(slovo, sufix):
    with flask_app.app_context():
        pm_objekty = PodstatneMeno.query.filter(PodstatneMeno.zak_tvar.like(slovo+"%")).\
            filter(PodstatneMeno.zak_tvar.like('%'+sufix))

        b_sufix = True

        if pm_objekty.count() == 0:
            pm_objekty = PodstatneMeno.query.filter(PodstatneMeno.zak_tvar.like(slovo + "%"))
            b_sufix = False

        slovo_id = None
        sql = ""

        if pm_objekty.count() == 1:
            slovo_id = pm_objekty.first().id
        elif pm_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            sql = "SELECT sd.*,sd_pod_m.* FROM sd_pod_m JOIN sd ON sd.id=sd_pod_m.id WHERE zak_tvar LIKE '"+slovo+"%'"

            if b_sufix:
                sql = sql + " AND zak_tvar LIKE '%"+sufix+"'"

        return slovo_id, sql

    return None, ""


def vrat_prid_m(slovo, sufix):
    with flask_app.app_context():
        pr_objekty = PridavneMeno.query.filter(PridavneMeno.zak_tvar.like(slovo+"%")).\
            filter(PridavneMeno.zak_tvar.like('%'+sufix))

        b_sufix = True

        if pr_objekty.count() == 0:
            pr_objekty = PridavneMeno.query.filter(PridavneMeno.zak_tvar.like(slovo+"%"))
            b_sufix = False

        slovo_id = None
        sql = ""

        if pr_objekty.count() == 1:
            slovo_id = pr_objekty.first().id
        elif pr_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            sql = "SELECT sd.*,sd_prid_m.* FROM sd_prid_m JOIN sd ON sd.id=sd_prid_m.id WHERE zak_tvar " \
                  "LIKE '"+slovo+"%'"
            if b_sufix:
                sql = sql + " AND zak_tvar LIKE '%"+sufix+"'"

        return slovo_id, sql

    return None, ""


def vrat_sloveso(slovo, sufix, zvratnost):
    with flask_app.app_context():

        z = None

        if zvratnost != "nezv":
            z = zvratnost

        sl_objekty = Sloveso.query.filter(Sloveso.zak_tvar.like(slovo+"%")).\
            filter(Sloveso.zak_tvar.like('%'+sufix)).\
            filter(Sloveso.zvratnost == z)

        b_sufix = True

        if sl_objekty.count() == 0:
            sl_objekty = Sloveso.query.filter(Sloveso.zak_tvar.like(slovo + "%")). \
                filter(Sloveso.zvratnost == z)
            b_sufix = False

        slovo_id = None
        sql = ""

        if sl_objekty.count() == 1:
            slovo_id = sl_objekty.first().id
        elif sl_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            if z:
                sql = "SELECT sd.*,sd_sloveso.* FROM sd_sloveso JOIN sd ON sd.id=sd_sloveso.id WHERE zak_tvar " \
                      "LIKE '"+slovo+"%' AND zvratnost='"+z+"'"
            else:
                sql = "SELECT sd.*,sd_sloveso.* FROM sd_sloveso JOIN sd ON sd.id=sd_sloveso.id WHERE zak_tvar " \
                      "LIKE '"+slovo+"%' AND ISNULL(zvratnost)=1"
            if b_sufix:
                sql = sql + " AND zak_tvar LIKE '%"+sufix+"'"

        return slovo_id, sql

    return None, ""


def vrat_prislovku(slovo):
    with flask_app.app_context():
        adv_objekty = Prislovka.query.filter(Prislovka.zak_tvar.like(slovo+"%"))

        slovo_id = None
        sql = ""

        if adv_objekty.count() == 1:
            slovo_id = adv_objekty.first().id
        elif adv_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            sql = "SELECT sd.*,sd_prislovka.* FROM sd_prislovka JOIN sd ON sd.id=sd_prislovka.id WHERE zak_tvar " \
                  "LIKE '"+slovo+"%'"

        return slovo_id, sql

    return None, ""


def vrat_cislovku(slovo):
    with flask_app.app_context():
        cis_objekty = Cislovka.query.filter(Cislovka.zak_tvar.like(slovo+"%"))

        slovo_id = None
        sql = ""

        if cis_objekty.count() == 1:
            slovo_id = cis_objekty.first().id
        elif cis_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            sql = "SELECT sd.*,sd_cislovka.* FROM sd_cislovka JOIN sd ON sd.id=sd_cislovka.id WHERE zak_tvar " \
                  "LIKE '"+slovo+"%'"

        return slovo_id, sql

    return None, ""


def vrat_citoslovce(slovo):
    with flask_app.app_context():
        cit_objekty = Citoslovce.query.filter(Citoslovce.zak_tvar == slovo)

        slovo_id = None
        sql = ""

        if cit_objekty.count() == 1:
            slovo_id = cit_objekty.first().id
        elif cit_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            sql = "SELECT sd.*,sd_citoslovce.* FROM sd_citoslovce JOIN sd ON sd.id=sd_citoslovce.id WHERE zak_tvar " \
                  "LIKE '"+slovo+"'"

        return slovo_id, sql

    return None, ""


def vrat_casticu(slovo):
    with flask_app.app_context():
        cast_objekty = Castica.query.filter(Castica.zak_tvar.like(slovo))

        slovo_id = None
        sql = ""

        if cast_objekty.count() == 1:
            slovo_id = cast_objekty.first().id
        elif cast_objekty.count() == 0:
            sql = "Chýba v db"
        else:
            sql = "SELECT sd.*,sd_castica.* FROM sd_castica JOIN sd ON sd.id=sd_castica.id WHERE zak_tvar " \
                  "LIKE '"+slovo+"'"

        return slovo_id, sql

    return None, ""


def vrat_slovesa_podla_pzkmena(pzkmen):
    with flask_app.app_context():
        slovesa = Sloveso.query.filter(Sloveso.pzkmen == pzkmen).all()
        return slovesa

