from app.db_models import *
from app.c_helper import *


def som_admin():
    if "logged" in session.keys():
        usr = int(session["logged"])
        ja = User.query.get(usr)
        if ja.je_admin == "A":
            return True
        else:
            return False
    else:
        return False


def som_metadata_admin():
    if "logged" in session.keys():
        usr = int(session["logged"])
        ja = User.query.get(usr)
        if ja.je_metadata_admin == "A":
            return True
        else:
            return False
    else:
        return False


def som_admin_slov():
    if "logged" in session.keys():
        usr = int(session["logged"])
        ja = User.query.get(usr)
        if ja.je_admin_slov == "A":
            return True
        else:
            return False
    else:
        return False


def daj_typ_z_poctov_sd(rows, typ):
    pocet = 0
    # for r in rows:
    #    if r.SlovnyDruh.typ == typ:
    #        pocet = r[1]

    if typ == "POD_M":
        pocet = "174 tis"
    elif typ == "PRID_M":
        pocet = "180 tis"
    elif typ == "ZAMENO":
        pocet = "800"
    elif typ == "CISLOVKA":
        pocet = "1,750"
    elif typ == "PRISLOVKA":
        pocet = "11 tis"
    elif typ == "SLOVESO":
        pocet = "70 tis"
    elif typ == "PREDLOZKA":
        pocet = "180"
    elif typ == "SPOJKA":
        pocet = "150"
    elif typ == "CASTICA":
        pocet = "480"
    elif typ == "CITOSLOVCE":
        pocet = "1,140"
    elif typ == "OSTATNE":
        pocet = "1,500"

    if pocet == 0:
        pocet = "21 453 tis"  # db.session.query(Slovo).count()

    return formatuj_cislo(pocet)


