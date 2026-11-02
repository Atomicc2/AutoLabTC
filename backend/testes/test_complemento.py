from api.nucleo.AutomatoFinito import AutomatoFinito
from api.nucleo.Estado import Estado
from api.nucleo.excecoes import OperacaoInvalidaError
from api.nucleo.operacao.Complemento import complemento
from api.nucleo.Transicao import Transicao


def test_complemento_de_afd_completo_inverte_finais():
    q0 = Estado("q0", inicial=True, final=False)
    q1 = Estado("q1", inicial=False, final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))
    automato.adicionar_transicao(Transicao(q1, "a", q0))

    resultado = complemento(automato)

    assert len(resultado.estados) == 2
    finais = {e.nome for e in resultado.estados if e.final}
    assert finais == {"q0"}

    finais_original = {e.nome for e in automato.estados if e.final}
    assert finais_original == {"q1"}


def test_complemento_de_afd_incompleto_adiciona_poco_e_completa():
    q0 = Estado("q0", inicial=True, final=True)
    q1 = Estado("q1", inicial=False, final=False)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q0},
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))

    resultado = complemento(automato)

    assert len(resultado.estados) == 3
    assert resultado.eh_completo()

    poco = next(e for e in resultado.estados if e.nome == "poço")
    assert poco.final is True

    auto_loops = [
        t
        for t in resultado.transicoes
        if t.origem == poco and t.destino == poco and t.simbodo == "a"
    ]
    assert len(auto_loops) == 1

    transicao_para_poco = [
        t
        for t in resultado.transicoes
        if t.origem.nome == "q1" and t.destino == poco and t.simbodo == "a"
    ]
    assert len(transicao_para_poco) == 1

    assert not automato.eh_completo()


def test_complemento_rejeita_afn():
    q0 = Estado("q0", inicial=True, final=False)
    q1 = Estado("q1", inicial=False, final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))
    automato.adicionar_transicao(Transicao(q0, "a", q0))  # não determinismo

    try:
        complemento(automato)
        assert False, "deveria lançar OperacaoInvalidaError"
    except OperacaoInvalidaError:
        pass

    # AFN com epsilon
    q2 = Estado("q2", inicial=True, final=False)
    q3 = Estado("q3", inicial=False, final=True)
    automato2 = AutomatoFinito(
        estados={q2, q3},
        alfabeto={"a"},
        estado_inicial=q2,
        estados_finais={q3},
    )
    automato2.adicionar_transicao(Transicao(q2, None, q3))
    try:
        complemento(automato2)
        assert False, "deveria lançar OperacaoInvalidaError"
    except OperacaoInvalidaError:
        pass


def test_complemento_registra_etapas():
    q0 = Estado("q0", inicial=True, final=False)
    q1 = Estado("q1", inicial=False, final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))
    automato.adicionar_transicao(Transicao(q1, "a", q0))

    resultado = complemento(automato)

    assert hasattr(resultado, "etapas")
    etapas = resultado.etapas
    assert isinstance(etapas, list)
    assert len(etapas) >= 2
    for etapa in etapas:
        assert hasattr(etapa, "descricao")
        assert etapa.descricao
        snap = etapa.snapshot if hasattr(etapa, "snapshot") else etapa.automato
        assert snap is not None
        assert isinstance(snap, AutomatoFinito)
