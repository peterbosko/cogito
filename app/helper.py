import re
from pyquery import PyQuery as pq

SPEC_ZNAKY = [".", ",", "!", "?", "\"", "'", ":"]
SPEC_ZNAKY_regexstr = "\\.|\\,|\\!|\\?|\\\"|\\'|\\:"


class ResponseStatus(object):
    OK = 1
    ERROR = 2


class CommonResponse(object):
    def __init__(self):
        self.status = ResponseStatus.OK
        self.error_text = ""
        self.message_text = ""
        self.data = None


class AutocompleteSingleResponse(object):
    id = None
    text = None


def daj_medzery_pred_specialne_znaky(text):

    rstr = "(?P<slovo>\\b(.*?)\\S)(?P<znak>["+SPEC_ZNAKY_regexstr+"])"

    regex = re.compile(r"{}".format(rstr), re.IGNORECASE)

    text = regex.sub(r"\g<slovo> \g<znak>", text)

    return text


def je_cislo(slovo):

    return slovo.replace('.', '', 1).isdigit()


def daj_cislo(slovo):
    if '.' in slovo:
        try:
            return float(slovo)
        except ValueError:
            return None
    else:
        try:
            return int(slovo)
        except ValueError:
            return None


def daj_prvy_non_whitespace_znak(html):
    for char in html:
        if not char.isspace():
            return char
    return None


def nekonci_bodkou(strvar):
    for i in reversed(range(0, len(strvar))):
        if strvar[i] == ".":
            return False
        elif not strvar[i].isspace():
            return True
    return True


def formatuj_datum(dt):
    if dt:
        return dt.strftime('%d.%m.%Y %H:%M:%S')
    return ""


"""def vyrob_korektne_html_z_editora(html):
    obsah_p = pq(html).contents()

    result = ""

    for content in obsah_p.items():
        if content.is_("span"):
            result += vyrob_korektne_html_z_editora(content.outerHtml())
        else:
            text = daj_medzery_pred_specialne_znaky(content.text())

            if pq(html).is_("span"):
                cl = pq(html).attr("class")
                sid = pq(html).attr("sid")
                result += "<span class='{cl}' sid='{id}'>{slovo}</span>".format(slovo=pq(html).outerHtml(),
                                                                                id=sid, cl=cl)
            else:
                result += "<p>{t}</p>".format(t=text)

    return result
"""
