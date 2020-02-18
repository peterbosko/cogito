from app.morfo.morfo_service import *


def vrat_slovo_slovesa(sd_id, osoba, cislo, cas=None, koncovka=None, rod=None, podrod=None, sposob=None):

    slovo = Slovo.query.filter(Slovo.sd_id == sd_id).filter(Slovo.osoba == osoba).filter(Slovo.cislo == cislo)

    if cas:
        slovo = slovo.filter(Slovo.cas == cas)

    if sposob:
        slovo = slovo.filter(Slovo.sposob == sposob)

    if koncovka:
        slovo = slovo.filter(Slovo.tvar.like("%"+koncovka))

    if rod:
        slovo = slovo.filter(Slovo.rod == rod)

    if podrod:
        slovo = slovo.filter(Slovo.podrod == podrod)

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
            elif slovo_bez_t.endswith("a"):
                if potencionalny_vzor.filter(SDVzor.vzor == "česať").count() > 0:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "česať").first()
                else:
                    vzor = potencionalny_vzor.filter(SDVzor.vzor == "lámať").first()
            elif slovo_bez_t.endswith("ä"):
                vzor = potencionalny_vzor.filter(SDVzor.vzor == "päť").first()
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


def daj_anotaciu_l_tvaru(rod, podrod, cislo, osoba, afirmacia, vid):
    anot_rod = daj_anotaciu_rodu(rod, podrod)

    anot_osoba = daj_anotaciu_osoby(osoba)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_afirm = daj_anotaciu_afirmacie(afirmacia)

    anot_vid = daj_anotaciu_vidu(vid)

    return f"VL{anot_vid}{anot_cislo}{anot_osoba}{anot_rod}{anot_afirm}"


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


def daj_tvar_l_pricastia(vzor_deklinacia, vzor, koren, rod, podrod, cislo, osoba, afirmacia, vid):
    vysledok = []

    upraveny_koren = koren

    if vzor_deklinacia == "o":
        if je_spoluhlaska(koren[-1]) and je_spoluhlaska(koren[-2]):
            upraveny_koren = koren[:-1]

    morfo_res_obj = SlovoFilterExport()
    morfo_res_obj.tvar = f"{upraveny_koren}{vzor_deklinacia}{daj_koncovku_l_tvar(rod, cislo)}"
    morfo_res_obj.rod = rod
    morfo_res_obj.podrod = podrod
    morfo_res_obj.cislo = cislo
    morfo_res_obj.osoba = osoba
    morfo_res_obj.sposob = "O"
    morfo_res_obj.cas = "M"
    morfo_res_obj.anotacia = daj_anotaciu_l_tvaru(rod, podrod, cislo, osoba, afirmacia, vid)

    vysledok.append(morfo_res_obj)

    return vysledok


def daj_koncovku_indikativ(cislo, osoba, deklinacia7):
    if cislo == "J":
        if osoba == "1":
            return "m"
        elif osoba == "2":
            return "š"
        elif osoba == "3":
            return ""
    else:
        if osoba == "1":
            return "me"
        elif osoba == "2":
            return "te"
        elif osoba == "3":
            return deklinacia7


def daj_anotaciu_vidu(vid):
    if vid == "dok":
        return "d"
    elif vid == "nedok":
        return "e"
    elif vid == "opak":
        return "e"
    elif vid == "oboj":
        return "j"
    else:
        return "?"


def daj_anotaciu_indik(cislo, osoba, afirmacia, vid):

    anot_osoba = daj_anotaciu_osoby(osoba)

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_afirm = daj_anotaciu_afirmacie(afirmacia)

    anot_vid = daj_anotaciu_vidu(vid)

    return f"VK{anot_vid}{anot_cislo}{anot_osoba}{anot_afirm}"


def daj_tvar_indikativ(deklinacia5, deklinacia7, vzor, pzkmen, cislo, osoba, afirmacia, vid):
    vysledok = []

    morfo_res_obj = SlovoFilterExport()

    koncovka_indik = daj_koncovku_indikativ(cislo, osoba, deklinacia7)

    if osoba == "3" and cislo == "M":
        deklinacia5 = ""

    tvar = f"{pzkmen}{deklinacia5}{koncovka_indik}"

    morfo_res_obj.tvar = tvar
    morfo_res_obj.rod = ""
    morfo_res_obj.podrod = ""
    morfo_res_obj.cas = "P"
    morfo_res_obj.sposob = "O"
    morfo_res_obj.cislo = cislo
    morfo_res_obj.osoba = osoba
    morfo_res_obj.anotacia = daj_anotaciu_indik(cislo, osoba, afirmacia, vid)

    vysledok.append(morfo_res_obj)

    return vysledok


def generuj_sloveso_ltvar(filter_obj):

    vysledok = []

    l_deklinacia = filter_obj.deklin2

    if filter_obj.rod == "" or filter_obj.rod == "M":
        rod = "M"
        if filter_obj.podrod == "" or filter_obj.podrod == "Z":
            podrod = "Z"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
        if filter_obj.podrod == "" or filter_obj.podrod == "N":
            podrod = "N"
            if filter_obj.cislo == "" or filter_obj.cislo == "J":
                cislo = "J"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.cislo == "" or filter_obj.cislo != "J":
                cislo = "M"
                if filter_obj.osoba == "" or filter_obj.osoba == "1":
                    osoba = "1"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "2":
                    osoba = "2"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
                if filter_obj.osoba == "" or filter_obj.osoba == "3":
                    osoba = "3"
                    vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                         cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    if filter_obj.rod == "" or filter_obj.rod == "Z":
        rod = "Z"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    if filter_obj.rod == "" or filter_obj.rod == "S":
        rod = "S"
        podrod = ""
        if filter_obj.cislo == "" or filter_obj.cislo == "J":
            cislo = "J"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    if filter_obj.rod == "" or filter_obj.rod == "h":
        rod = "h"
        podrod = ""

        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.osoba == "" or filter_obj.osoba == "1":
                osoba = "1"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
            if filter_obj.osoba == "" or filter_obj.osoba == "2":
                osoba = "2"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    if filter_obj.rod == "" or filter_obj.rod == "o":
        rod = "o"
        podrod = ""

        if filter_obj.cislo == "" or filter_obj.cislo != "J":
            cislo = "M"
            if filter_obj.osoba == "" or filter_obj.osoba == "3":
                osoba = "3"
                vysledok.extend(daj_tvar_l_pricastia(l_deklinacia, filter_obj.vzor, filter_obj.koren, rod, podrod,
                                                     cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    return vysledok


def generuj_sloveso_indikativ(filter_obj):

    vysledok = []

    dekl5 = filter_obj.deklin5
    dekl7 = filter_obj.deklin7

    if filter_obj.cislo == "" or filter_obj.cislo == "J":
        cislo = "J"
        if filter_obj.osoba == "" or filter_obj.osoba == "1":
            osoba = "1"
            vysledok.extend(daj_tvar_indikativ(dekl5, dekl7, filter_obj.vzor, filter_obj.pzkmen,
                                               cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
        if filter_obj.osoba == "" or filter_obj.osoba == "2":
            osoba = "2"
            vysledok.extend(daj_tvar_indikativ(dekl5, dekl7, filter_obj.vzor, filter_obj.pzkmen,
                                               cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
        if filter_obj.osoba == "" or filter_obj.osoba == "3":
            osoba = "3"
            vysledok.extend(daj_tvar_indikativ(dekl5, dekl7, filter_obj.vzor, filter_obj.pzkmen,
                                               cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    if filter_obj.cislo == "" or filter_obj.cislo != "J":
        cislo = "M"
        if filter_obj.osoba == "" or filter_obj.osoba == "1":
            osoba = "1"
            vysledok.extend(daj_tvar_indikativ(dekl5, dekl7, filter_obj.vzor, filter_obj.pzkmen,
                                               cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

        if filter_obj.osoba == "" or filter_obj.osoba == "2":
            osoba = "2"
            vysledok.extend(daj_tvar_indikativ(dekl5, dekl7, filter_obj.vzor, filter_obj.pzkmen,
                                               cislo, osoba, filter_obj.afirmacia, filter_obj.vid))
        if filter_obj.osoba == "" or filter_obj.osoba == "3":
            osoba = "3"
            vysledok.extend(daj_tvar_indikativ(dekl5, dekl7, filter_obj.vzor, filter_obj.pzkmen,
                                               cislo, osoba, filter_obj.afirmacia, filter_obj.vid))

    return vysledok


def daj_anotaciu_infinitivu(afirmacia, vid):
    return f"VI{daj_anotaciu_vidu(vid)}{daj_anotaciu_afirmacie(afirmacia)}"


def generuj_sloveso_infinitiv(mfilter, tvar):

    vysledok = []

    morfo_res_obj = SlovoFilterExport()

    morfo_res_obj.tvar = tvar
    morfo_res_obj.rod = ""
    morfo_res_obj.podrod = ""
    morfo_res_obj.cas = ""
    morfo_res_obj.sposob = ""
    morfo_res_obj.cislo = ""
    morfo_res_obj.osoba = ""
    morfo_res_obj.anotacia = daj_anotaciu_infinitivu(mfilter.afirmacia, mfilter.vid)

    vysledok.append(morfo_res_obj)

    return vysledok


def daj_anotaciu_prechodniku(afirmacia, vid):
    return f"VH{daj_anotaciu_vidu(vid)}{daj_anotaciu_afirmacie(afirmacia)}"


def generuj_sloveso_prechodnik(mfilter, tvar):

    vysledok = []

    morfo_res_obj = SlovoFilterExport()

    deklin7 = mfilter.deklin7

    morfo_res_obj.tvar = f"{mfilter.pzkmen}{deklin7}c"
    morfo_res_obj.rod = ""
    morfo_res_obj.podrod = ""
    morfo_res_obj.cas = ""
    morfo_res_obj.sposob = ""
    morfo_res_obj.cislo = ""
    morfo_res_obj.osoba = ""
    morfo_res_obj.anotacia = daj_anotaciu_prechodniku(mfilter.afirmacia, mfilter.vid)

    vysledok.append(morfo_res_obj)

    return vysledok


def daj_koncovku_imperativ(osoba, cislo):
    if cislo == "J" and osoba == "2":
        return ""
    elif cislo != "J" and osoba == "1":
        return "me"
    elif cislo != "J" and osoba == "2":
        return "te"
    else:
        return ""


def daj_anotaciu_immperativu(cislo, osoba, afirmacia, vid):

    anot_cislo = daj_anotaciu_cisla(cislo)

    anot_osoba = daj_anotaciu_osoby(osoba)

    anot_vid = daj_anotaciu_vidu(vid)

    return f"VM{anot_vid}{anot_cislo}{anot_osoba}{daj_anotaciu_afirmacie(afirmacia)}"


def generuj_sloveso_imperativy(mfilter, pzkmen):

    vysledok = []

    # abdikuj
    morfo_res_obj = SlovoFilterExport()
    morfo_res_obj.rod = ""
    morfo_res_obj.podrod = ""
    morfo_res_obj.cas = ""
    morfo_res_obj.sposob = ""
    morfo_res_obj.cislo = "J"
    morfo_res_obj.osoba = "2"
    morfo_res_obj.sposob = "R"
    morfo_res_obj.tvar = f"{pzkmen}{mfilter.deklin6}{daj_koncovku_imperativ(morfo_res_obj.osoba, morfo_res_obj.cislo)}"
    morfo_res_obj.anotacia = daj_anotaciu_immperativu(morfo_res_obj.cislo, morfo_res_obj.osoba, mfilter.afirmacia,
                                                      mfilter.vid)
    vysledok.append(morfo_res_obj)

    # abdikujme
    morfo_res_obj = SlovoFilterExport()
    morfo_res_obj.rod = ""
    morfo_res_obj.podrod = ""
    morfo_res_obj.cas = ""
    morfo_res_obj.sposob = ""
    morfo_res_obj.cislo = "M"
    morfo_res_obj.osoba = "1"
    morfo_res_obj.sposob = "R"
    morfo_res_obj.tvar = f"{pzkmen}{mfilter.deklin6}{daj_koncovku_imperativ(morfo_res_obj.osoba, morfo_res_obj.cislo)}"
    morfo_res_obj.anotacia = daj_anotaciu_immperativu(morfo_res_obj.cislo, morfo_res_obj.osoba, mfilter.afirmacia,
                                                      mfilter.vid)
    vysledok.append(morfo_res_obj)

    # abdikujte
    morfo_res_obj = SlovoFilterExport()
    morfo_res_obj.rod = ""
    morfo_res_obj.podrod = ""
    morfo_res_obj.cas = ""
    morfo_res_obj.sposob = ""
    morfo_res_obj.cislo = "M"
    morfo_res_obj.osoba = "2"
    morfo_res_obj.sposob = "R"
    morfo_res_obj.tvar = f"{pzkmen}{mfilter.deklin6}{daj_koncovku_imperativ(morfo_res_obj.osoba, morfo_res_obj.cislo)}"
    morfo_res_obj.anotacia = daj_anotaciu_immperativu(morfo_res_obj.cislo, morfo_res_obj.osoba, mfilter.afirmacia,
                                                      mfilter.vid)
    vysledok.append(morfo_res_obj)

    return vysledok


def vrat_tvary_pre_sloveso(morfo, sloveso):
    vysledok = []

    vzor = SDVzor.query.filter(SDVzor.typ == "SLOVESO").filter(SDVzor.vzor == morfo.vzor).first()

    morfo.deklin1 = vzor.deklinacia.split(',')[0]
    morfo.deklin2 = vzor.deklinacia.split(',')[1]
    morfo.deklin3 = vzor.deklinacia.split(',')[2]
    morfo.deklin4 = vzor.deklinacia.split(',')[3]
    morfo.deklin5 = vzor.deklinacia.split(',')[4]
    morfo.deklin6 = vzor.deklinacia.split(',')[5]
    morfo.deklin7 = vzor.deklinacia.split(',')[6]

    if morfo.co_generovat == "l" or morfo.co_generovat == "*":
        vysledok.extend(generuj_sloveso_ltvar(morfo))

    if morfo.co_generovat == "i" or morfo.co_generovat == "*":
        vysledok.extend(generuj_sloveso_indikativ(morfo))

    if morfo.co_generovat == "f" or morfo.co_generovat == "*":
        vysledok.extend(generuj_sloveso_infinitiv(morfo, sloveso.zak_tvar))

    if morfo.co_generovat == "p" or morfo.co_generovat == "*":
        vysledok.extend(generuj_sloveso_prechodnik(morfo, morfo.pzkmen))

    if morfo.co_generovat == "!" or morfo.co_generovat == "*":
        vysledok.extend(generuj_sloveso_imperativy(morfo, morfo.pzkmen))

    return vysledok


def odstran_koren_z_t_tvaru(t_tvar, koren):
    len_t = len(t_tvar)

    vysledok = lchop(t_tvar, koren)

    if len_t == len(vysledok):
        pole_znakov_korena = daj_pole_znakov(koren)

        i = 0

        uz_bolo_nahradene = False

        for znak in pole_znakov_korena:
            if znak == "ie" and not uz_bolo_nahradene:
                uz_bolo_nahradene = True
                pole_znakov_korena[i] = "e"

            i += 1

        vysledok = lchop(t_tvar, zretaz_pole_znakov(pole_znakov_korena))

    vysledok = rchop(rchop(vysledok, "ý"), "y")

    return vysledok


def odstran_koren_z_m_tvaru(m_tvar, koren):
    len_m = len(m_tvar)

    vysledok = lchop(m_tvar, koren)

    if len_m == len(vysledok):
        if koren.endswith("br"):
            koren = koren[:-1]+"er"
            vysledok = lchop(m_tvar, koren)

    vysledok = rchop(vysledok, "ší")

    return vysledok


def odstran_koren_z_l_tvaru(l_tvar, koren):
    len_l = len(l_tvar)

    vysledok = lchop(l_tvar, koren)

    if len_l == len(vysledok):
        if l_tvar[-2] == "o" and je_spoluhlaska(koren[-1]) and je_spoluhlaska(koren[-2]):
            koren = koren[:-1]
            vysledok = lchop(l_tvar, koren)

    vysledok = rchop(vysledok, "l")

    return vysledok


def je_dtnl(hlaska):
    if hlaska.lower() == "d" or hlaska.lower() == "t" or hlaska.lower() == "n" or hlaska.lower() == "l":
        return True

    return False


def daj_makku_spoluhlasku_k_spoluhlaske(spoluhlaska):

    je_upper = spoluhlaska == spoluhlaska.upper()

    spoluhlaska = spoluhlaska.lower()

    p = {"d": "ď", "t": "ť", "n": "ň", "l": "ľ"}

    if spoluhlaska in p:
        if je_upper:
            return p[spoluhlaska].upper()
        else:
            return p[spoluhlaska]

    return spoluhlaska


def daj_imperativ_z_pzkmena(imperativ, pzkmen):

    l_imp = len(imperativ)

    vysledok = lchop(imperativ, pzkmen)

    if len(vysledok) == l_imp:
        if je_dtnl(pzkmen[-1]) and daj_makku_spoluhlasku_k_spoluhlaske(pzkmen[-1]) == imperativ[-1]:
            vysledok = "ˇ"
        elif imperativ == pzkmen[:-1]:
            vysledok = "<"

    return vysledok


def daj_koncovku_3os_mc(koncovka, pzkmen):
    k = len(koncovka)

    vysledok = lchop(koncovka, pzkmen)

    if k == len(vysledok):
        pass

    return vysledok

