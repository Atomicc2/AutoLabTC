from api.nucleo.AutomatoFinito import AutomatoFinito
from api.nucleo.Estado import Estado
from api.nucleo.Transicao import Transicao


def test_estado_basico():
    e = Estado("q0", inicial=True, final=False)
    assert e.nome == "q0"
    assert e.inicial is True
    assert e.final is False


def test_transicao_normal_e_epsilon():
    q0 = Estado("q0")
    q1 = Estado("q1")
    t1 = Transicao(q0, "a", q1)
    t2 = Transicao(q0, None, q1)  # epsilon
    assert t1.simbodo == "a"
    assert t2.simbodo is None


def test_automato_valido():
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1", final=True)
    a = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    a.adicionar_transicao(Transicao(q0, "a", q1))
    a.validar()  # não deve lançar
    assert a.obter_estado_inicial() == q0


def test_validar_estado_inicial_ausente():
    q0 = Estado("q0")
    a = AutomatoFinito(estados={q0}, alfabeto=set(), estado_inicial=None)
    try:
        a.validar()
        assert False, "deveria lançar ValueError"
    except ValueError:
        pass


def test_validar_estado_final_inexistente():
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1", final=True)
    a = AutomatoFinito(
        estados={q0}, alfabeto=set(), estado_inicial=q0, estados_finais={q1}
    )
    try:
        a.validar()
        assert False, "deveria lançar ValueError"
    except ValueError:
        pass


def test_validar_transicao_estado_desconhecido():
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1")
    q2 = Estado("q2")
    a = AutomatoFinito(estados={q0, q1}, alfabeto={"a"}, estado_inicial=q0)
    a.adicionar_transicao(Transicao(q0, "a", q2))  # q2 não existe
    try:
        a.validar()
        assert False, "deveria lançar ValueError"
    except ValueError:
        pass


def test_validar_simbodo_fora_do_alfabeto():
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1")
    a = AutomatoFinito(estados={q0, q1}, alfabeto={"a"}, estado_inicial=q0)
    a.adicionar_transicao(Transicao(q0, "b", q1))  # 'b' não está no alfabeto
    try:
        a.validar()
        assert False, "deveria lançar ValueError"
    except ValueError:
        pass
