"""Conversão de um autômato finito para um diagrama TikZ."""

import math

from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.estado import Estado
from api.relatorios.latex import escapar_latex

_RAIO_MINIMO = 2.0
_ESPACO_POR_ESTADO = 3.2


def automato_para_tikz(automato: AutomatoFinito) -> str:
    """Gera o código TikZ que desenha um autômato finito.

    Os estados são distribuídos em um círculo, na ordem de descoberta a
    partir do estado inicial (busca em largura). Transições entre o mesmo
    par de estados são agrupadas em uma única aresta, com os símbolos
    separados por vírgula. Autotransições usam ``loop`` e arestas de ida e
    volta recebem uma curvatura para não se sobreporem.
    """
    automato.validar()

    estados = _ordenar_estados(automato)
    ids = {estado: f"q{indice}" for indice, estado in enumerate(estados)}
    indices = {estado: indice for indice, estado in enumerate(estados)}

    linhas = [r"\begin{tikzpicture}[shorten >=1pt,node distance=2.8cm,on grid,auto]"]

    posicoes = _posicoes_circulares(len(estados))
    for indice, estado in enumerate(estados):
        estilos = ["state"]
        if estado == automato.estado_inicial:
            estilos.append("initial")
        if estado in automato.estados_finais:
            estilos.append("accepting")

        x, y = posicoes[indice]
        linhas.append(
            f"  \\node[{', '.join(estilos)}] ({ids[estado]}) "
            f"at ({x:.1f},{y:.1f}) {{{escapar_latex(estado.nome)}}};"
        )

    transicoes = _agrupar_por_par(automato)
    arestas = sorted(
        transicoes.items(),
        key=lambda item: (indices[item[0][0]], indices[item[0][1]]),
    )

    if arestas:
        linhas.append(r"  \path[->]")
        comandos = []
        for (origem, destino), simbolos in arestas:
            rotulo = _rotulo_simbolos(simbolos)

            if origem == destino:
                direcao = (
                    "loop above" if posicoes[indices[origem]][1] >= 0 else "loop below"
                )
                comandos.append(
                    f"    ({ids[origem]}) edge [{direcao}] "
                    f"node {{{rotulo}}} ({ids[destino]})"
                )
                continue

            opcao = ""
            if (destino, origem) in transicoes:
                opcao = " [bend left=25]"

            comandos.append(
                f"    ({ids[origem]}) edge{opcao} "
                f"node {{{rotulo}}} ({ids[destino]})"
            )

        linhas.append("\n".join(comandos) + ";")

    linhas.append(r"\end{tikzpicture}")
    return "\n".join(linhas)


def _ordenar_estados(automato: AutomatoFinito) -> list[Estado]:
    """Ordena os estados pela descoberta em largura a partir do inicial.

    A ordem de descoberta deixa estados adjacentes próximos no círculo e
    garante que estados inalcançáveis apareçam ao final, em ordem de nome.
    """
    ordem: list[Estado] = []
    visitados: set[Estado] = set()
    fila: list[Estado] = [automato.estado_inicial]

    while fila:
        estado = fila.pop(0)
        if estado in visitados:
            continue

        visitados.add(estado)
        ordem.append(estado)
        for transicao in sorted(
            automato.transicoes,
            key=lambda transicao: (
                transicao.simbodo is not None,
                transicao.simbodo or "",
                transicao.destino.nome,
            ),
        ):
            if transicao.origem == estado and transicao.destino not in visitados:
                fila.append(transicao.destino)

    for estado in sorted(automato.estados, key=lambda estado: estado.nome):
        if estado not in visitados:
            ordem.append(estado)

    return ordem


def _posicoes_circulares(quantidade: int) -> list[tuple[float, float]]:
    """Distribui os estados em um círculo, começando pelo topo."""
    if quantidade == 1:
        return [(0.0, 0.0)]
    if quantidade == 2:
        return [(-_RAIO_MINIMO, 0.0), (_RAIO_MINIMO, 0.0)]

    raio = max(_RAIO_MINIMO, quantidade * _ESPACO_POR_ESTADO / (2 * math.pi))
    posicoes = []
    for indice in range(quantidade):
        angulo = math.radians(90 - 360 * indice / quantidade)
        posicoes.append((raio * math.cos(angulo), raio * math.sin(angulo)))
    return posicoes


def _agrupar_por_par(
    automato: AutomatoFinito,
) -> dict[tuple[Estado, Estado], list[str | None]]:
    """Agrupa os símbolos das transições por par de origem e destino."""
    grupos: dict[tuple[Estado, Estado], list[str | None]] = {}

    for transicao in sorted(
        automato.transicoes,
        key=lambda transicao: (
            transicao.origem.nome,
            transicao.destino.nome,
            transicao.simbodo is not None,
            transicao.simbodo or "",
        ),
    ):
        simbolos = grupos.setdefault((transicao.origem, transicao.destino), [])
        if transicao.simbodo not in simbolos:
            simbolos.append(transicao.simbodo)

    return grupos


def _rotulo_simbolos(simbolos: list[str | None]) -> str:
    """Monta o rótulo LaTeX de uma aresta."""
    rotulos = [
        r"\varepsilon" if simbolo is None else escapar_latex(simbolo)
        for simbolo in simbolos
    ]
    return ", ".join(rotulos)
