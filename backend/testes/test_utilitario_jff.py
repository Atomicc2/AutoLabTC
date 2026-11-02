import api.nucleo.excecoes
import api.nucleo.utilitarioJFF

JFF_SIMPLES = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<structure>
    <type>fa</type>
    <automaton>
        <state id="0" name="q0">
            <x>100.0</x>
            <y>200.0</y>
            <initial/>
        </state>
        <state id="1" name="q1">
            <x>300.0</x>
            <y>200.0</y>
            <final/>
        </state>
        <transition>
            <from>0</from>
            <to>1</to>
            <read>a</read>
        </transition>
        <transition>
            <from>1</from>
            <to>1</to>
            <read>b</read>
        </transition>
    </automaton>
</structure>
"""

JFF_EPSILON = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<structure>
    <type>fa</type>
    <automaton>
        <state id="0" name="q0">
            <x>100.0</x>
            <y>200.0</y>
            <initial/>
        </state>
        <state id="1" name="q1">
            <x>300.0</x>
            <y>200.0</y>
            <final/>
        </state>
        <transition>
            <from>0</from>
            <to>1</to>
            <read/>
        </transition>
    </automaton>
</structure>
"""


def escrever_jff(tmp_path, conteudo, nome="automato.jff"):
    caminho = tmp_path / nome
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def test_converter_automato_simples(tmp_path):
    caminho = escrever_jff(tmp_path, JFF_SIMPLES)
    automato = api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
    automato.validar()  # não deve lançar
    assert sorted(e.nome for e in automato.estados) == ["q0", "q1"]
    assert automato.alfabeto == {"a", "b"}
    assert len(automato.transicoes) == 2
    assert automato.estado_inicial.nome == "q0"
    assert [e.nome for e in automato.estados_finais] == ["q1"]


def test_converter_transicao_epsilon(tmp_path):
    caminho = escrever_jff(tmp_path, JFF_EPSILON)
    automato = api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
    assert automato.transicoes[0].simbodo is None
    assert automato.alfabeto == set()


def test_converter_estado_sem_name_usa_id(tmp_path):
    jff = JFF_SIMPLES.replace('<state id="0" name="q0">', '<state id="0">')
    caminho = escrever_jff(tmp_path, jff)
    automato = api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
    assert any(e.nome == "0" for e in automato.estados)


def test_arquivo_inexistente(tmp_path):
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(tmp_path / "abc.jff")
        assert False, "deveria lançar ErroAutomatoNaoEncontrado"
    except api.nucleo.excecoes.ErroAutomatoNaoEncontrado:
        pass


def test_xml_invalido(tmp_path):
    caminho = escrever_jff(tmp_path, "<structure><automaton>")
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_raiz_inesperada(tmp_path):
    caminho = escrever_jff(tmp_path, "<notas>oi</notas>")
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_tipo_nao_fa(tmp_path):
    jff = JFF_SIMPLES.replace("<type>fa</type>", "<type>turing</type>")
    caminho = escrever_jff(tmp_path, jff)
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_sem_secao_automaton(tmp_path):
    caminho = escrever_jff(tmp_path, "<structure><type>fa</type></structure>")
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_transicao_estado_inexistente(tmp_path):
    jff = JFF_SIMPLES.replace("<from>0</from>", "<from>9</from>", 1)
    caminho = escrever_jff(tmp_path, jff)
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_sem_estado_inicial(tmp_path):
    jff = JFF_SIMPLES.replace("<initial/>", "")
    caminho = escrever_jff(tmp_path, jff)
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_dois_estados_iniciais(tmp_path):
    jff = JFF_SIMPLES.replace("<final/>", "<final/><initial/>")
    caminho = escrever_jff(tmp_path, jff)
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_estado_sem_id(tmp_path):
    jff = JFF_SIMPLES.replace('<state id="0" name="q0">', '<state name="q0">')
    caminho = escrever_jff(tmp_path, jff)
    try:
        api.nucleo.utilitarioJFF.UtilitarioJFF.converter(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass
