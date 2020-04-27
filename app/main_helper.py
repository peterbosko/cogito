from app.db_models import *
from app.c_helper import *
from flask import current_app as app
import requests
from requests.exceptions import HTTPError


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


def som_admin_konceptov():
    if "logged" in session.keys():
        usr = int(session["logged"])
        ja = User.query.get(usr)
        if ja.je_admin_konceptov == "A":
            return True
        else:
            return False
    else:
        return False


def daj_typ_z_poctov_sd(rows, typ):
    pocet = 0
    for r in rows:
        if r.typ == typ:
            pocet = r.pocet

    return formatuj_cislo(pocet)


def over_captcha(captcha):

    url = f"https://www.google.com/recaptcha/api/siteverify?secret={app.config['RECAPTCHA_PRIVATE_KEY']}" \
        f"&response={captcha}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        json = response.json()

        if json['success']:
            return True

        return False

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
