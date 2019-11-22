from flask import Blueprint
from flask import render_template
from flask import request
from app.service import *

chatbot_blueprint = Blueprint("chatbot", __name__)


@chatbot_blueprint.route("/chatbot/", methods=["GET"])
def chatbot():
    return render_template("m_chatbot/chatbot.jinja.html")


@chatbot_blueprint.route("/odpovedz_na_otazku/", methods=["POST"])
def odpovedz_na_otazku():
    otazka = request.json["otazka"]

    kontext = request.json["kontext"]

    response = CommonResponse()

    response.data = cb_odpovedz_na_otazku(otazka, kontext)

    return jsonpickle.encode(response)

