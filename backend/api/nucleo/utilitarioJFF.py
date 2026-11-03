"""Utilitário que transforma arquivos .jff (XML do JFLAP) em um AutomatoFinito e vice-versa."""

import xml.etree.ElementTree as ET
from pathlib import Path

from api.nucleo.AutomatoFinito import AutomatoFinito
from api.nucleo.Estado import Estado
from api.nucleo.Transicao import Transicao
from api.nucleo.excecoes import ErroAutomatoNaoEncontrado, ErroJFFInvalido


class UtilitarioJFF:
    """Lê/grava arquivos .jff transformando-os de/para um objeto AutomatoFinito."""

    @staticmethod
    def converter(caminho: str | Path) -> AutomatoFinito:
        """Transforma o arquivo .jff apontado por `caminho` em um AutomatoFinito.

        O alfabeto é derivado das transições, pois o formato .jff não o
        declara explicitamente. Transições com `<read/>` vazio representam
        transições épsilon (`simbodo=None`).

        Raises:
            ErroAutomatoNaoEncontrado: se o arquivo não existir.
            ErroJFFInvalido: se o arquivo não for um .jff válido.
            ValueError: se o autômato resultante for inconsistente.
        """
        raiz = UtilitarioJFF._carregar_raiz(caminho)
        UtilitarioJFF._verificar_tipoFa(raiz)
        xml_automato = raiz.find("automaton")
        if xml_automato is None:
            raise ErroJFFInvalido("Arquivo .jff sem a seção <automaton>.")

        estados = UtilitarioJFF._extrair_estados(xml_automato)
        transicoes, alfabeto = UtilitarioJFF._extrair_transicoes(xml_automato, estados)

        automato = AutomatoFinito(
            estados=set(estados.values()),
            alfabeto=alfabeto,
            transicoes=transicoes,
            estado_inicial=UtilitarioJFF._extrair_estado_inicial(estados.values()),
            estados_finais={estado for estado in estados.values() if estado.final},
        )
        automato.validar()
        return automato

    @staticmethod
    def exportar(automato: AutomatoFinito, caminho: str | Path) -> Path:
        """Serializa o AutomatoFinito e grava o .jff resultante em `caminho`.

        Raises:
            ValueError: se o autômato for inconsistente (via `validar`).
        """
        caminho = Path(caminho)
        caminho.write_text(UtilitarioJFF.serializar(automato), encoding="utf-8")
        return caminho

    @staticmethod
    def serializar(automato: AutomatoFinito) -> str:
        """Transforma um AutomatoFinito no texto XML de um arquivo .jff.

        Os estados recebem ids sequenciais em ordem determinística de nome e
        coordenadas em grade, para que o arquivo abra organizado no JFLAP.
        Os marcadores `<initial/>` e `<final/>` são escritos a partir dos
        atributos `estado_inicial` e `estados_finais` do autômato.
        """
        automato.validar()
        ordem = sorted(
            automato.estados,
            key=lambda estado: (estado.nome, estado.inicial, estado.final),
        )
        ids = {estado: indice for indice, estado in enumerate(ordem)}

        raiz = ET.Element("structure")
        ET.SubElement(raiz, "type").text = "fa"
        xml_automato = ET.SubElement(raiz, "automaton")
        for indice, estado in enumerate(ordem):
            elemento = ET.SubElement(
                xml_automato, "state", id=str(indice), name=estado.nome
            )
            ET.SubElement(elemento, "x").text = f"{100.0 + (indice % 6) * 150:.1f}"
            ET.SubElement(elemento, "y").text = f"{100.0 + (indice // 6) * 150:.1f}"
            if estado == automato.estado_inicial:
                ET.SubElement(elemento, "initial")
            if estado in automato.estados_finais:
                ET.SubElement(elemento, "final")
        for transicao in sorted(
            automato.transicoes,
            key=lambda t: (ids[t.origem], ids[t.destino], t.simbodo or ""),
        ):
            elemento = ET.SubElement(xml_automato, "transition")
            ET.SubElement(elemento, "from").text = str(ids[transicao.origem])
            ET.SubElement(elemento, "to").text = str(ids[transicao.destino])
            if transicao.simbodo is None:
                ET.SubElement(elemento, "read")  # <read/> vazio representa épsilon.
            else:
                ET.SubElement(elemento, "read").text = transicao.simbodo

        ET.indent(raiz)
        texto = ET.tostring(raiz, encoding="unicode")
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + texto + "\n"
        )

    @staticmethod
    def _carregar_raiz(caminho: str | Path) -> ET.Element:
        """Lê e valida o XML do arquivo .jff, retornando o elemento raiz."""
        caminho = Path(caminho)
        if not caminho.is_file():
            raise ErroAutomatoNaoEncontrado(f"Arquivo não encontrado: '{caminho}'.")
        try:
            raiz = ET.parse(caminho).getroot()
        except ET.ParseError as erro:
            raise ErroJFFInvalido(f"O arquivo não é um XML válido: {caminho.name}.") from erro
        if raiz.tag != "structure":
            raise ErroJFFInvalido(
                f"Elemento raiz inesperado <{raiz.tag}>, esperado <structure>."
            )
        return raiz

    @staticmethod
    def _verificar_tipoFa(raiz: ET.Element) -> None:
        """Confirma que o arquivo descreve um autômato finito (`<type>` = 'fa')."""
        tipo = raiz.findtext("type")
        if tipo is not None and tipo.strip() != "fa":
            raise ErroJFFInvalido(
                f"O arquivo descreve um '{tipo.strip()}', e não um autômato finito ('fa')."
            )

    @staticmethod
    def _extrair_estados(xml_automato: ET.Element) -> dict[int, Estado]:
        """Constrói os estados do .jff, indexados pelo atributo `id`."""
        estados: dict[int, Estado] = {}
        for elemento in xml_automato.findall("state"):
            try:
                id_estado = int(elemento.attrib["id"])
            except (KeyError, ValueError) as erro:
                raise ErroJFFInvalido(
                    "Estado sem atributo 'id' numérico válido."
                ) from erro
            if id_estado in estados:
                raise ErroJFFInvalido(f"Estado com id '{id_estado}' duplicado no arquivo.")
            estados[id_estado] = Estado(
                nome=elemento.attrib.get("name", str(id_estado)),
                inicial=elemento.find("initial") is not None,
                final=elemento.find("final") is not None,
            )
        if not estados:
            raise ErroJFFInvalido("O arquivo .jff não possui estados.")
        return estados

    @staticmethod
    def _extrair_transicoes(
        xml_automato: ET.Element, estados: dict[int, Estado]
    ) -> tuple[list[Transicao], set[str]]:
        """Constrói as transições do .jff e o alfabeto a partir das leituras."""
        transicoes: list[Transicao] = []
        alfabeto: set[str] = set()
        for elemento in xml_automato.findall("transition"):
            try:
                origem = estados[int(elemento.findtext("from"))]
                destino = estados[int(elemento.findtext("to"))]
            except (KeyError, TypeError, ValueError) as erro:
                raise ErroJFFInvalido(
                    "Transição com <from>/<to> ausente ou referenciando estado inexistente."
                ) from erro
            leitura = (elemento.findtext("read") or "").strip()
            simbodo = leitura or None  # <read/> vazio representa transição épsilon.
            if simbodo is not None:
                alfabeto.add(simbodo)
            transicoes.append(Transicao(origem=origem, simbodo=simbodo, destino=destino))
        return transicoes, alfabeto

    @staticmethod
    def _extrair_estado_inicial(estados) -> Estado:
        """Retorna o único estado marcado como `<initial/>` no .jff."""
        iniciais = [estado for estado in estados if estado.inicial]
        if len(iniciais) != 1:
            raise ErroJFFInvalido(
                f"Esperado um estado inicial, encontrado {len(iniciais)}."
            )
        return iniciais[0]
