from app.db_models import *
from app.app import flask_app
from sqlalchemy import or_
from app.morfo_service import *
from app.morfo_sloveso_service import *
from app.sd_service import *

db.init_app(flask_app)


def updatuj_slovesa(start):
    with flask_app.app_context():
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
                koren, pzkmen, vzor, chyba_do_tabulky = vrat_kpv_o_slovese(infinitiv, jednotne_1os.tvar,
                                                                           mnozne_3os.tvar)

            if chyba_do_tabulky:
                sloveso.status = "E"
                sloveso.chyba = chyba_do_tabulky
            else:
                sloveso.status = "OK"
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

                koren, pzkmen, vzor, chyba = vrat_kpv_o_slovese(infinitiv, jednotne_1os.tvar,
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


def zapis_rozdiel(sl, slovo, status, sd_id):
    slovo_r = SlovoRozdiel()

    slovo_r.tvar = slovo.tvar
    slovo_r.rod = slovo.rod
    slovo_r.podrod = slovo.podrod
    slovo_r.stupen = slovo.stupen
    slovo_r.sposob = slovo.sposob
    slovo_r.osoba = slovo.osoba
    slovo_r.cas = slovo.cas
    slovo_r.pricastie = slovo.pricastie
    slovo_r.cislo = slovo.cislo
    slovo_r.anotacia = slovo.anotacia
    slovo_r.vygen_status = status
    slovo_r.sd_id = sd_id

    if sl:
        slovo_r.sl_id = sl.id

    db.session.add(slovo_r)
    db.session.commit()


def generuj_a_porovnaj_slovesa(start):
    with flask_app.app_context():
        slovesa = Sloveso.query.filter(Sloveso.id >= start).order_by(Sloveso.id.asc())

        for sloveso in slovesa:
            infinitiv = sloveso.zak_tvar

            m = SlovoFilterExport()
            m.co_generovat = "*"
            m.vzor = sloveso.vzor
            m.koren = sloveso.koren
            m.pzkmen = sloveso.pzkmen
            m.afirmacia = sloveso.je_negacia == "N"
            m.vid = sloveso.vid
            m.rod = ""
            m.podrod = ""
            m.cas = ""
            m.stupen = ""
            m.osoba = ""
            m.cislo = ""

            slova = vrat_tvary_pre_sloveso(m, sloveso)

            for slovo in slova:

                print(f"Ide sloveso:{sloveso.id}")

                slovo_v_db = najdi_slovo_z_exportu(sloveso.id, slovo)

                if slovo_v_db:
                    if slovo_v_db.tvar != slovo.tvar:
                        print(f"Slovo najdene, rozdiel v tvare vyg:{slovo.tvar} nájd:{slovo_v_db.tvar}")
                        zapis_rozdiel(slovo_v_db, slovo, "R_T", sloveso.id)
                    elif slovo_v_db.anotacia != slovo.anotacia:
                        print(f"Slovo najdene, rozdiel v anotácii vyg:{slovo.anotacia} nájd:{slovo_v_db.anotacia}")
                        if not slovo_v_db.anotacia:
                            print(f"Opravujem anotaciu v db : slovo:{slovo_v_db.id} na tvar:{slovo.anotacia}")
                            slovo_v_db.anotacia = slovo.anotacia
                            db.session.add(slovo_v_db)
                            db.session.commit()
                        else:
                            print(f"Zapisujem rozdiel v anotacii v db : slovo:{slovo_v_db.id} vyg:{slovo.anotacia} "
                                  f"najd:{slovo_v_db.anotacia}")
                            zapis_rozdiel(slovo_v_db, slovo, "R_A", sloveso.id)
                else:
                    print(f"Chýbajúce slovo v db. tvar:{slovo.tvar}")
                    zapis_rozdiel(None, slovo, "M_S", sloveso.id)


def zisti_vzory_slovies(start):
    with flask_app.app_context():
        slovesa = Sloveso.query.filter(Sloveso.id >= start).order_by(Sloveso.id.asc())

        for sloveso in slovesa:
            infinitiv = sloveso.zak_tvar

            print(f"Ide sloveso:{infinitiv} s id: {sloveso.id}")

            pole_znakov_infinitiv = daj_pole_znakov(infinitiv)

            s_1 = pole_znakov_infinitiv[-2]

            km = zretaz_pole_znakov(pole_znakov_infinitiv[:-2])

            l_tvar = vrat_slovo_slovesa(sloveso.id, "1", "J", "M", "l", "M", "Z")

            s_2 = ""

            if l_tvar:
                s_2 = odstran_koren_z_l_tvaru(l_tvar.tvar, km)

            s_3 = ""

            m_prid_m = daj_pridavne_meno_k_slovesu(sloveso.id, sloveso.je_negacia)

            if m_prid_m:
                m_tvar = vrat_slovo_prid_m(m_prid_m.id, "M", "Z", "J", "Nom", "M")

                if m_tvar:
                    s_3 = odstran_koren_z_m_tvaru(m_tvar.tvar, km)
            else:
                s_3 = "%"

            t_prid_m = daj_pridavne_meno_k_slovesu(sloveso.id, sloveso.je_negacia)

            s_4 = ""

            if t_prid_m:
                t_tvar = vrat_slovo_prid_m(m_prid_m.id, "M", "Z", "J", "Nom", "T")

                if t_tvar:
                    s_4 = odstran_koren_z_t_tvaru(t_tvar.tvar, km)
            else:
                s_4 = "%"

            znak_s1 = daj_pole_znakov(s_1)[0]

            if (len(s_2) > 0 and znak_s1 == daj_pole_znakov(s_2)[0])\
                    and (len(s_3) == 0 or znak_s1 == daj_pole_znakov(s_3)[0]) \
                    and (len(s_4) == 0 or znak_s1 == daj_pole_znakov(s_4)[0]) \
                    and znak_s1 != "a":  # vzor chytať v prípade a
                s_1 = lchop(s_1, znak_s1)
                s_2 = lchop(s_2, znak_s1)
                s_3 = lchop(s_3, znak_s1)
                s_4 = lchop(s_4, znak_s1)
                km = zretaz_pole_znakov(pole_znakov_infinitiv[:-1])

            indikativ = vrat_slovo_slovesa(sloveso.id, "1", "J", "P", "m")

            pzkmen = km

            s_5 = ""

            if indikativ:
                pzkmen = indikativ.tvar

                pzkmen = rchop(indikativ.tvar, "m")

                pole_z_pzkmen = daj_pole_znakov(pzkmen)

                pzkmen = zretaz_pole_znakov(pole_z_pzkmen[:-1])

                s_5 = rchop(indikativ.tvar, "m")

                s_5 = lchop(s_5, pzkmen)

            imperativ = vrat_slovo_slovesa(sloveso.id, "2", "J", None, None, None, None, "R")

            s_6 = ""

            if imperativ:
                s_6 = daj_imperativ_z_pzkmena(imperativ.tvar, pzkmen)

            s_7 = ""

            indik3os_mc = vrat_slovo_slovesa(sloveso.id, "3", "M", "P")

            if indik3os_mc:
                s_7 = daj_koncovku_3os_mc(indik3os_mc.tvar, pzkmen)

            deklin = f"{s_1},{s_2},{s_3},{s_4},{s_5},{s_6},{s_7}"

            vzor = db.session.query(SDVzorTemp).filter(SDVzorTemp.deklinacia.like(deklin)).first()

            deklin = deklin.replace("%", "")

            if vzor:
                sloveso.vzor_temp = vzor.vzor
                db.session.add(sloveso)
                print(f"Sloveso patrí pod vzor:{vzor.vzor}")

            else:
                vt = SDVzorTemp()

                vt.vzor = sloveso.zak_tvar
                vt.deklinacia = deklin
                vt.rod = ""
                vt.typ = "SLOVESO"

                sloveso.vzor_temp = sloveso.zak_tvar

                db.session.add(vt)
                db.session.add(sloveso)

                print(f"Založil som nový vzor:{vt.vzor} deklin:{deklin}")

            db.session.commit()
