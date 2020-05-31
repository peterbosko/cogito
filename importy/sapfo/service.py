from app.db.slovny_druh import *
from app.app import flask_app
from importy.sapfo.updatuj_service import *
from importy.sapfo.vrat_service import *
import codecs
import pymysql.cursors
import re

I_USER = 'cogito'
I_PASSWORD = 'cogito'
I_HOST = 'localhost'
I_DB_NAME = 'cogito'


db.init_app(flask_app)


def daj_regex_pre(sd):
    if sd == "sub":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s?,\s?(?P<slovo_poradie>\d+)\s?\)\s*,\s*(?P<rodic>.*)sub\s*,\s*cat\s*\(\s*\[?(?P<sem_priznak>(.*?))\]?\s*,\s*('?(?P<prefix>.*?)'?)\s*,\s*('?(?P<sufix>.*?)'?)\s*,\s*'?(?P<vzor>.*?)'?\s*,\s*(?P<poc>.*?)\)(.*?)")
    elif sd == "adj":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s*,\s*(?P<slovo_poradie>\d+)\)\s*,\s*(\(('?(?P<rodic>.*?))'?\s*,\s*(?P<rodic_poradie>\d+?)\)|(?P<rodic_nil>nil))\s*,\s*adj\s*,\s*cat\s*\(\s*\[?(?P<pod_m_kategoria>(.*?))\]?\s*,(?P<prid_m_kategoria>.*?)\s*,\s*'?(?P<prefix>.*?)'?\s*,\s*'?(?P<sufix>.*?)'?\s*,\s*'?(?P<vzor>.*?)'?\s*,\s*'?(?P<pom_tvar>.*?)'?\)(.*?)")
    elif sd == "sl":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s*,\s*(?P<slovo_poradie>\d+)\)\s*,\s*((\('?(?P<rodic>.*?))'?\s*,\s*(?P<rodic_poradie>\d+)\s*\)|nil)\s*,\s*sl\s*,\s*cat\s*\(\s*(?P<intencny_ramec>(\d+)|(.*))\s*,\s*'?(?P<prefix>.*?)'?\s*,\s*'?(?P<sufix>.*?)'?\s*,\s*'?(?P<zvratnost>.*?)'?\s*,\s*'?(?P<vid>.*?)'?\s*,\s*'?(?P<vzor>.*?)'?\s*,\s*'?(?P<vzor2>.*?)'?\s*\)(.*?)")
    elif sd == "adv":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s*,\s*(?P<slovo_poradie>\d+)\)\s*,\s*((\('?(?P<rodic>.*?))'?\s*,\s*(?P<rodic_poradie>\d+)\s*\)|nil)\s*,\s*adv\s*,\s*cat\s*\(\s*(?P<sem_pad>.*?)\s*,\s*'?(?P<prefix>.*?)'?\s*,\s*'?(?P<sufix>.*?)'?\s*,\s*'?(?P<vzor>.*?)'?\s*,\s*'?(?P<koncovka>.*?)'?\s*\)(.*?)")
    elif sd == "cast":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s*,\s*(?P<slovo_poradie>\d+)\)\s*,\s*nil\s*,\s*cast\s*,\s*cat\s*\(\s*(?P<sem_priznak>.*?)\s*,\s*'?(?P<sem_priznak2>.*?)'?\)(.*?)")
    elif sd == "cit":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s*,\s*(?P<slovo_poradie>\d+)\)\s*,\s*nil\s*,\s*cit\s*,\s*cat\s*\(\s*(?P<sem_priznak>.*?)\s*,\s*'?(?P<sem_priznak2>.*?)'?\)(.*?)")
    elif sd == "cis":
        return re.compile(r"(.*?)kmen\(\('?(?P<slovo>(.+?))'?\s*,\s*(?P<slovo_poradie>\d+)\)\s*,\s*((\('?(?P<rodic>(.+?))'?\s*,\s*(?P<rodic_poradie>\d+)\))|nil)\s*,\s*cis\s*,\s*cat\s*\(\s*'?(?P<sem_priznak>.*?)'?\s*,\s*'?(?P<prefix>.*?)'?\s*,\s*'?(?P<sufix>.*?)'?\s*,\s*'?(?P<vzor>.*?)'?\s*,\s*'?(?P<hodnota>.*?)'?\)(.*?)")


def vytvor_slovniky(mode):
    pocet_slov = 0

    pocet_sparovanych_slov = 0

    slovnik_dict = {}

    with open("data\\LEXICON.LEXc", newline='', encoding="utf-8") as sapfo:

        re_sub = daj_regex_pre("sub")
        re_adj = daj_regex_pre("adj")
        re_sl = daj_regex_pre("sl")
        re_cast = daj_regex_pre("cast")
        re_adv = daj_regex_pre("adv")
        re_cit = daj_regex_pre("cit")
        re_cis = daj_regex_pre("cis")

        for s in sapfo:
            m_sub = re.match(re_sub, s)
            m_adj = re.match(re_adj, s)
            m_sl = re.match(re_sl, s)
            m_adv = re.match(re_adv, s)
            m_cast = re.match(re_cast, s)
            m_cit = re.match(re_cit, s)
            m_cis = re.match(re_cis, s)

            was_processed = "unknown"
            was_matched = "unknown"

            if m_sub:
                was_matched = "sub"
                if mode == "sub" or mode == "all":
                    pocet_slov += 1
                    re_rodic = re.compile(r"(\('?(?P<rodic_slovo>.*?)'?\s*,\s*(?P<rodic_slovo_poradie>\d+?))|(?P<rodic_slovo_nil>nil)")

                    m_rodic = re.match(re_rodic, m_sub.group('rodic'))

                    print(f"Substantivum ==> Slovo:{m_sub.group('slovo')} Slovo poradie:{m_sub.group('slovo_poradie')} Sem priznak:{m_sub.group('sem_priznak')} Vzor:{m_sub.group('vzor')} Poc:{m_sub.group('poc')}")

                    slovo_id, select = vrat_pod_m(m_sub.group('slovo'), m_sub.group('sufix'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["sub_"+m_sub.group('slovo')+"_"+m_sub.group('slovo_poradie')] = s+":"+str(slovo_id)+":"+select

                    was_processed = "sub"

            if m_adj:
                was_matched = "adj"
                if mode == "adj" or mode == "all":
                    pocet_slov += 1
                    print(f"Adjektivum ==> Slovo:{m_adj.group('slovo')} Slovo poradie:{m_adj.group('slovo_poradie')} Rodic:{m_adj.group('rodic')} Rodic poradie:{m_adj.group('rodic_poradie')} Kategoria POD_M:{m_adj.group('pod_m_kategoria')} Vzor:{m_adj.group('vzor')} PomTvar:{m_adj.group('pom_tvar')} typ adjektiva:{m_adj.group('prid_m_kategoria')}")

                    slovo_id, select = vrat_prid_m(m_adj.group('slovo'), m_adj.group('sufix'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["adj_"+m_adj.group('slovo')+"_"+m_adj.group('slovo_poradie')] = s+":"+str(slovo_id)+":"+select

                    was_processed = "adj"

            if m_sl:
                was_matched = "sl"
                if mode == "sl" or mode == "all":
                    print(f"Sloveso ==> Slovo:{m_sl.group('slovo')} SlovoPoradie:{m_sl.group('slovo_poradie')} Rodic:{m_sl.group('rodic')}  Rodic poradie:{m_sl.group('rodic_poradie')} "
                          f"Intencny ramec:{m_sl.group('intencny_ramec')} Vzor:{m_sl.group('vzor')} Vzor2:{m_sl.group('vzor2')} zvratnost:{m_sl.group('zvratnost')} vid:{m_sl.group('vid')} Prefix:{m_sl.group('prefix')} Sufix:{m_sl.group('sufix')}")

                    pocet_slov += 1

                    slovo_id, select = vrat_sloveso(m_sl.group('slovo'), m_sl.group('sufix'), m_sl.group('zvratnost'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["slo_"+m_sl.group('slovo')+"_"+m_sl.group('slovo_poradie')] = s+":"+str(slovo_id)+":"+select

                    was_processed = "sl"

            if m_adv:
                was_matched = "adv"
                if mode == "adv" or mode == "all":
                    pocet_slov += 1
                    print(f"Adverbium ==> Slovo:{m_adv.group('slovo')} Slovo poradie:{m_adv.group('slovo_poradie')} "
                          f"Rodic:{m_adv.group('rodic')}  Rodic poradie:{m_adv.group('rodic_poradie')} "
                          f"SP:{m_adv.group('sem_pad')} Vzor:{m_adv.group('vzor')} koncovka:{m_adv.group('koncovka')} "
                          f"Prefix:{m_adv.group('prefix')} sufix:{m_adv.group('sufix')}")

                    slovo_id, select = vrat_prislovku(m_adv.group('slovo'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["adv_"+m_adv.group('slovo')+"_"+m_adv.group('slovo_poradie')] = s+":"+str(slovo_id)\
                        + ":"+select

                    was_processed = "adv"

            if m_cast:
                was_matched = "cast"
                if mode == "cast" or mode == "all":
                    pocet_slov += 1
                    print(f"Castica ==> Slovo:{m_cast.group('slovo')}  sem priznak:{m_cast.group('sem_priznak')} "
                          f":sem priznak2:{m_cast.group('sem_priznak2')}")
                    slovo_id, select = vrat_casticu(m_cast.group('slovo'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["cas_"+m_cast.group('slovo')+"_"+m_cast.group('slovo_poradie')] = s+":"+str(slovo_id)\
                        + ":"+select
                    was_processed = "cast"

            if m_cit:
                was_matched = "cit"
                if mode == "cit" or mode == "all":
                    pocet_slov += 1
                    print(f"Citoslovce ==> Slovo:{m_cit.group('slovo')}  Kategorie:{m_cit.group('sem_priznak')} "
                          f"sem priznak 2:{m_cit.group('sem_priznak2')}")

                    slovo_id, select = vrat_citoslovce(m_cit.group('slovo'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["cit_"+m_cit.group('slovo')+"_"+m_cit.group('slovo_poradie')] = s+":"+str(slovo_id)\
                        + ":"+select

                    was_processed = "cit"

            if m_cis:
                was_matched = "cis"
                if mode == "cis" or mode == "all":
                    pocet_slov += 1
                    print(f"Cislovka ==> Slovo:{m_cis.group('slovo')}  Slovo poradie:{m_cis.group('slovo_poradie')}  "
                          f"Kategorie:{m_cis.group('sem_priznak')} vzor:{m_cis.group('vzor')} "
                          f"prefix:{m_cis.group('prefix')} sufix:{m_cis.group('sufix')} "
                          f"hodnota:{m_cis.group('hodnota')}")

                    slovo_id, select = vrat_cislovku(m_cis.group('slovo'))

                    if slovo_id:
                        select = ""
                        pocet_sparovanych_slov += 1

                    slovnik_dict["cis_"+m_cis.group('slovo')+"_"+m_cis.group('slovo_poradie')] = s+":"+str(slovo_id)\
                        + ":"+select
                    was_processed = "cis"

            if s[0:4] != "list" and was_matched == "unknown":
                print("*******    NOT IMPLEMENTED:     *********")
                print(s)

            if s[0:4] == "eof.":
                break

    with codecs.open("data\\sub_slovnik_s_idckami.txt", "w", "utf-8-sig") as fsub:
        with codecs.open("data\\adj_slovnik_s_idckami.txt", "w", "utf-8-sig") as fadj:
            with codecs.open("data\\slo_slovnik_s_idckami.txt", "w", "utf-8-sig") as fsl:
                with codecs.open("data\\adv_slovnik_s_idckami.txt", "w", "utf-8-sig") as fadv:
                    with codecs.open("data\\cis_slovnik_s_idckami.txt", "w", "utf-8-sig") as fcis:
                        with codecs.open("data\\cit_slovnik_s_idckami.txt", "w", "utf-8-sig") as fcit:
                            with codecs.open("data\\cas_slovnik_s_idckami.txt", "w", "utf-8-sig") as fcas:
                                for slov in slovnik_dict:
                                    if slov[0:3] == "sub":
                                        fsub.write(slov+">"+slovnik_dict[slov].replace("\n", "").replace("\r", "")+"\n")
                                    elif slov[0:3] == "adj":
                                        fadj.write(slov + ">" + slovnik_dict[slov].replace("\n", "").replace("\r", "") + "\n")
                                    elif slov[0:3] == "slo":
                                        fsl.write(slov + ">" + slovnik_dict[slov].replace("\n", "").replace("\r", "") + "\n")
                                    elif slov[0:3] == "adv":
                                        fadv.write(slov + ">" + slovnik_dict[slov].replace("\n", "").replace("\r", "") + "\n")
                                    elif slov[0:3] == "cis":
                                        fcis.write(slov + ">" + slovnik_dict[slov].replace("\n", "").replace("\r", "") + "\n")
                                    elif slov[0:3] == "cit":
                                        fcit.write(slov + ">" + slovnik_dict[slov].replace("\n", "").replace("\r", "") + "\n")
                                    elif slov[0:3] == "cas":
                                        fcas.write(slov + ">" + slovnik_dict[slov].replace("\n", "").replace("\r", "") + "\n")

    return pocet_slov, pocet_sparovanych_slov


def nacitaj_subor(subor):
    dic = {}
    with open(subor, newline='', encoding="utf-8") as sapfo:
        for s in sapfo:
            key = s[4:s.index('>')]
            dic[key] = s

    return dic


def daj_id_z_riadku(s):
    ret = None
    if s[s.index(':')+1 : s.index(':', s.index(':')+1)] != "None":
        ret = int(s[s.index(':')+1: s.index(':', s.index(':')+1)])

    return ret


def daj_id_zo_slovnika(slovnik, slovo, slovo_poradie):

    if slovo+'_'+str(slovo_poradie) in slovnik:
        return daj_id_z_riadku(slovnik[slovo+'_'+str(slovo_poradie)])
    else:
        return -1


def daj_koren_z_d(dict_key):
    if dict_key[0] == "_":
        dict_key = dict_key[1:]

    res = dict_key[0:dict_key.index("_", 1)]
    return res


def spracuj_slovniky(mode):

    dic = {}

    dic.update(nacitaj_subor("data\\sub_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\adj_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\slo_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\adv_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\cis_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\cit_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\cas_slovnik_s_idckami.txt"))

    for d in dic.keys():
        s = dic[d]

        re_sub = daj_regex_pre("sub")
        re_adj = daj_regex_pre("adj")
        re_sl = daj_regex_pre("sl")
        re_cast = daj_regex_pre("cast")
        re_adv = daj_regex_pre("adv")
        re_cit = daj_regex_pre("cit")
        re_cis = daj_regex_pre("cis")

        m_sub = re.match(re_sub, s)
        m_adj = re.match(re_adj, s)
        m_sl = re.match(re_sl, s)
        m_adv = re.match(re_adv, s)
        m_cast = re.match(re_cast, s)
        m_cit = re.match(re_cit, s)
        m_cis = re.match(re_cis, s)

        if m_sub:
            if mode == "sub" or mode == "all":
                re_rodic = re.compile(
                    r"(\('?(?P<rodic_slovo>.*?)'?\s*,\s*(?P<rodic_slovo_poradie>\d+?))|(?P<rodic_slovo_nil>nil)")
                m_rodic = re.match(re_rodic, m_sub.group('rodic'))
                print(f"Substantivum ==> Slovo:{m_sub.group('slovo')} "
                      f"sem priznak:{m_sub.group('sem_priznak')} Vzor:{m_sub.group('vzor')} Poc:{m_sub.group('poc')}")
                slovo_id = daj_id_z_riadku(s)

                if slovo_id:
                    rodic_id = None

                    if m_rodic.group('rodic_slovo'):
                        rodic_id = daj_id_zo_slovnika(dic, m_rodic.group('rodic_slovo'),
                                                      m_rodic.group('rodic_slovo_poradie'))

                        if rodic_id == -1:
                            print(f"!!!!!!!!!!!!!!!!! Rodic nebol najdeny v dictionary:{m_rodic.group('rodic_slovo')} "
                                  f"{m_rodic.group('rodic_slovo_poradie')}")

                        if rodic_id is None:
                            print(f"!!!!!!!!!!!!!!!!! Treba pridat slovo:{m_rodic.group('rodic_slovo')} "
                                  f"{m_rodic.group('rodic_slovo_poradie')}")

                    updatuj_pod_m(daj_koren_z_d(d), slovo_id, rodic_id, m_sub.group('sem_priznak'), m_sub.group('prefix'),
                                  m_sub.group('sufix'), m_sub.group('vzor'), m_sub.group('poc'))

                    # dve slova v rodicoch
                    if m_sub.group('rodic') and '((' in m_sub.group('rodic'):
                        re_2rodic = re.compile(
                            r"\(\('?(?P<rodic_slovo>.*?)'?\s*,\s*(?P<rodic_slovo_poradie>\d+)\)\s*,\s*'?(?P<rodic2_slovo>.*?)'?\s*,\s*(?P<rodic2_slovo_poradie>\d+)\)")

                        m_2rodic = re.match(re_2rodic, m_sub.group('rodic'))

                        r1 = daj_id_zo_slovnika(dic, m_2rodic.group('rodic_slovo'), m_2rodic.group('rodic_slovo_poradie'))

                        if r1 and r1 > 0:
                            zaloz_hierarchiu_sd(slovo_id, r1)

                        r2 = daj_id_zo_slovnika(dic, m_2rodic.group('rodic2_slovo'), m_2rodic.group('rodic2_slovo_poradie'))

                        if r2 and r2 > 0:
                            zaloz_hierarchiu_sd(slovo_id, r2)

                        print(f"R:{m_2rodic.group('rodic_slovo')}:R")
                        print(f"P:{m_2rodic.group('rodic_slovo_poradie')}:P")
                        print(f"R2:{m_2rodic.group('rodic2_slovo')}:R2")
                        print(f"P2:{m_2rodic.group('rodic2_slovo_poradie')}:P2")
                        print("koniec")

        if m_adj:
            if mode == "adj" or mode == "all":
                print(f"Adjektivum ==> Slovo:{m_adj.group('slovo')} "
                      f"Slovo poradie:{m_adj.group('slovo_poradie')} Rodic:{m_adj.group('rodic')} "
                      f"Rodic poradie:{m_adj.group('rodic_poradie')} Kategoria "
                      f"POD_M:{m_adj.group('pod_m_kategoria')} Vzor:{m_adj.group('vzor')} "
                      f"PomTvar:{m_adj.group('pom_tvar')} typ adjektiva:{m_adj.group('prid_m_kategoria')}")
                slovo_id = daj_id_z_riadku(s)

                if slovo_id:
                    rodic_id = None

                    if m_adj.group('rodic'):

                        rodic_id = daj_id_zo_slovnika(dic, m_adj.group('rodic'),
                                                      m_adj.group('rodic_poradie'))

                        if rodic_id == -1:
                            print(f"!!!!!!!!!!!!!!!!! Rodic nebol najdeny v dictionary:{m_adj.group('rodic')} " +
                                  f"{m_adj.group('rodic_poradie')}")

                        if rodic_id is None:
                            print(f"!!!!!!!!!!!!!!!!! Treba pridat slovo:{m_adj.group('rodic')} " +
                                  f"poradie: {m_adj.group('rodic_poradie')}")

                    v2 = None

                    if m_adj.group('pom_tvar') and m_adj.group('pom_tvar') != "nil":
                        v2 = m_adj.group('pom_tvar')

                    updatuj_prid_m(daj_koren_z_d(d), slovo_id, rodic_id, m_adj.group('pod_m_kategoria'), m_adj.group('prefix'),
                                   m_adj.group('sufix'), m_adj.group('vzor'), m_adj.group('prid_m_kategoria'), v2)

                    # dve slova v rodicoch
                    if m_adj.group('rodic') and '(' in m_adj.group('rodic'):
                        re_2rodic = re.compile(
                            r"\('?(?P<rodic_slovo>.*?)'?\s*,\s*(?P<rodic_slovo_poradie>\d+)\)\s*,\s*'?(?P<rodic2_slovo>.*)")

                        m_2rodic = re.match(re_2rodic, m_adj.group('rodic'))

                        print(f"R:{m_2rodic.group('rodic_slovo')}:R")
                        print(f"P:{m_2rodic.group('rodic_slovo_poradie')}:P")
                        print(f"R2:{m_2rodic.group('rodic2_slovo')}:R2")
                        print(f"P2:{m_adj.group('rodic_poradie')}:P2")

                        r1 = daj_id_zo_slovnika(dic, m_2rodic.group('rodic_slovo'), m_2rodic.group('rodic_slovo_poradie'))

                        if r1 and r1 > 0:
                            zaloz_hierarchiu_sd(slovo_id, r1)

                        r2 = daj_id_zo_slovnika(dic, m_2rodic.group('rodic2_slovo'), m_adj.group('rodic_poradie'))

                        if r2 and r2 > 0:
                            zaloz_hierarchiu_sd(slovo_id, r2)

                        print("koniec")


        if m_sl:
            if mode == "sl" or mode == "all":
                print(f"Sloveso ==> Slovo:{m_sl.group('slovo')} SlovoPoradie:{m_sl.group('slovo_poradie')} "
                      f"Rodic:{m_sl.group('rodic')}  Rodic poradie:{m_sl.group('rodic_poradie')} "
                      f"Intencny ramec:{m_sl.group('intencny_ramec')} Vzor:{m_sl.group('vzor')} "
                      f"Vzor2:{m_sl.group('vzor2')} zvratnost:{m_sl.group('zvratnost')} "
                      f"vid:{m_sl.group('vid')} Prefix:{m_sl.group('prefix')} Sufix:{m_sl.group('sufix')}")

                slovo_id = daj_id_z_riadku(s)

                if slovo_id:
                    rodic_id = None

                    if m_sl.group('rodic'):
                        rodic_id = daj_id_zo_slovnika(dic, m_sl.group('rodic'),
                                                      m_sl.group('rodic_poradie'))

                        if rodic_id == -1:
                            print(f"!!!!!!!!!!!!!!!!! Rodic nebol najdeny v dictionary:{m_sl.group('rodic')} " +
                                  f"{m_sl.group('rodic_poradie')}")

                        if rodic_id is None:
                            print(f"!!!!!!!!!!!!!!!!! Treba pridat slovo:{m_sl.group('rodic')} " +
                                  f"poradie: {m_sl.group('rodic_poradie')}")

                    updatuj_sl(daj_koren_z_d(d),slovo_id, rodic_id, m_sl.group('intencny_ramec'), m_sl.group('prefix'),
                               m_sl.group('sufix'), m_sl.group('vzor'), m_sl.group('vid'),
                               m_sl.group('vzor2'))

        if m_adv:
            if mode == "adv" or mode == "all":
                print(f"Adverbium ==> Slovo:{m_adv.group('slovo')} Slovo poradie:{m_adv.group('slovo_poradie')} "
                      f"Rodic:{m_adv.group('rodic')}  Rodic poradie:{m_adv.group('rodic_poradie')} "
                      f"SP:{m_adv.group('sem_pad')} Vzor:{m_adv.group('vzor')} koncovka:{m_adv.group('koncovka')} "
                      f"Prefix:{m_adv.group('prefix')} sufix:{m_adv.group('sufix')}")

                slovo_id = daj_id_z_riadku(s)

                if slovo_id:
                    rodic_id = None

                    if m_adv.group('rodic'):
                        rodic_id = daj_id_zo_slovnika(dic, m_adv.group('rodic'),
                                                      m_adv.group('rodic_poradie'))

                        if rodic_id == -1:
                            print(f"!!!!!!!!!!!!!!!!! Rodic nebol najdeny v dictionary:{m_adv.group('rodic')} " +
                                  f"{m_adv.group('rodic_poradie')}")

                        if rodic_id is None:
                            print(f"!!!!!!!!!!!!!!!!! Treba pridat slovo:{m_adv.group('rodic')} " +
                                  f"poradie: {m_adv.group('rodic_poradie')}")

                    updatuj_prislovku(daj_koren_z_d(d), slovo_id, rodic_id, m_adv.group('sem_pad'), m_adv.group('vzor'),
                                      m_adv.group('prefix'), m_adv.group('sufix'), m_adv.group('koncovka'))

        if m_cast:
            if mode == "cast" or mode == "all":
                print(f"Castica ==> Slovo:{m_cast.group('slovo')}  sem priznak:{m_cast.group('sem_priznak')} "
                      f":sem priznak2:{m_cast.group('sem_priznak2')}")

        if m_cit:
            if mode == "cit" or mode == "all":
                print(f"Citoslovce ==> Slovo:{m_cit.group('slovo')}  Kategorie:{m_cit.group('sem_priznak')} "
                      f"sem priznak 2:{m_cit.group('sem_priznak2')}")

        if m_cis:
            if mode == "cis" or mode == "all":
                print(f"Cislovka ==> Slovo:{m_cis.group('slovo')}  Slovo poradie:{m_cis.group('slovo_poradie')}  "
                      f"Kategorie:{m_cis.group('sem_priznak')} vzor:{m_cis.group('vzor')} "
                      f"prefix:{m_cis.group('prefix')} sufix:{m_cis.group('sufix')} "
                      f"hodnota:{m_cis.group('hodnota')}")

                slovo_id = daj_id_z_riadku(s)

                if slovo_id:
                    rodic_id = None

                    if m_cis.group('rodic'):
                        rodic_id = daj_id_zo_slovnika(dic, m_cis.group('rodic'),
                                                      m_cis.group('rodic_poradie'))

                        if rodic_id == -1:
                            print(f"!!!!!!!!!!!!!!!!! Rodic nebol najdeny v dictionary:{m_cis.group('rodic')} " +
                                  f"{m_cis.group('rodic_poradie')}")

                        if rodic_id is None:
                            print(f"!!!!!!!!!!!!!!!!! Treba pridat slovo:{m_cis.group('rodic')} " +
                                  f"poradie: {m_cis.group('rodic_poradie')}")

                    v = None

                    if m_cis.group('vzor') and m_cis.group('vzor') != "nil":
                        v = m_cis.group('vzor')

                    updatuj_cislovku(daj_koren_z_d(d), slovo_id, rodic_id, m_cis.group('sem_priznak'), v,
                                     m_cis.group('prefix'), m_cis.group('sufix'), m_cis.group('hodnota'))

        print(s)

    return 0


def daj_sem(sem):
    s_connection = pymysql.connect(host=I_HOST,
                                   user=I_USER,
                                   password=I_PASSWORD,
                                   db=I_DB_NAME,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
    try:
        with s_connection.cursor() as cursor:
            sql = f"SELECT id FROM sem WHERE kod='{sem}'"
            cursor.execute(sql)
            for row in cursor:
                return int(row['id'])
    finally:
        s_connection.close()


def daj_int_ramec(ramec):
    s_connection = pymysql.connect(host=I_HOST,
                                   user=I_USER,
                                   password=I_PASSWORD,
                                   db=I_DB_NAME,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
    try:
        with s_connection.cursor() as cursor:

            sql = f"SELECT id FROM int_ramec WHERE kod='{ramec}'"
            cursor.execute(sql)
            for row in cursor:
                return int(row['id'])
    finally:
        s_connection.close()


def daj_sem_pad(sp, o):
    s_connection = pymysql.connect(host=I_HOST,
                                   user=I_USER,
                                   password=I_PASSWORD,
                                   db=I_DB_NAME,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
    try:
        with s_connection.cursor() as cursor:

            sem_p2 = sp

            if o > 0:
                sem_p2 = sem_p2 + "_" + str(o)

            sql = f"SELECT id FROM sem_pad WHERE kod='{sem_p2}'"
            cursor.execute(sql)
            for row in cursor:
                return int(row['id'])
    finally:
        s_connection.close()


def vloz_intenciu(i, predlozka, pad, sem, sp, sp_o, fl):
    i_connection = pymysql.connect(host=I_HOST,
                                   user=I_USER,
                                   password=I_PASSWORD,
                                   db=I_DB_NAME,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
    try:
        with i_connection.cursor() as cursor:
            sql = "INSERT INTO `cogito`.`int`(`typ`,`int_ramec_id`,`predlozka`,`pad`,`sem`,`sem_pad`,`fl`)" \
                  "VALUES(%s,%s,%s,%s,%s,%s,%s);"

            predlozka2 = None
            if predlozka != "0":
                predlozka2 = predlozka

            pad2 = "Nom"

            if 'nom' in pad:
                pad2 = 'Nom'
            elif 'gen' in pad:
                pad2 = 'Gen'
            elif 'dat' in pad:
                pad2 = 'Dat'
            elif 'ak' in pad:
                pad2 = 'Aku'
            elif 'vok' in pad:
                pad2 = 'Vok'
            elif 'lok' in pad:
                pad2 = 'Lok'
            elif 'ins' in pad:
                pad2 = 'Ins'

            sem2 = None
            if sem != "":
                sem2 = daj_sem(sem)

            sem_pad2 = daj_sem_pad(sp, sp_o)

            ir = daj_int_ramec(i)

            cursor.execute(sql, ("int1", ir, predlozka2, pad2, sem2, sem_pad2, fl))
            i_connection.commit()
    finally:
        i_connection.close()


def importuj_sapfo_intenciu():
    pocet_intencii = 0
    with open("data\\LEXICON.LEXc", newline='', encoding="utf-8") as sapfo:
        re_int = re.compile(r"int\((?P<intencia>\d+?),\'?(?P<predlozka>.*?)\'?,(?P<pad>.*?),\[(?P<sem>.*?)\],\((?P<sp>.*?)\s?,\s?(?P<sp_ord>\d+?)\),(?P<fl>\d+?)\)")
        for s in sapfo:
            if s[0:3] == "int":
                m_int = re.match(re_int, s)
                print(f"intencia ==> Kod:{m_int.group('intencia')} predlozka:{m_int.group('predlozka')} " +
                      f"Pad:{m_int.group('pad')} Sem:{m_int.group('sem')} SP:{m_int.group('sp')} " +
                      f"O:{m_int.group('sp_ord')} fl:{m_int.group('fl')}")
                vloz_intenciu(int(m_int.group('intencia')), m_int.group('predlozka'), m_int.group('pad'),
                              m_int.group('sem'), m_int.group('sp'), int(m_int.group('sp_ord')), m_int.group('fl'))
                pocet_intencii += 1
    return pocet_intencii


def spracuj_pzkmene():
    dic = {}

    dic.update(nacitaj_subor("data\\sub_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\adj_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\slo_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\adv_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\cis_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\cit_slovnik_s_idckami.txt"))
    dic.update(nacitaj_subor("data\\cas_slovnik_s_idckami.txt"))

    with flask_app.app_context():

        with open("data\\LEXICON.LEXc", newline='', encoding="utf-8") as sapfo:
            re_kmen = re.compile(r"pzkmen\(\s*'?(?P<kmen>.*?)'?\s*,\s*\('?(?P<rodic_1>.*?)'?\s*,\s*(?P<rodic_1_poradie>\d+)\s*\)\s*,\s*((\('?(?P<rodic_2>.*?)'?\s*,\s*(?P<rodic_2_poradie>\d+)\s*\))|nil)")

               # r"pzkmen\(\s*'?(?P<kmen>.*?)'?\s*,\s*\('?(?P<rodic_1>.*?)'?\s*,\s*(?P<rodic_1_poradie>\d+)\s*\)\s*,\s*(\((\s*\'?(?P<rodic_2>(.*?))'\s*,\s*(?P<rodic_2_poradie>\d+))|nil)")
            for s in sapfo:
                if s[0:6] == "pzkmen":
                    m_s = re.match(re_kmen, s)

                    if not m_s:
                        print("Chyba pri parsovani:"+s)
                        break

                    slovesa = vrat_slovesa_podla_pzkmena(m_s.group('kmen'))

                    for sloveso in slovesa:

                        ids = daj_id_zo_slovnika(dic, m_s.group('rodic_1'), m_s.group('rodic_1_poradie'))

                        if ids:
                            rodic_slovo = Sloveso.query.get(ids)
                            if rodic_slovo:
                                print(f"Zakladam hierachiu pre slovo:{sloveso.zak_tvar} Parent:{rodic_slovo.zak_tvar}")

                                if sloveso.id != ids:
                                    zaloz_hierarchiu_sd(sloveso.id, ids)

                        if m_s.group('rodic_2'):
                            ids2 = daj_id_zo_slovnika(dic, m_s.group('rodic_2'), m_s.group('rodic_2_poradie'))

                            if ids2:
                                rodic2_slovo = Sloveso.query.get(ids2)

                                if rodic2_slovo:
                                    print(
                                        f"Zakladam druhu hierachiu pre slovo:{sloveso.zak_tvar} Parent:{rodic2_slovo.zak_tvar}")
                                    if sloveso.id != ids2:
                                        zaloz_hierarchiu_sd(sloveso.id, ids2)


def spracuj_vzory():
    postfix_dict = {}
    alternacie_vzorov = {}
    with open("data\\POD_M_vzory.txt", newline='', encoding="utf-8") as subor:
        re_pf = re.compile(r"postfix\('?(?P<postfix>.*?)'?,(?P<koncovky>.*?)\)")
        re_vzor = re.compile(r"vzorsub\('?(?P<vzor>.*?)'?,(?P<rod>.*?),'?(?P<postfix>.*?)'?\)")
        re_alt = re.compile(r"alt\('?(?P<vzor>.*?)'?,'?(?P<alternacia>.*?)'?\)")
        for line in subor:
            if line[0:3] == "alt":
                m_alt = re.match(re_alt, line)
                alternacie_vzorov[m_alt.group('vzor')] = m_alt.group('alternacia')
            elif line[0:7] == "postfix":
                m_pf = re.match(re_pf, line)
                postfix_dict[m_pf.group('postfix')] = m_pf.group('koncovky').replace('\'', '')
            elif line[0:7] == "vzorsub":
                m_v = re.match(re_vzor, line)
                vzor = m_v.group('vzor').replace('\'', '')
                rod = m_v.group('rod')
                pf = m_v.group('postfix').replace('\'', '')
                alternacia = None
                if vzor in alternacie_vzorov.keys():
                    alternacia = alternacie_vzorov[vzor]

                zaloz_vzor("POD_M", vzor, rod, postfix_dict[pf], alternacia)
                print(f"Vzor:{vzor} rod:{rod} "
                      f"koncovky:{postfix_dict[pf]}")
