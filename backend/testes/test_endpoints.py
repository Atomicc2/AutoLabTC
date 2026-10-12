from fastapi.testclient import TestClient

from backend.app.main import app

cliente = TestClient(app)

AFD_COMPLETO = [
    (0, "q0", True, False, 0, 0),
    (1, "q1", False, True, 100, 0),
]
TRANSICOES_AFD = [(0, 1, "a"), (1, 0, "a")]

AFN = [
    (0, "q0", True, False, 0, 0),
    (1, "q1", False, True, 100, 0),
]
TRANSICOES_AFN = [(0, 1, "a"), (0, 0, "a")]


def test_listar_operacoes():
    resposta = cliente.get("/operacoes")

    assert resposta.status_code == 200
    assert "complemento" in resposta.json()


def test_executar_complemento_com_sucesso(criar_jff):
    conteudo = criar_jff(AFD_COMPLETO, TRANSICOES_AFD)

    resposta = cliente.post(
        "/operacoes/complemento",
        files={"arquivo": ("meu_afd.jff", conteudo, "application/xml")},
    )

    assert resposta.status_code == 200
    assert resposta.headers["content-type"].startswith("application/xml")
    assert "meu_afd_complemento.jff" in resposta.headers["content-disposition"]
    assert b"<structure>" in resposta.content


def test_executa_complemento_com_arquivo_jflap():
    conteudo = (
        b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        b"<!--Created with JFLAP 6.4.--><structure><type>fa</type><automaton>"
        b'<state id="0" name="q0"><x>484.0</x><y>278.0</y></state>'
        b'<state id="1" name="q1"><x>653.0</x><y>279.0</y><final/></state>'
        b"<transition><from>0</from><to>0</to><read>a</read></transition>"
        b"<transition><from>0</from><to>1</to><read>b</read></transition>"
        b"<transition><from>1</from><to>1</to><read>b</read></transition>"
        b"<transition><from>1</from><to>0</to><read>a</read></transition>"
        b"</automaton></structure>"
    )

    resposta = cliente.post(
        "/operacoes/complemento",
        files={"arquivo": ("afd_default.jff", conteudo, "application/xml")},
    )

    assert resposta.status_code == 200
    assert "afd_default_complemento.jff" in resposta.headers["content-disposition"]


def test_rejeita_extensao_diferente_de_jff(criar_jff):
    conteudo = criar_jff(AFD_COMPLETO, TRANSICOES_AFD)

    resposta = cliente.post(
        "/operacoes/complemento",
        files={"arquivo": ("meu_afd.txt", conteudo, "text/plain")},
    )

    assert resposta.status_code == 400
    assert "extensão" in resposta.json()["detail"]


def test_rejeita_xml_invalido():
    resposta = cliente.post(
        "/operacoes/complemento",
        files={"arquivo": ("quebrado.jff", b"<structure><automaton>", "application/xml")},
    )

    assert resposta.status_code == 400
    assert "detail" in resposta.json()


def test_rejeita_operacao_inexistente(criar_jff):
    conteudo = criar_jff(AFD_COMPLETO, TRANSICOES_AFD)

    resposta = cliente.post(
        "/operacoes/inexistente",
        files={"arquivo": ("meu_afd.jff", conteudo, "application/xml")},
    )

    assert resposta.status_code == 404
    assert "não existe" in resposta.json()["detail"]


def test_rejeita_automato_que_nao_e_afd(criar_jff):
    conteudo = criar_jff(AFN, TRANSICOES_AFN)

    resposta = cliente.post(
        "/operacoes/complemento",
        files={"arquivo": ("afn.jff", conteudo, "application/xml")},
    )

    assert resposta.status_code == 422
    assert "AFD" in resposta.json()["detail"]
