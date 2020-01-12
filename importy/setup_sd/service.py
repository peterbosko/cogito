from app.db_models import *
from app.app import flask_app
from sqlalchemy import or_
from app.morfo_service import *


db.init_app(flask_app)


def daj_koren(sloveso):
    with flask_app.app_context():
        slovo = Slovo.query.filter(Slovo.sd_id == sloveso.id)

    return ""


def updatuj_slovesa(start):
    with flask_app.app_context():
        # filter(Sloveso.status == "E")
        slovesa = Sloveso.query.filter(Sloveso.id >= start).order_by(Sloveso.id.asc())

        for sloveso in slovesa:
            infinitiv = sloveso.zak_tvar
            print(f"Ide sloveso :{infinitiv} ID:{sloveso.id}")

            jednotne_1os = vrat_slovo_slovesa(sloveso.id, "1", "J", "P", "m")
            mnozne_3os = vrat_slovo_slovesa(sloveso.id, "3", "M", "P")

            chyba = ""
            status = "OK"
            chyba_do_tabulky = ""

            if not infinitiv or not jednotne_1os or not mnozne_3os:
                if not jednotne_1os:
                    chyba_do_tabulky = f"Nenájdená 1os J čísla"
                    chyba = chyba_do_tabulky
                if not mnozne_3os:
                    chyba_do_tabulky = f"Nenájdená 3os M čísla"
                    chyba = chyba_do_tabulky

            if chyba:
                chyba_do_tabulky += chyba
                print(f"Chyba pri spracovávaní slovesa:{infinitiv} chyba:{chyba}")

            if not chyba:
                koren, pzkmen, vzor, prefix, sufix, chyba_do_tabulky = vrat_meta_info_o_slovese(infinitiv, jednotne_1os.tvar,
                                                                                                mnozne_3os.tvar)

            if chyba_do_tabulky:
                sloveso.status = "E"
                sloveso.chyba = chyba_do_tabulky
            else:
                sloveso.status = None
                sloveso.chyba = None
                sloveso.vzor = vzor
                sloveso.koren = koren
                sloveso.pzkmen = pzkmen

            db.session.add(sloveso)
            db.session.commit()


def checkni_vyplnene_slovesa(start):
    with flask_app.app_context():
        slovesa = Sloveso.query.filter(Sloveso.id >= start).filter(or_(Sloveso.vzor.isnot(None), Sloveso.vzor != "")).\
            order_by(Sloveso.id.asc())

        for sloveso in slovesa:
            infinitiv = sloveso.zak_tvar

            print(f"Ide sloveso : {infinitiv}")

            jednotne_1os = vrat_slovo_slovesa(sloveso.id, "1", "J", "P", "m")
            mnozne_3os = vrat_slovo_slovesa(sloveso.id, "3", "M", "P")
            chyba = ""
            status = "OK"
            chyba_do_tabulky = ""

            if not infinitiv or not jednotne_1os or not mnozne_3os:
                if not jednotne_1os:
                    chyba_do_tabulky = f"Nenájdená 1os J čísla"
                    chyba = chyba_do_tabulky
                if not mnozne_3os:
                    chyba_do_tabulky = f"Nenájdená 3os M čísla"
                    chyba = chyba_do_tabulky

            if chyba:
                chyba_do_tabulky += chyba
                print(f"Chyba pri spracovávaní slovesa:{infinitiv} chyba:{chyba}")

            if not chyba:

                koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese(infinitiv, jednotne_1os.tvar,
                                                                                     mnozne_3os.tvar)

                if chyba:
                    chyba_do_tabulky += f"{chyba}"
                    print(f"Chyba pri spracovávaní slovesa:{infinitiv} chyba:{chyba}>|>>>|")

                if koren != sloveso.koren:
                    chyba_do_tabulky += f"R. v koreni > pôvodný:{sloveso.koren} nový:{koren}|>>>|"
                    print(f"Rozdiel v koreni >>> povodny:{sloveso.koren} novy :{koren}")

                if pzkmen != sloveso.pzkmen:
                    chyba_do_tabulky += f"R. v pzkmeni > pôvodný:{sloveso.pzkmen} nový:{pzkmen}|>>>|"
                    print(f"Rozdiel v prezentnom kmeno > povodny:{sloveso.pzkmen} novy:{pzkmen}")

                if vzor != sloveso.vzor:
                    chyba_do_tabulky += f"R. vo vzore > pôvodný:{sloveso.vzor} nový:{vzor}|>>>|"
                    print(f"Rozdiel vo vzore > povodny:{sloveso.vzor} novy :{vzor}")

            if chyba_do_tabulky:
                sloveso.status = "E"
                sloveso.chyba = chyba_do_tabulky
            else:
                sloveso.status = None
                sloveso.chyba = None

            db.session.add(sloveso)
            db.session.commit()
