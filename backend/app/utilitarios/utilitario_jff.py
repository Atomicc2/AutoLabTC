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

    @staticmethod
    def escrever(automato):
        estrutura = ElementTree.Element("structure")

        tipo = ElementTree.SubElement(estrutura, "type")
        tipo.text = "fa"

        no_automato = ElementTree.SubElement(estrutura, "automaton")

        for estado in automato.estados:
            no_estado = ElementTree.SubElement(
                no_automato, "state",
                {"id": str(estado.id), "name": estado.nome}
            )

            x = ElementTree.SubElement(no_estado, "x")
            x.text = str(estado.x)

            y = ElementTree.SubElement(no_estado, "y")
            y.text = str(estado.y)

            if estado.inicial:
                ElementTree.SubElement(no_estado, "initial")

            if estado.final:
                ElementTree.SubElement(no_estado, "final")

        for transicao in automato.transicoes:
            no_transicao = ElementTree.SubElement(no_automato, "transition")

            de = ElementTree.SubElement(no_transicao, "from")
            de.text = str(transicao.de)

            para = ElementTree.SubElement(no_transicao, "to")
            para.text = str(transicao.para)

            ElementTree.SubElement(no_transicao, "read").text = transicao.simbolo or None

        ElementTree.indent(estrutura)

        return ElementTree.tostring(estrutura, encoding="utf-8", xml_declaration=True)