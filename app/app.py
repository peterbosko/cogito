from flask import Flask, session
from .m_main import main_blueprint
from .m_kontext import kontext_blueprint
from .m_user import user_blueprint
from .m_chatbot import chatbot_blueprint
from .m_sd import sd_blueprint
from .m_metadata import metadata_blueprint
from flask_fontawesome import FontAwesome
from app.main_helper import *

flask_app = Flask(__name__, static_folder='static', static_url_path='')

fa = FontAwesome(flask_app)

flask_app.secret_key = b'\xa4\x07GU\x9a\x9f\x07\xe3\x7f\xf5v\xbcBx\xcf\xc7\xe0w\xbe\xcd>\xc9\r\x99'
flask_app.config.from_pyfile("..\\config\\config.py")

flask_app.register_blueprint(main_blueprint)
flask_app.register_blueprint(kontext_blueprint)
flask_app.register_blueprint(user_blueprint)
flask_app.register_blueprint(chatbot_blueprint)
flask_app.register_blueprint(sd_blueprint)
flask_app.register_blueprint(metadata_blueprint)

flask_app.jinja_env.globals.update(som_admin=som_admin)
flask_app.jinja_env.globals.update(som_metadata_admin=som_metadata_admin)
flask_app.jinja_env.globals.update(som_admin_slov=som_admin_slov)
flask_app.jinja_env.globals.update(daj_typ_z_poctov_sd=daj_typ_z_poctov_sd)

