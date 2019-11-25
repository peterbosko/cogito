from app.app import flask_app
from app.db_models import *
import sys

db.init_app(flask_app)


def start():
    debug = False
    host = "0.0.0.0"
    port = 80
    flask_app.run(host, debug=debug, port=port)


def drop_view(view):
    print(f"Dropping view : {view}")
    db.engine.execute(f"DROP VIEW IF EXISTS {view}")


def drop_views():
    drop_view('int_ramec_v')
    drop_view('sem_hier_v')
    drop_view('sem_pad_v')
    drop_view('sd_sloveso_v')
    drop_view('int_slovesa_v')


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

        usr_kacala = User.query.filter(User.email == "kacala.jan@gmail.com").first()

        if not usr_kacala:
            usr_kacala = User(email="kacala.jan@gmail.com", meno="Ján", priezvisko="Kačala", status="V",
                              je_admin="A")
            usr_kacala.nastav_heslo("profkacala")
            db.session.add(usr_kacala)
            db.session.commit()
            print("user Kacala was created")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            start()
        elif command == "init_db":
            init_db(flask_app)
    else:
        print("usage:\n\n\trun.py [ start | init_db ]")  
