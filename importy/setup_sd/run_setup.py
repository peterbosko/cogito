import sys
from importy.setup_sd.service import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        start = 0

        if len(sys.argv) > 2:
            start = int(sys.argv[2])

        if command == "updatuj_slovesa":
            updatuj_slovesa(start)
        elif command == "checkni_vyplnene_slovesa":
            checkni_vyplnene_slovesa(start)
        elif command == "generuj_a_porovnaj_slovesa":
            generuj_a_porovnaj_slovesa(start)
        elif command == "zisti_vzory_slovies":
            zisti_vzory_slovies(start)
        elif command == "zjednot_zamena":
            zjednot_zamena()
        elif command == "zjednot_cislovky":
            zjednot_cislovky()
        elif command == "anotuj_predlozky":
            anotuj_predlozky()
        elif command == "anotuj_cislovky":
            anotuj_cislovky()
        elif command == "anotuj_zamena":
            anotuj_zamena()
        elif command == "anotuj_prislovky":
            anotuj_prislovky()
        elif command == "anotuj_slovesa":
            anotuj_slovesa(start)
        elif command == "anotuj_pod_m":
            anotuj_pod_m(start)
        elif command == "anotuj_prid_m":
            anotuj_prid_m(start)

    else:
        print("usage:\n\n\trun_setup.py updatuj_slovesa | checkni_vyplnene_slovesa | generuj_a_porovnaj_slovesa "
              "| zisti_vzory_slovies | zjednot_zamena")
