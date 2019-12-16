from importy.sapfo.service import *
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "vytvor_slovniky":
            mode = "all"
            if len(sys.argv) > 2:
                mode = sys.argv[2]
            p, s = vytvor_slovniky(mode)
            print(f"{p} slov bolo zmenených...")
            print(f"Pocet sparovanych slov:{s}")
        elif command == "vloz_intencie":
            p = importuj_sapfo_intenciu()
            print(f"{p} intencii bolo pridanych...")
        elif command == "spracuj_slovniky":
            mode = "all"
            if len(sys.argv) > 2:
                mode = sys.argv[2]
            spracuj_slovniky(mode)
        elif command == "spracuj_pzkmene":
            spracuj_pzkmene()

    else:
        print("usage:\n\n\trun_import.py [ vytvor_slovniky all|sub|sl|adj|adv|cast|cisl|cit ] | "
              "vloz_intencie | spracuj_slovniky | spracuj_pzkmene ]")
