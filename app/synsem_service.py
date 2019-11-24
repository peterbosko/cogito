def je_sloveso(slovo):
    if slovo.anotacia[0] == "V":
        return True
    return False


def je_indikativ(slovo):
    if slovo.anotacia[1] == "K":
        return True
    return False


def vrat_sloveso(slova):
    pred = True
    slova_pred = []
    slova_po = []
    sloveso = None
    for s in slova:
        if je_sloveso(s) and je_indikativ(s) and pred:
            sloveso = s
            pred = False
        else:
            if pred:
                slova_pred.append(s)
            else:
                slova_po.append(s)

    return sloveso, slova_pred, slova_po


def veta(mod, slova):
    sloveso, s_pred, s_po = vrat_sloveso(slova)


def vrat_strom_vety(slova_vety):
    return veta("hl", slova_vety)

