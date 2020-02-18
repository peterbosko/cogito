from app.app import flask_app
from app.morfo.morfo_sloveso_service import *
from app.sd_service import *
import datetime
from app.morfo.morfo_prid_m_service import *

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


def zjednot_zamena():
    with flask_app.app_context():
        for z in db.session.query(Zameno.zak_tvar, func.count(Zameno.zak_tvar)). \
                group_by(Zameno.zak_tvar).having(func.count(Zameno.zak_tvar) > 1).all():

            prve_zameno = Zameno.query.filter(Zameno.zak_tvar == z[0]).order_by(Zameno.id).first()

            for rovnake_zameno in Zameno.query.filter(Zameno.zak_tvar == z[0]).filter(Zameno.id != prve_zameno.id):
                for slovo in Slovo.query.filter(Slovo.sd_id == rovnake_zameno.id):
                    print(f"kopirujem slovo:{slovo.tvar}")
                    nove_slovo = Slovo()
                    nove_slovo.tvar = slovo.tvar
                    nove_slovo.rod = slovo.rod
                    nove_slovo.podrod = slovo.podrod
                    nove_slovo.stuper = slovo.stupen
                    nove_slovo.pad = slovo.pad
                    nove_slovo.sposob = slovo.sposob
                    nove_slovo.osoba = slovo.osoba
                    nove_slovo.cas = slovo.cas
                    nove_slovo.pricastie = slovo.pricastie
                    nove_slovo.cislo = slovo.cislo
                    nove_slovo.zvratnost = slovo.zvratnost
                    nove_slovo.anotacia = slovo.anotacia
                    nove_slovo.sd_id = prve_zameno.id

                    db.session.add(nove_slovo)

                chyba = zmaz_cely_s_druh(rovnake_zameno.id)

                print(f"Pokusil som sa zmazat slovny druh id:{rovnake_zameno.id} chyba bola:{chyba}")

                db.session.commit()


def zjednot_cislovky():
    with flask_app.app_context():
        for z in db.session.query(Cislovka.zak_tvar, func.count(Cislovka.zak_tvar)). \
                group_by(Cislovka.zak_tvar).having(func.count(Cislovka.zak_tvar) > 1).all():

            prva_cislovka = Cislovka.query.filter(Cislovka.zak_tvar == z[0]).order_by(Cislovka.id).first()

            for rovnake_cis in Cislovka.query.filter(Cislovka.zak_tvar == z[0]).filter(Cislovka.id != prva_cislovka.id):
                for slovo in Slovo.query.filter(Slovo.sd_id == rovnake_cis.id):
                    print(f"kopirujem slovo:{slovo.tvar}")
                    nove_slovo = Slovo()
                    nove_slovo.tvar = slovo.tvar
                    nove_slovo.rod = slovo.rod
                    nove_slovo.podrod = slovo.podrod
                    nove_slovo.stuper = slovo.stupen
                    nove_slovo.pad = slovo.pad
                    nove_slovo.sposob = slovo.sposob
                    nove_slovo.osoba = slovo.osoba
                    nove_slovo.cas = slovo.cas
                    nove_slovo.pricastie = slovo.pricastie
                    nove_slovo.cislo = slovo.cislo
                    nove_slovo.zvratnost = slovo.zvratnost
                    nove_slovo.anotacia = slovo.anotacia
                    nove_slovo.sd_id = prva_cislovka.id

                    db.session.add(nove_slovo)

                chyba = zmaz_cely_s_druh(rovnake_cis.id)

                print(f"Pokusil som sa zmazat slovny druh id:{rovnake_cis.id} chyba bola:{chyba}")

                db.session.commit()


def anotuj_predlozky():
    with flask_app.app_context():
        for c in Predlozka.query.join(Slovo, Predlozka.id == Slovo.sd_id).filter(Slovo.anotacia.is_(None)):
            print(f"Ide predlozka:{c.zak_tvar}")
            pad = c.pady[0:3]
            print(f"Pad:{pad}")
            for s in c.slova:
                vokaliz = "u"
                if s.tvar[-1] == "o":
                    vokaliz = "v"
                p = daj_anotaciu_padu(pad)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = f"E{vokaliz}{p}"

                db.session.add(slovo)

                db.session.commit()


def anotuj_cislovky():
    with flask_app.app_context():
        for c in Cislovka.query.join(Slovo, Cislovka.id == Slovo.sd_id).filter(Slovo.anotacia.is_(None)):
            print(f"Ide cislovka:{c.zak_tvar}")
            for s in c.slova:
                a = daj_anotaciu_cislovky(c.paradigma, s.rod, s.podrod, s.cislo, s.pad)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = a

                print(f"Nastavil som anotaciu slovu:{slovo.tvar} anotacia:{a}")

                db.session.add(slovo)

                db.session.commit()


def anotuj_zamena():
    with flask_app.app_context():
        for c in Zameno.query.join(Slovo, Zameno.id == Slovo.sd_id).filter(Slovo.anotacia.is_(None)):
            print(f"Ide zameno:{c.zak_tvar}")
            for s in c.slova:
                a = daj_anotaciu_zamena(c.paradigma, s.rod, s.podrod, s.cislo, s.pad)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = a

                print(f"Nastavil som anotaciu slovu:{slovo.tvar} anotacia:{a}")

                db.session.add(slovo)

                db.session.commit()


def anotuj_prislovky():
    with flask_app.app_context():
        for c in Prislovka.query.join(Slovo, Prislovka.id == Slovo.sd_id).filter(Slovo.anotacia.is_(None)):
            print(f"Ide prislovka:{c.zak_tvar}")
            for s in c.slova:
                a = daj_anotaciu_prislovky(s.stupen)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = a

                print(f"Nastavil som anotaciu slovu:{slovo.tvar} anotacia:{a}")

                db.session.add(slovo)

                db.session.commit()


def anotuj_slovesa(start):
    pocet_zaznamov = 0
    with flask_app.app_context():
        for c in Sloveso.query.filter(Sloveso.id >= start).order_by(Sloveso.id).all():
            print(f"Ide sloveso:{c.zak_tvar} Id:{c.id}")
            afirmacia = c.je_negacia == "N"

            for s in Slovo.query.filter(Slovo.sd_id == c.id).filter(or_(Slovo.anotacia.is_(None),
                                                                        Slovo.anotacia == "")):

                a = ""

                if s.tvar.endswith("l") or s.tvar.endswith("la") or s.tvar.endswith("lo") or s.tvar.endswith("li"):
                    a = daj_anotaciu_l_tvaru(s.rod, s.podrod, s.cislo, s.osoba, afirmacia, c.vid)
                elif s.je_neurcitok == "A":
                    a = daj_anotaciu_infinitivu(afirmacia, c.vid)
                elif s.je_prechodnik == "A":
                    a = daj_anotaciu_prechodniku(afirmacia, c.vid)
                elif s.sposob == "R":
                    a = daj_anotaciu_immperativu(s.cislo, s.osoba, afirmacia, c.vid)
                else:
                    a = daj_anotaciu_indik(s.cislo, s.osoba, afirmacia, c.vid)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = a

                slovo.zmenene = datetime.datetime.now()
                slovo.user_id = 1

                print(f"Nastavil som anotaciu slovu:{slovo.tvar} anotacia:{a}")

                db.session.add(slovo)

                pocet_zaznamov += 1

                if pocet_zaznamov >= 500:
                    db.session.commit()
                    pocet_zaznamov = 0

        db.session.commit()


def anotuj_pod_m(start):
    pocet_zaznamov = 0
    with flask_app.app_context():
        for c in PodstatneMeno.query.filter(PodstatneMeno.id >= start).order_by(PodstatneMeno.id).all():
            print(f"Ide pm:{c.zak_tvar} Id:{c.id}")

            for s in Slovo.query.filter(Slovo.sd_id == c.id).filter(or_(Slovo.anotacia.is_(None),
                                                                        Slovo.anotacia == "")):

                a = daj_anotaciu_pm(c.paradigma, s.rod, s.podrod, s.cislo, s.pad)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = a

                slovo.zmenene = datetime.datetime.now()
                slovo.user_id = 1

                print(f"Nastavil som anotaciu slovu:{slovo.tvar} anotacia:{a}")

                db.session.add(slovo)

                pocet_zaznamov += 1

                if pocet_zaznamov >= 500:
                    db.session.commit()
                    pocet_zaznamov = 0

        db.session.commit()


def anotuj_prid_m(start):
    pocet_zaznamov = 0
    with flask_app.app_context():
        for c in PridavneMeno.query.filter(PridavneMeno.id >= start).order_by(PridavneMeno.id).all():
            print(f"Ide pridm:{c.zak_tvar} Id:{c.id}")

            for s in Slovo.query.filter(Slovo.sd_id == c.id).filter(or_(Slovo.anotacia.is_(None),
                                                                        Slovo.anotacia == "")):

                a = daj_anotaciu_prid_m(c.paradigma, s.rod, s.podrod, s.cislo, s.pad, s.stupen, s.pricastie)

                slovo = Slovo.query.get(s.id)

                slovo.anotacia = a

                slovo.zmenene = datetime.datetime.now()
                slovo.user_id = 1

                print(f"Nastavil som anotaciu slovu:{slovo.tvar} anotacia:{a}")

                db.session.add(slovo)

                pocet_zaznamov += 1

                if pocet_zaznamov >= 500:
                    db.session.commit()
                    pocet_zaznamov = 0

        db.session.commit()


def vyhod_duplicitne_slova():
    with flask_app.app_context():
        for s in db.session.query(Slovo.tvar, Slovo.sd_id, Slovo.anotacia, func.min(Slovo.id)).\
                group_by(Slovo.tvar, Slovo.sd_id, Slovo.anotacia).having(func.count(Slovo.tvar) > 1).all():

            if s[2].startswith("VL"):
                print(f"Sloveso L tvar : SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")
                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.sposob = "O"
                osoba = s[2][-3:-2]
                slovo.osoba = daj_osobu_z_anotacie(osoba)
                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)
            elif s[2].startswith("VK"):
                print(f"Sloveso indikativ : SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")
                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.sposob = "O"
                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)
            elif s[2].startswith("S"):
                print(f"Podstatne meno: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")
                sid = s[3]

                s_pomnozne = Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.cislo == "P").first()

                if s_pomnozne:
                    sid = s_pomnozne.id

                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != sid).delete()

                slovo = Slovo.query.get(sid)

                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)

            elif s[2].startswith("VI"):
                print(f"Neurcitok: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)

            elif s[2].startswith("VH") or s[2].startswith("VM"):
                print(f"prechodnik: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)

            elif s[2].startswith("P"):
                print(f"zameno: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)

            elif s[2].startswith("G"):
                print(f"Pricastie: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

                if Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                        filter(Slovo.anotacia == s[2]).filter(Slovo.rod.is_(None)).count() > 0:
                    Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]). \
                        filter(Slovo.anotacia == s[2]).filter(Slovo.rod.is_(None)).delete()
                else:
                    print(f"Pricastie UNKNWN: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")
                    Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                        filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                    slovo = Slovo.query.get(s[3])

                    slovo.user_id = 1
                    slovo.zmenene = datetime.datetime.now()

                    db.session.add(slovo)

            elif s[2].startswith("N"):
                print(f"cislovka: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)

            elif s[2].startswith("A"):
                print(f"prid meno: SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

                Slovo.query.filter(Slovo.sd_id == s[1]).filter(Slovo.tvar == s[0]).\
                    filter(Slovo.anotacia == s[2]).filter(Slovo.id != s[3]).delete()

                slovo = Slovo.query.get(s[3])

                slovo.user_id = 1
                slovo.zmenene = datetime.datetime.now()

                db.session.add(slovo)

            else:
                print(f"NEZNAME : SD_ID:{s[1]} Tvar:{s[0]} Anotacia:{s[2]} Min:{s[3]}")

            db.session.commit()

