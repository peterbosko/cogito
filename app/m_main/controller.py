from flask import Blueprint
from flask import render_template
from flask import request
from app.db_models import Kontext
from app.c_service import *

main_blueprint = Blueprint("main", __name__)


def vitaj():
    loguj(request)

    page = request.args.get("page", 1, type=int)
    paginate = Kontext.query.order_by(Kontext.id.desc()).paginate(page, 4, False)
    return render_template("m_main/uvod.jinja.html", kontexty=paginate.items, paginate=paginate)


@main_blueprint.route("/")
def index():
    loguj(request)
    return vitaj()


@main_blueprint.route("/uvod/")
def uvod():
    loguj(request)
    return vitaj()


@main_blueprint.route("/popis_cogita/")
def popis():
    loguj(request)
    return render_template("m_main/popis_cogita.jinja.html")


@main_blueprint.route("/potrebne_prihlasenie/")
def potrebne_prihlasenie():
    loguj(request)
    return render_template("m_main/potrebne_prihlasenie.jinja.html")
