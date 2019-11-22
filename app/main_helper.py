from app.db_models import *


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

