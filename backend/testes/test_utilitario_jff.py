import api.nucleo.automato_finito
import api.nucleo.estado
import api.nucleo.transicao
import api.nucleo.excecoes
from api.nucleo.utilitario.utilitarios_jff import converter_automato_para_jff, converter_jff_para_automato, serializar


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
    automato = converter_jff_para_automato(caminho)

    automato.validar()  # não deve lançar
    assert sorted(e.nome for e in automato.estados) == ["q0", "q1"]
    assert automato.alfabeto == {"a", "b"}
    assert len(automato.transicoes) == 2
    assert automato.estado_inicial.nome == "q0"
    assert [e.nome for e in automato.estados_finais] == ["q1"]


def test_converter_transicao_epsilon(tmp_path):
    caminho = escrever_jff(tmp_path, JFF_EPSILON)
    automato = converter_jff_para_automato(caminho)

    assert automato.transicoes[0].simbodo is None
    assert automato.alfabeto == set()


def test_converter_estado_sem_name_usa_id(tmp_path):
    jff = JFF_SIMPLES.replace(
        '<state id="0" name="q0">',
        '<state id="0">'
    )
    caminho = escrever_jff(tmp_path, jff)
    automato = converter_jff_para_automato(caminho)

    assert any(e.nome == "0" for e in automato.estados)


def test_arquivo_inexistente(tmp_path):
    try:
        converter_jff_para_automato(
            tmp_path / "abc.jff"
        )
        assert False, "deveria lançar ErroAutomatoNaoEncontrado"
    except api.nucleo.excecoes.ErroAutomatoNaoEncontrado:
        pass


def test_xml_invalido(tmp_path):
    caminho = escrever_jff(tmp_path, "<structure><automaton>")

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_raiz_inesperada(tmp_path):
    caminho = escrever_jff(tmp_path, "<notas>oi</notas>")

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_tipo_nao_fa(tmp_path):
    jff = JFF_SIMPLES.replace(
        "<type>fa</type>",
        "<type>turing</type>"
    )
    caminho = escrever_jff(tmp_path, jff)

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_sem_secao_automaton(tmp_path):
    caminho = escrever_jff(
        tmp_path,
        "<structure><type>fa</type></structure>"
    )

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_transicao_estado_inexistente(tmp_path):
    jff = JFF_SIMPLES.replace(
        "<from>0</from>",
        "<from>9</from>",
        1
    )
    caminho = escrever_jff(tmp_path, jff)

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_sem_estado_inicial(tmp_path):
    jff = JFF_SIMPLES.replace("<initial/>", "")
    caminho = escrever_jff(tmp_path, jff)

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_dois_estados_iniciais(tmp_path):
    jff = JFF_SIMPLES.replace(
        "<final/>",
        "<final/><initial/>"
    )
    caminho = escrever_jff(tmp_path, jff)

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def test_estado_sem_id(tmp_path):
    jff = JFF_SIMPLES.replace(
        '<state id="0" name="q0">',
        '<state name="q0">'
    )
    caminho = escrever_jff(tmp_path, jff)

    try:
        converter_jff_para_automato(caminho)
        assert False, "deveria lançar ErroJFFInvalido"
    except api.nucleo.excecoes.ErroJFFInvalido:
        pass


def construir_automato_teste():
    q0 = api.nucleo.estado.Estado("q0", inicial=True)
    q1 = api.nucleo.estado.Estado("q1", final=True)

    automato = api.nucleo.automato_finito.AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a", "b"},
        estado_inicial=q0,
        estados_finais={q1},
    )

    automato.adicionar_transicao(
        api.nucleo.transicao.Transicao(q0, "a", q0)
    )
    automato.adicionar_transicao(
        api.nucleo.transicao.Transicao(q0, "b", q1)
    )
    automato.adicionar_transicao(
        api.nucleo.transicao.Transicao(q1, "a", q1)
    )

    return automato


def test_exportar_grava_arquivo(tmp_path):
    automato = construir_automato_teste()

    caminho = converter_automato_para_jff(
        automato,
        tmp_path / "saida.jff"
    )

    texto = caminho.read_text(encoding="utf-8")

    assert texto.startswith('<?xml version="1.0"')
    assert "<type>fa</type>" in texto
    assert 'name="q0"' in texto


def test_exportar_roundtrip(tmp_path):
    automato = construir_automato_teste()

    reconstruido = converter_jff_para_automato(
        converter_automato_para_jff(
            automato,
            tmp_path / "roundtrip.jff"
        )
    )

    reconstruido.validar()  # não deve lançar
    assert reconstruido.estados == automato.estados
    assert reconstruido.alfabeto == {"a", "b"}
    assert reconstruido.estado_inicial == automato.estado_inicial
    assert reconstruido.estados_finais == automato.estados_finais

    assert sorted(
        (t.origem.nome, t.simbodo, t.destino.nome)
        for t in reconstruido.transicoes
    ) == sorted(
        (t.origem.nome, t.simbodo, t.destino.nome)
        for t in automato.transicoes
    )


def test_exportar_transicao_epsilon(tmp_path):
    q0 = api.nucleo.estado.Estado("q0", inicial=True)
    q1 = api.nucleo.estado.Estado("q1", final=True)

    automato = api.nucleo.automato_finito.AutomatoFinito(
        estados={q0, q1},
        alfabeto=set(),
        estado_inicial=q0,
        estados_finais={q1}
    )

    automato.adicionar_transicao(
        api.nucleo.transicao.Transicao(q0, None, q1)
    )  # épsilon

    reconstruido = converter_jff_para_automato(
        converter_automato_para_jff(
            automato,
            tmp_path / "epsilon.jff"
        )
    )

    assert reconstruido.transicoes == [
        api.nucleo.transicao.Transicao(q0, None, q1)
    ]
    assert reconstruido.alfabeto == set()


def test_exportar_usa_atributos_do_automato(tmp_path):
    q0 = api.nucleo.estado.Estado("q0")  # flags inicial/final ausentes
    q1 = api.nucleo.estado.Estado("q1")

    automato = api.nucleo.automato_finito.AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1}
    )

    automato.adicionar_transicao(
        api.nucleo.transicao.Transicao(q0, "a", q1)
    )

    reconstruido = converter_jff_para_automato(
        converter_automato_para_jff(
            automato,
            tmp_path / "flags.jff"
        )
    )

    assert reconstruido.estado_inicial.nome == "q0"
    assert [e.nome for e in reconstruido.estados_finais] == ["q1"]


def test_serializar_ordem_deterministica():
    automato = construir_automato_teste()

    texto = serializar(automato)

    assert "<initial" in texto
    assert "<final" in texto
    assert texto.find('name="q0"') < texto.find('name="q1"')


def test_exportar_automato_invalido(tmp_path):
    automato = api.nucleo.automato_finito.AutomatoFinito(
        estados=set(),
        alfabeto=set(),
        estado_inicial=None
    )

    try:
        converter_automato_para_jff(
            automato,
            tmp_path / "invalido.jff"
        )
        assert False, "deveria lançar ValueError"
    except ValueError:
        pass