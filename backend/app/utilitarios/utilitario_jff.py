from xml.etree import ElementTree

from defusedxml import ElementTree as DefusedElementTree
from defusedxml.common import DefusedXmlException

from backend.app.entidades.automato_finito import AutomatoFinito
from backend.app.entidades.estado import Estado
from backend.app.entidades.transicao import Transicao
from backend.app.erros import ArquivoInvalidoError


class UtilitarioJff:

    @staticmethod
    def ler(conteudo):
        if not conteudo:
            raise ArquivoInvalidoError("O arquivo .jff está vazio.")

        try:
            raiz = DefusedElementTree.fromstring(conteudo)
        except (ElementTree.ParseError, DefusedXmlException, ValueError) as erro:
            raise ArquivoInvalidoError("O arquivo .jff não contém um XML válido.") from erro

        if raiz.tag != "structure":
            raise ArquivoInvalidoError("O arquivo .jff não possui a tag <structure>.")

        automaton = raiz.find("automaton")
        if automaton is None:
            raise ArquivoInvalidoError("O arquivo .jff não possui a tag <automaton>.")

        estados = []
        transicoes = []
        alfabeto = set()

        try:
            for elemento in automaton.iter("state"):
                id_estado = int(elemento.get("id"))
                nome = elemento.get("name")
                inicial = elemento.find("initial") is not None
                final = elemento.find("final") is not None
                x = int(elemento.find("x").text)
                y = int(elemento.find("y").text)

                estados.append(Estado(id_estado, nome, inicial, final, x, y))

            for elemento in automaton.iter("transition"):
                de = int(elemento.find("from").text)
                para = int(elemento.find("to").text)

                no_simbolo = elemento.find("read")
                if no_simbolo is None:
                    raise ArquivoInvalidoError(
                        "Uma transição do arquivo .jff não possui a tag <read>."
                    )

                simbolo = no_simbolo.text
                if simbolo is None:
                    simbolo = ""

                if simbolo != "":
                    alfabeto.add(simbolo)

                transicoes.append(Transicao(de, para, simbolo))
        except ArquivoInvalidoError:
            raise
        except (TypeError, ValueError, AttributeError) as erro:
            raise ArquivoInvalidoError(
                "O arquivo .jff possui campos inválidos ou tags obrigatórias ausentes."
            ) from erro

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
