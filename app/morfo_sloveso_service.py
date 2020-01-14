from app.morfo_service import *


def vrat_slovo_slovesa(sd_id, osoba, cislo, cas="P", koncovka=None):

    slovo = Slovo.query.filter(Slovo.sd_id == sd_id).filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo).\
        filter(Slovo.cas == cas)

    if koncovka:
        slovo = slovo.filter(Slovo.tvar.like("%"+koncovka))

    slovo = slovo.first()

    return slovo


def vrat_kpv_o_slovese(infinitiv, jednotne_1os, mnozne_3os):
    koren = ""
    pzkmen = ""
    vzor = ""
    chyba = ""

    pole_znakov_infinitiv = daj_pole_znakov(infinitiv)

    hlaska_pred_t = pole_znakov_infinitiv[-2]

    slovo_bez_t = zretaz_pole_znakov(pole_znakov_infinitiv[:-1])

    pole_znakov_mnozne_3os = daj_pole_znakov(mnozne_3os)

    koncovka3m = pole_znakov_mnozne_3os[-2]

    if mnozne_3os.endswith("ajú"):
        koncovka3m = "ajú"
    elif mnozne_3os.endswith("ejú"):
        koncovka3m = "ejú"
    elif mnozne_3os.endswith("ia"):
        koncovka3m = "ia"
    elif mnozne_3os.endswith("ú"):
        koncovka3m = "ú"
    elif mnozne_3os.endswith("u"):
        koncovka3m = "u"
    elif mnozne_3os.endswith("a"):
        koncovka3m = "a"

    pole_znakov_jednotne_1os = daj_pole_znakov(jednotne_1os)

    indikativ_bez_koncovky = zretaz_pole_znakov(pole_znakov_jednotne_1os[:-1])

    koncovka_pred_indik = pole_znakov_jednotne_1os[-2]

    potencionalny_vzor = SDVzor.query.filter(SDVzor.typ == "SLOVESO").\
        filter(or_(SDVzor.deklinacia.like(f"{hlaska_pred_t},%,%,%,{koncovka_pred_indik},%,{koncovka3m}"),
                   SDVzor.deklinacia.like(f",%,%,%,{koncovka_pred_indik},%,{koncovka3m}")))

    if potencionalny_vzor.count() == 0 and koncovka3m in ("ejú", "ajú"):
        koncovka3m = "ú"
        potencionalny_vzor = SDVzor.query.filter(SDVzor.typ == "SLOVESO").\
            filter(or_(SDVzor.deklinacia.like(f"{hlaska_pred_t},%,%,%,{koncovka_pred_indik},%,{koncovka3m}"),
                       SDVzor.deklinacia.like(f",%,%,%,{koncovka_pred_indik},%,{koncovka3m}")))

    if potencionalny_vzor.count() > 1:
        if koncovka_pred_indik == "á":
            vzor = potencionalny_vzor.filter(SDVzor.vzor == "chytať").first()
        elif koncovka_pred_indik == "ia":
            vzor = potencionalny_vzor.filter(SDVzor.vzor == "klaňať").first()
        elif koncovka_pred_indik == "a":
            vzor = potencionalny_vzor.filter(SDVzor.vzor == "čítať").first()
        elif koncovka_pred_indik == "i":
            if je_spoluhlaska(pole_znakov_jednotne_1os[-3]) and je_spoluhlaska(pole_znakov_jednotne_1os[-2]):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "krášliť").first()
            elif pole_znakov_jednotne_1os[-3] == "j":
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "bájiť").first()
            else:
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "kúpiť").first()
        elif koncovka_pred_indik == "í":
            if hlaska_pred_t == "i":
                if je_spoluhlaska(pole_znakov_jednotne_1os[-3]) and je_spoluhlaska(pole_znakov_jednotne_1os[-4]):
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "kresliť").first()
                else:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "robiť").first()
            elif hlaska_pred_t == "ie":
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "vidieť").first()
            elif hlaska_pred_t == "a":
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "kričať").first()
        elif koncovka_pred_indik == "ie":
            if hlaska_pred_t == "a":
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "brať").first()
            elif hlaska_pred_t == "ú":
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "hynúť").first()
            elif hlaska_pred_t == "ie":
                if slovo_bez_t.endswith("ie"):
                    if slovo_bez_t.endswith("rie") or potencionalny_vzor.filter(SDVzor.vzor == "rozumieť").count() == 0:
                        vzor = potencionalny_vzor.filter(SDVzor.vzor == "trieť").first()
                    else:
                        vzor = potencionalny_vzor.filter(SDVzor.vzor == "rozumieť").first()
            # sloveso doondiať
            elif hlaska_pred_t == "ia":
                vzor = SDVzor.query.filter(SDVzor.typ == "SLOVESO").filter(SDVzor.vzor == "samovzor").first()
            elif je_spoluhlaska(hlaska_pred_t):
                predkoncovka_pred_indik = ""

                if len(pole_znakov_jednotne_1os) >= 3:
                    predkoncovka_pred_indik = pole_znakov_jednotne_1os[-3]

                if hlaska_pred_t == predkoncovka_pred_indik:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "niesť").first()
                else:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "viesť").first()
        elif indikativ_bez_koncovky.endswith("je"):
            if slovo_bez_t.endswith("ova"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "pracovať").first()
            elif slovo_bez_t.endswith("ia"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "kliať").first()
            elif slovo_bez_t.endswith("a") or slovo_bez_t.endswith("u"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "žuť").first()
            elif slovo_bez_t.endswith("i"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "piť").first()
            elif slovo_bez_t.endswith("pä"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "päť").first()
            elif slovo_bez_t.endswith("y"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "ryť").first()
            elif slovo_bez_t.endswith("ie"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "dospieť").first()
        elif indikativ_bez_koncovky.endswith("e"):
            if slovo_bez_t.endswith("ú"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "chudnúť").first()
            elif slovo_bez_t.endswith("ža"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "žať").first()
            # elif slovo_bez_t.endswith("ja"):
            #    vzor = potencionalny_vzor.filter(SDVzor.vzor == "jať").first()
            elif slovo_bez_t.endswith("u"):
                if potencionalny_vzor.filter(SDVzor.vzor == "vládnuť").count() > 0:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "vládnuť").first()
                else:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "vzlietnuť").first()
            elif slovo_bez_t.endswith("ia"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "predsavziať").first()
            elif slovo_bez_t.endswith("a"):
                if potencionalny_vzor.filter(SDVzor.vzor == "česať").count() > 0:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "česať").first()
                else:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "lámať").first()
            elif slovo_bez_t.endswith("ä"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "päť").first()
            elif infinitiv.endswith("ísť") or infinitiv.endswith("jsť"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "ísť").first()
            elif infinitiv.endswith("chcieť"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "chcieť").first()
    elif potencionalny_vzor.count() == 1:
        vzor = potencionalny_vzor.first()
    else:
        vzor = SDVzor.query.filter(SDVzor.typ == "SLOVESO").filter(SDVzor.vzor == "samovzor").first()

    if not vzor:
        chyba = f"Nenájdený vzor pre infinitív:{infinitiv} J, 1 os:{jednotne_1os} M 3 os:{mnozne_3os}"

    if chyba:
        print(chyba)
        return "", "", "", "", "", chyba

    koren = slovo_bez_t

    koren = rchop(koren, vzor.deklinacia.split(",")[0])

    pzkmen = rchop(mnozne_3os, vzor.deklinacia.split(",")[6])

    return koren, pzkmen, vzor.vzor, chyba


def daj_anotaciu_l_tvaru(rod, podrod, cislo, osoba, afirmacia):
    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_osoba = daj_anotaciu_osoby(osoba)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_afirm = daj_anotaciu_afirmacie(afirmacia)

    return f"VL?{anot_cislo}{anot_osoba}{anot_rod}{anot_afirm}"


def daj_koncovku_l_tvar(rod, cislo):
    if rod == "M":
        if cislo == "J":
            return "l"
        else:
            return "li"
    elif rod == "Z":
        if cislo == "J":
            return "la"
        else:
            return "li"
    elif rod == "S":
        if cislo == "J":
            return "lo"
        else:
            return "li"
    else:
        return "li"


def daj_tvar_l_pricastia(vzor_deklinacia, koren, rod, podrod, cislo, osoba, afirmacia):
    vysledok = []

    upraveny_koren = koren

    if vzor_deklinacia == "o":
        if je_spoluhlaska(koren[-1] and je_spoluhlaska(koren[-2])):
            upraveny_koren = koren[:-1]

    morfo_res_obj = MorfoFilter()
    morfo_res_obj.tvar = f"{upraveny_koren}{vzor_deklinacia}{daj_koncovku_l_tvar(rod, cislo)}"
    morfo_res_obj.rod = rod
    morfo_res_obj.rod = podrod
    morfo_res_obj.rod = cislo
    morfo_res_obj.osoba = osoba
    morfo_res_obj.anotacia = daj_anotaciu_l_tvaru(rod, podrod, cislo, osoba, afirmacia)

    vysledok.append(morfo_res_obj)

    return vysledok


def generuj_sloveso_ltvar(filter_obj, l_deklinacia):

    vysledok = []

    if filter_obj.rod == "" or filter_obj.rod == "M":
        rod = "M"
        if filter_obj.podrod == "" or filter_obj.podrod == "Z":
            podrod = "Z"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))

            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))

                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
        if filter_obj.podrod == "" or filter_obj.podrod == "N":
            podrod = "N"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba))
                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia))

    if filter_obj.rod == "" or filter_obj.rod == "Z":
        rod = "Z"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))

    if filter_obj.rod == "" or filter_obj.rod == "S":
        rod = "S"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia))

    return vysledok

