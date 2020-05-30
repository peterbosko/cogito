from app.app import flask_app
from app.db.user import *
from app.sd_service import *
import sys
from ufal.udpipe import Model
import nltk

db.init_app(flask_app)


def read_udpipe_model():
    print("Loading udpipe model...")
    model = Model.load('udpipe\\data\\slovak-snk-ud-2.5-191206.udpipe')
    print("Downloading nltk punkt...")
    nltk.download('punkt')
    return model


def start(load_pipe):
    debug = False
    host = "0.0.0.0"
    port = 80

    if load_pipe:
        flask_app.udpipe_model = read_udpipe_model()
        if flask_app.udpipe_model:
            print("Model loaded...")
    else:
        print("Not loading pipe...")

    flask_app.run(host, debug=debug, port=port)


def drop_view(view):
    print(f"Dropping view : {view}")
    db.engine.execute(f"DROP VIEW IF EXISTS {view}")


def drop_views():
    drop_view('sem_hier_v')
    drop_view('sd_sloveso_v')


def init_db(app):
    with app.app_context():
        drop_views()

        db.create_all()
        print("Database inicialized")

        usr_bosko = User.query.filter(User.email == "bosko.peter@gmail.com").first()

        if not usr_bosko:
            usr_bosko = User(email="bosko.peter@gmail.com", meno="Peter", priezvisko="Boško", status="V",
                             je_admin="A")
            usr_bosko.nastav_heslo("pbosko")
            db.session.add(usr_bosko)
            db.session.commit()
            print("user bosko was created")

        prepocitaj_sd_stat()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            load_pipe = True

            if len(sys.argv) > 2:
                load_pipe = sys.argv[2] != "nopipe"

            start(load_pipe)
        elif command == "init_db":
            init_db(flask_app)
    else:
        print("usage:\n\n\trun.py [ start | init_db ]")  
