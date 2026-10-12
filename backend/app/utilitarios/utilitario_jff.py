import xml.etree.ElementTree as ElementTree

from app.entidades import Estado, Transicao
from app.automato import AutomatoFinito


class UtilitarioJff:

    @staticmethod
    def ler(conteudo):
        raiz = ElementTree.fromstring(conteudo)

        estados = []
        transicoes = []
        alfabeto = set()

        for elemento in raiz.iter("state"):
            id_estado = int(elemento.get("id"))
            nome = elemento.get("name")
            inicial = elemento.find("initial") is not None
            final = elemento.find("final") is not None
            x = int(elemento.find("x").text)
            y = int(elemento.find("y").text)

            estados.append(Estado(id_estado, nome, inicial, final, x, y))

        for elemento in raiz.iter("transition"):
            de = int(elemento.find("from").text)
            para = int(elemento.find("to").text)

            simbolo = elemento.find("read").text
            if simbolo is None:
                simbolo = ""

            if simbolo != "":
                alfabeto.add(simbolo)

            transicoes.append(Transicao(de, para, simbolo))

        return AutomatoFinito(estados, transicoes, alfabeto)