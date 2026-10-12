import pytest


def montar_jff(estados, transicoes):
    linhas = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<structure>",
        "<type>fa</type>",
        "<automaton>",
    ]

    for id_estado, nome, inicial, final, x, y in estados:
        linhas.append(f'<state id="{id_estado}" name="{nome}">')
        linhas.append(f"<x>{x}</x>")
        linhas.append(f"<y>{y}</y>")
        if inicial:
            linhas.append("<initial/>")
        if final:
            linhas.append("<final/>")
        linhas.append("</state>")

    for de, para, simbolo in transicoes:
        linhas.append("<transition>")
        linhas.append(f"<from>{de}</from>")
        linhas.append(f"<to>{para}</to>")
        linhas.append(f"<read>{simbolo}</read>")
        linhas.append("</transition>")

    linhas.append("</automaton>")
    linhas.append("</structure>")

    return "\n".join(linhas).encode("utf-8")


@pytest.fixture
def criar_jff():
    return montar_jff
