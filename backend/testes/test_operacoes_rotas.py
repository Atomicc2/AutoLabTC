import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.nucleo.excecoes import ErroGeracaoPdf
from api.rotas import operacoes_rotas

JFF = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<structure>
    <type>fa</type>
    <automaton>
        <state id="0" name="q0">
            <x>100</x>
            <y>100</y>
            <initial/>
            <final/>
        </state>
        <state id="1" name="q1">
            <x>200</x>
            <y>100</y>
        </state>
        <transition>
            <from>0</from>
            <to>1</to>
            <read>a</read>
        </transition>
    </automaton>
</structure>
"""


@pytest.fixture
def cliente() -> TestClient:
    return TestClient(app)


def enviar(cliente: TestClient, formato: str | None = None):
    parametros = {} if formato is None else {"formato": formato}
    return cliente.post(
        "/operacoes/complemento",
        params=parametros,
        files={"arquivo": ("automato.jff", JFF, "application/xml")},
    )


def test_complemento_retorna_jff_por_padrao(cliente):
    resposta = enviar(cliente)

    assert resposta.status_code == 200
    assert resposta.headers["content-type"].startswith("application/xml")
    assert "<structure>" in resposta.text


def test_complemento_pdf_retorna_anexo(cliente, monkeypatch):
    monkeypatch.setattr(
        operacoes_rotas, "complemento_pdf", lambda jff: b"%PDF-1.4\nconteudo"
    )

    resposta = enviar(cliente, formato="pdf")

    assert resposta.status_code == 200
    assert resposta.headers["content-type"] == "application/pdf"
    assert (
        resposta.headers["content-disposition"]
        == 'attachment; filename="complemento.pdf"'
    )
    assert resposta.content.startswith(b"%PDF-1.4")


def test_complemento_pdf_indisponivel_retorna_503(cliente, monkeypatch):
    def falhar(jff):
        raise ErroGeracaoPdf("O compilador LaTeX não está disponível no servidor.")

    monkeypatch.setattr(operacoes_rotas, "complemento_pdf", falhar)

    resposta = enviar(cliente, formato="pdf")

    assert resposta.status_code == 503
    assert resposta.json() == {
        "detail": "O compilador LaTeX não está disponível no servidor."
    }


def test_formato_invalido_retorna_422(cliente):
    resposta = enviar(cliente, formato="json")

    assert resposta.status_code == 422
