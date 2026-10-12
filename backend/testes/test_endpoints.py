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
