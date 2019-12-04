from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from app.db_models import *
from app.c_helper import *
from app.c_service import *
from sqlalchemy import and_
import json

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/login/", methods=["GET"])
def login():
    loguj(request)

    if 'logged' in session.keys():
        user = User.query.filter_by(id=session["logged"]).first()
        return render_template("m_user/prihlaseny_user.jinja.html",user=user)
    else:
        return render_template("m_user/login.jinja.html")


@user_blueprint.route("/login/", methods=['POST'])
def prihlas_ma():
    loguj(request)
    email = request.json["email"]
    heslo = request.json["heslo"]

    red = ""
    if request.json["redirect"] != "None":
        red = request.json["redirect"]

    permanent = bool(request.json["permanent"])

    response = CommonResponse()

    user = User.query.filter_by(email=email).first()
    if user and user.skontroluj_heslo(heslo):
        session["logged"] = user.id
        session.permanent = permanent
        response.status = ResponseStatus.OK
        response.redirect = red

    else:
        response.status = ResponseStatus.ERROR
        response.error_text = "Zlé prihlasovacie údaje"

    return json.dumps(response.__dict__)


@user_blueprint.route("/user_pridaj_zmen/", methods=['POST'])
def user_pridaj_zmen():
    loguj(request)
    id = int(request.json["id"])
    meno = request.json["meno"]
    priezvisko = request.json["priezvisko"]
    email = request.json["email"]
    heslo = request.json["heslo"]
    nove_heslo = request.json["nove_heslo"]

    red = ""
    if request.json["redirect"] != "None":
        red = request.json["redirect"]

    response = CommonResponse()

    if nove_heslo and not heslo:
        response.status = ResponseStatus.ERROR
        response.error_text = "Pri zmene hesla musí byť zadané staré heslo"
        return json.dumps(response.__dict__)

    if id == 0:
        if User.query.filter(User.email == email).first():
            response.status = ResponseStatus.ERROR
            response.error_text = "Email už používa iný používateľ"
        else:
            user = User()
            user.meno = meno
            user.priezvisko = priezvisko
            user.email = email
            user.nastav_heslo(heslo)
            user.status = "N"
            db.session.add(user)
            db.session.commit()
            session["logged"] = user.id
            session.permanent = False
            response.status = ResponseStatus.OK
            response.redirect = red
    else:
        user = User.query.get(id)

        if nove_heslo and user.skontroluj_heslo(heslo):
            if User.query.filter(and_(User.email == email, User.id != id)).first():
                response.status = ResponseStatus.ERROR
                response.error_text = "Email už používa iný používateľ"
            else:
                user.meno = meno
                user.priezvisko = priezvisko
                user.email = email
                user.nastav_heslo(nove_heslo)
                db.session.commit()
        elif not nove_heslo:
            if User.query.filter(and_(User.email == email, User.id != id)).first():
                response.status = ResponseStatus.ERROR
                response.error_text = "Email už používa iný používateľ"
            else:
                user.meno = meno
                user.priezvisko = priezvisko
                user.email = email
                db.session.commit()
        else:
            response.status = ResponseStatus.ERROR
            response.error_text = "Zlé staré heslo"

    return json.dumps(response.__dict__)


@user_blueprint.route("/odhlas_ma/", methods=['GET'])
def odhlas_ma():
    loguj(request)

    if session["logged"]:
        session.pop("logged")
    response = CommonResponse()
    return json.dumps(response.__dict__)


@user_blueprint.route("/registracia/", methods=['GET'])
def registracia():
    loguj(request)
    return render_template("m_user/registracia.jinja.html")

