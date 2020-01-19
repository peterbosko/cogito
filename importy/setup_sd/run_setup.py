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

    else:
        print("usage:\n\n\trun_setup.py updatuj_slovesa | checkni_vyplnene_slovesa")
