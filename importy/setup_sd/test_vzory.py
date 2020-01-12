from importy.setup_sd.service import *
from app.morfo_service import *


def test_zakladne_vzory():
    with flask_app.app_context():
        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("chytať", "chytám", "chytajú")
        print(f"Vzor chytať:{vzor}")
        assert vzor == "chytať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("klaňať", "klaniam", "klaňajú")
        print(f"Vzor klaňať:{vzor}")
        assert vzor == "klaňať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("čítať", "čítam", "čítajú")
        print(f"Vzor čítať:{vzor}")
        assert vzor == "čítať"

        # koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("krášliť", "krášlim", "krášlia")
        # print(f"Vzor krášliť:{vzor}")
        # assert vzor == "krášliť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("kúpiť", "kúpim", "kúpia")
        print(f"Vzor kúpiť:{vzor}")
        assert vzor == "kúpiť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("kresliť", "kreslím", "kreslia")
        print(f"Vzor kresliť:{vzor}")
        assert vzor == "kresliť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("robiť", "robím", "robia")
        print(f"Vzor robiť:{vzor}")
        assert vzor == "robiť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("vidieť", "vidím", "vidia")
        print(f"Vzor vidieť:{vzor}")
        assert vzor == "vidieť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("kričať", "kričím", "kričia")
        print(f"Vzor kričať:{vzor}")
        assert vzor == "kričať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("brať", "beriem", "berú")
        print(f"Vzor brať:{vzor}")
        assert vzor == "brať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("hynúť", "hyniem", "hynú")
        print(f"Vzor hynúť:{vzor}")
        assert vzor == "hynúť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("trieť", "triem", "trú")
        print(f"Vzor trieť:{vzor}")
        assert vzor == "trieť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("rozumieť", "rozumiem", "rozumejú")
        print(f"Vzor rozumieť:{vzor}")
        assert vzor == "rozumieť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("niesť", "nesiem", "nesú")
        print(f"Vzor niesť:{vzor}")
        assert vzor == "niesť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("pracovať", "pracujem", "pracujú")
        print(f"Vzor pracovať:{vzor}")
        assert vzor == "pracovať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("kliať", "kľajem", "kľajú")
        print(f"Vzor kliať:{vzor}")
        assert vzor == "kliať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("žuť", "žujem", "žujú")
        print(f"Vzor žuť:{vzor}")
        assert vzor == "žuť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("piť", "pijem", "pijú")
        print(f"Vzor piť:{vzor}")
        assert vzor == "piť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("chudnúť", "chudnem", "chudnú")
        print(f"Vzor chudnúť:{vzor}")
        assert vzor == "chudnúť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("päť", "päjem", "päjú")
        print(f"Vzor päť:{vzor}")
        assert vzor == "päť"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("žať", "žnem", "žnú")
        print(f"Vzor žať:{vzor}")
        assert vzor == "žať"

        # koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("pojať", "pojmem", "pojmú")
        # print(f"Vzor jať:{vzor}")
        # assert vzor == "jať"

        koren, pzkmen, vzor, prefix, sufix, chyba = vrat_meta_info_o_slovese("česať", "češem", "češú")
        print(f"Vzor česať:{vzor}")
        assert vzor == "česať"


if __name__ == "__main__":
    test_zakladne_vzory()
