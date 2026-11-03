
import xml.etree.ElementTree as ET

from pathlib import Path

from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.estado import Estado
from api.nucleo.transicao import Transicao
from api.nucleo.excecoes import ErroJFFInvalido


def converter_jff_para_automato(jff: str) -> AutomatoFinito:
    """Transforma o conteúdo XML de um arquivo .jff em um AutomatoFinito.

    O alfabeto é derivado das transições, pois o formato .jff não o
    declara explicitamente. Transições com <read/> vazio representam
    transições épsilon (simbodo=None).

    Raises:
        ErroJFFInvalido: se o conteúdo não for um .jff válido.
        ValueError: se o autômato resultante for inconsistente.
    """
    try:
        raiz = ET.fromstring(jff)
    except ET.ParseError as erro:
        raise ErroJFFInvalido("O conteúdo fornecido não é um XML válido.") from erro

    if raiz.tag != "structure":
        raise ErroJFFInvalido(
            f"Elemento raiz inesperado <{raiz.tag}>, esperado <structure>."
        )

    _verificar_tipo_fa(raiz)

    xml_automato = raiz.find("automaton")
    if xml_automato is None:
        raise ErroJFFInvalido("Arquivo .jff sem a seção <automaton>.")

    estados = _extrair_estados(xml_automato)
    transicoes, alfabeto = _extrair_transicoes(xml_automato, estados)

    automato = AutomatoFinito(
        estados=set(estados.values()),
        alfabeto=alfabeto,
        transicoes=transicoes,
        estado_inicial=_extrair_estado_inicial(estados.values()),
        estados_finais={estado for estado in estados.values() if estado.final},
    )
    automato.validar()
    return automato


def converter_automato_para_jff(automato: AutomatoFinito) -> str:
    """Transforma um AutomatoFinito no conteúdo XML de um arquivo .jff."""
    return serializar(automato)


def salvar_jff(jff: str, caminho: str | Path) -> Path:
    """Grava o conteúdo XML de um .jff no caminho informado."""
    caminho = Path(caminho)
    caminho.write_text(jff, encoding="utf-8")
    return caminho


def serializar(automato: AutomatoFinito) -> str:
    """Transforma um AutomatoFinito no texto XML de um arquivo .jff.

    Os estados recebem ids sequenciais em ordem determinística de nome e
    coordenadas em grade, para que o arquivo abra organizado no JFLAP.
    Os marcadores <initial/> e <final/> são escritos a partir dos
    atributos estado_inicial e estados_finais do autômato.
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
            ET.SubElement(elemento, "read")
        else:
            ET.SubElement(elemento, "read").text = transicao.simbodo

    ET.indent(raiz)
    texto = ET.tostring(raiz, encoding="unicode")

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + texto + "\n"
    )


def _verificar_tipo_fa(raiz: ET.Element) -> None:
    """Confirma que o conteúdo descreve um autômato finito (<type> = 'fa')."""
    tipo = raiz.findtext("type")
    if tipo is not None and tipo.strip() != "fa":
        raise ErroJFFInvalido(
            f"O arquivo descreve um '{tipo.strip()}', e não um autômato finito ('fa')."
        )


def _extrair_estados(xml_automato: ET.Element) -> dict[int, Estado]:
    """Constrói os estados do .jff, indexados pelo atributo id."""
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
        simbodo = leitura or None

        if simbodo is not None:
            alfabeto.add(simbodo)

        transicoes.append(
            Transicao(origem=origem, simbodo=simbodo, destino=destino)
        )

    return transicoes, alfabeto


def _extrair_estado_inicial(estados) -> Estado:
    """Retorna o único estado marcado como <initial/> no .jff."""
    iniciais = [estado for estado in estados if estado.inicial]

    if len(iniciais) != 1:
        raise ErroJFFInvalido(
            f"Esperado um estado inicial, encontrado {len(iniciais)}."
        )

    return iniciais[0]
