import pytest

from backend.app.entidades.automato_finito import AutomatoFinito
from backend.app.entidades.estado import Estado
from backend.app.entidades.transicao import Transicao
from backend.app.erros import OperacaoInvalidaError
from backend.app.servicos.operacoes import complemento


def test_complemento_de_afd_completo_inverte_finais():
    automato = AutomatoFinito(
        estados=[
            Estado(0, "q0", inicial=True, final=False, x=0, y=0),
            Estado(1, "q1", inicial=False, final=True, x=100, y=0),
        ],
        transicoes=[
            Transicao(0, 1, "a"),
            Transicao(1, 0, "a"),
        ],
    )

    resultado = complemento(automato)

    assert len(resultado.estados) == 2
    finais = {estado.id for estado in resultado.estados if estado.final}
    assert finais == {0}

    finais_original = {estado.id for estado in automato.estados if estado.final}
    assert finais_original == {1}


def test_complemento_de_afd_incompleto_adiciona_poco_e_completa():
    automato = AutomatoFinito(
        estados=[
            Estado(0, "q0", inicial=True, final=True, x=0, y=0),
            Estado(1, "q1", inicial=False, final=False, x=100, y=0),
        ],
        transicoes=[
            Transicao(0, 1, "a"),
        ],
    )

    resultado = complemento(automato)

    assert len(resultado.estados) == 3
    assert resultado.eh_completo()

    poco = resultado.estados[-1]
    assert poco.nome == "poço"
    assert poco.final is True

    auto_loops = [
        transicao
        for transicao in resultado.transicoes
        if transicao.de == poco.id and transicao.para == poco.id and transicao.simbolo == "a"
    ]
    assert len(auto_loops) == 1

    transicao_para_poco = [
        transicao
        for transicao in resultado.transicoes
        if transicao.de == 1 and transicao.para == poco.id and transicao.simbolo == "a"
    ]
    assert len(transicao_para_poco) == 1

    assert automato.eh_completo() is False


def test_complemento_rejeita_afn():
    automato = AutomatoFinito(
        estados=[
            Estado(0, "q0", inicial=True, final=False, x=0, y=0),
            Estado(1, "q1", inicial=False, final=True, x=100, y=0),
        ],
        transicoes=[
            Transicao(0, 1, "a"),
            Transicao(0, 0, "a"),
        ],
    )

    with pytest.raises(OperacaoInvalidaError):
        complemento(automato)
