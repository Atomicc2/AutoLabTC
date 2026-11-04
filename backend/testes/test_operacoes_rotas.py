import shutil
from io import BytesIO
from zipfile import ZipFile

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.nucleo.dto.resposta_operacao import RespostaOperacao
from api.nucleo.excecoes import ErroGeracaoPdf
from api.nucleo.utilitario.utilitarios_jff import converter_jff_para_automato
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

JFF_AFN = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<structure>
    <type>fa</type>
    <automaton>
        <state id="0" name="q0">
            <x>100</x>
            <y>100</y>
            <initial/>
        </state>
        <state id="1" name="q1">
            <x>200</x>
            <y>100</y>
            <final/>
        </state>
        <transition>
            <from>0</from>
            <to>1</to>
            <read>a</read>
        </transition>
        <transition>
            <from>0</from>
            <to>0</to>
            <read>a</read>
        </transition>
    </automaton>
</structure>
"""


@pytest.fixture
def cliente() -> TestClient:
    return TestClient(app)


def enviar(cliente: TestClient, conteudo: bytes = b""):
    arquivo = conteudo if conteudo else JFF.encode("utf-8")
    return cliente.post(
        "/operacoes/complemento",
        files={"arquivo": ("automato.jff", arquivo, "application/xml")},
    )


def test_complemento_retorna_zip_com_os_dois_arquivos(cliente, monkeypatch):
    resposta_fake = RespostaOperacao(arquivo_jff=JFF, relatorio_pdf=b"%PDF-1.4\n")

    monkeypatch.setattr(operacoes_rotas, "complemento", lambda jff: resposta_fake)

    resposta = enviar(cliente)

    assert resposta.status_code == 200
    assert resposta.headers["content-type"] == "application/zip"
    assert (
        resposta.headers["content-disposition"]
        == 'attachment; filename="complemento.zip"'
    )

    with ZipFile(BytesIO(resposta.content)) as zip:
        assert zip.namelist() == ["complemento.jff", "complemento.pdf"]
        assert zip.read("complemento.jff") == JFF.encode("utf-8")
        assert zip.read("complemento.pdf") == b"%PDF-1.4\n"


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex não está disponível no PATH.",
)
def test_complemento_retorna_zip_real(cliente):
    resposta = enviar(cliente)

    assert resposta.status_code == 200

    with ZipFile(BytesIO(resposta.content)) as zip:
        jff = zip.read("complemento.jff")

    automato = converter_jff_para_automato(jff.decode("utf-8"))

    assert automato.eh_afd()


def test_jff_invalido_retorna_422(cliente):
    resposta = enviar(cliente, conteudo=b"isto nao e um xml")

    assert resposta.status_code == 422
    assert resposta.json()["detail"]


def test_afn_retorna_422(cliente):
    resposta = enviar(cliente, conteudo=JFF_AFN.encode("utf-8"))

    assert resposta.status_code == 422
    assert "AFD" in resposta.json()["detail"]


def test_erro_pdf_retorna_503(cliente, monkeypatch):
    def falhar(jff):
        raise ErroGeracaoPdf("O compilador LaTeX não está disponível no servidor.")

    monkeypatch.setattr(operacoes_rotas, "complemento", falhar)

    resposta = enviar(cliente)

    assert resposta.status_code == 503
    assert resposta.json() == {
        "detail": "O compilador LaTeX não está disponível no servidor."
    }
