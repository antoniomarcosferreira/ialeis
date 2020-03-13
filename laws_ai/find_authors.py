import re
from unicodedata import normalize


def authors(text):
    text = text.replace("Presidente da República", "")
    text = normalize('NFKD', text).encode(
        'ASCII', 'ignore').decode('ASCII')
    text = text.upper().split("ESTE TEXTO NAO SUBSTITUI O")[0]

    text = text.replace(" DE ", " ")
    text = text.replace(" DO ", " ")
    text = text.replace(" DOS ", " ")
    text = text.replace(" DA ", " ")

    text = text.replace(",", "")
    text = text.replace(". ", ".")
    text = text.replace(".\n", ".")
    text = text.replace("\r\n", " ")

    if 'ESTE\n' in text:
        text = text.split("ESTE\nTEXTO")[0]
    elif 'ESTE\r' in text:
        text = text.split("ESTE\rTEXTO")[0]
    else:
        text = text.split("ESTE TEXTO")[0]

    text = text.split("REPUBLICA")
    text = text[-1]

    text = text.upper()

    text = text.replace(".\n", "\n")

    text = text.replace("CASTELLO", "CASTELO")
    text = text.replace("H. \n", "H")
    text = text.replace("CASTELO\nBRANCO", "CASTELO BRANCO")
    text = text.replace("COSTA E COSTA", "COSTA E SILVA")
    text = text.replace("ERNESTE", "ERNESTO")
    text = text.replace("ERNESTRO", "ERNESTO")
    text = text.replace("ENESTRO", "ERNESTO")
    text = text.replace("GIESEL", "GEISEL")
    text = text.replace("GESIEL", "GEISEL")
    text = text.replace("EMILO", "EMILIO")
    text = text.replace("EMILHO", "EMILIO")

    text = text.replace("\n\t", "")
    text = text.split("\n")

    authors = []
    for i in text:
        i = " ".join(i.split())
        i = i.upper()
        if not i == ".":
            authors.append(i)
    authors = list(filter(None, authors))

    if "<" in " ".join(authors):
        return []

    authors_ok = []
    name = []
    for i in authors:
        name.append(i)
        if len(name) == 1 and len(i.split(" ")) < 2:
            continue

        name_ok = ' '.join(name)
        name_ok = name_ok.replace(".", " ")
        name_ok = " ".join(name_ok.split())
        name_ok = name_ok.strip()
        name_ok = name_ok.replace("JOAO B ", "JOAO ")
        name_ok = name_ok.replace("EJOAO", "JOAO")
        name_ok = name_ok.replace("AURELIANO CHAVE", "AURELIANO CHAVES")
        name_ok = name_ok.replace("SENADOR", "")
        name_ok = name_ok.replace("FIGUPIRED0", "FIGUEIREDO")
        name_ok = name_ok.replace("FIGUEIRED0", "FIGUEIREDO")
        name_ok = name_ok.replace("FIGIJEIREDO", "FIGUEIREDO")
        name_ok = name_ok.replace("FIGIJEIREDO", "FIGUEIREDO")

        if name_ok == "LUIZ INACIO": name_ok = 'LUIZ INACIO LULA SILVA'
        if name_ok == "LUIZ INACIO LULA": name_ok = 'LUIZ INACIO LULA SILVA'
        if name_ok == "LUIZ INACIO LULA DASILVA": name_ok = 'LUIZ INACIO LULA SILVA'
        if name_ok == "DAVI": name_ok = 'DAVI ALCOLUMBRE'
        if name_ok == "JAIR MESSIAS": name_ok = 'JAIR MESSIAS BOLSONARO'
        if name_ok == "JOSE ALENCAR": name_ok = 'JOSE ALENCAR GOMES SILVA'

        authors_ok.append(name_ok.strip())
        name = []

    return authors_ok
