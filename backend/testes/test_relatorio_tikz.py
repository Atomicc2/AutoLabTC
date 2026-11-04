from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.estado import Estado
from api.nucleo.transicao import Transicao
from api.relatorios.diagrama import automato_para_tikz
from api.relatorios.latex import escapar_latex


def construir_automato() -> AutomatoFinito:
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1", final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a", "b"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))
    automato.adicionar_transicao(Transicao(q0, "b", q1))
    automato.adicionar_transicao(Transicao(q1, "a", q1))
    return automato


def test_escapar_latex():
    assert escapar_latex("q_0") == r"q\_0"
    assert escapar_latex("a&b") == r"a\&b"
    assert escapar_latex("100%") == r"100\%"
    assert escapar_latex("{x}") == r"\{x\}"
    assert escapar_latex(r"a\b") == r"a\textbackslash{}b"
    assert escapar_latex("a~b^c") == r"a\textasciitilde{}b\textasciicircum{}c"


def test_tikz_contem_estados_e_transicoes():
    tikz = automato_para_tikz(construir_automato())

    assert tikz.startswith(r"\begin{tikzpicture}")
    assert tikz.endswith(r"\end{tikzpicture}")
    assert r"\node[state, initial] (q0)" in tikz
    assert r"\node[state, accepting] (q1)" in tikz
    assert "loop above" in tikz or "loop below" in tikz
    assert "a, b" in tikz


def test_tikz_com_epsilon():
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1", final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, None, q1))
    automato.adicionar_transicao(Transicao(q0, "a", q1))

    tikz = automato_para_tikz(automato)

    assert r"\varepsilon" in tikz
    assert r"a, \varepsilon" in tikz or r"\varepsilon, a" in tikz


def test_tikz_com_arestas_de_ida_e_volta():
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1")
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))
    automato.adicionar_transicao(Transicao(q1, "a", q0))

    tikz = automato_para_tikz(automato)

    assert tikz.count("bend left=25") == 2


def test_tikz_escapa_nomes_e_simbolos():
    q0 = Estado("q_0", inicial=True)
    q1 = Estado("q_1", final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a&b"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a&b", q1))

    tikz = automato_para_tikz(automato)

    assert r"q\_0" in tikz
    assert r"q\_1" in tikz
    assert r"a\&b" in tikz


def test_tikz_e_deterministico():
    automato = construir_automato()

    assert automato_para_tikz(automato) == automato_para_tikz(automato)
