import shutil
from io import BytesIO
from zipfile import ZipFile

import pytest

from api.nucleo.dto.resposta_operacao import RespostaOperacao
from api.nucleo.utilitario.utilitarios_jff import converter_jff_para_automato
from api.servicos.operacoes_servico import complemento

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


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex não está disponível no PATH.",
)
def test_complemento():
    resultado = complemento(JFF)

    assert isinstance(resultado, RespostaOperacao)
    assert "<structure>" in resultado.arquivo_jff

    automato = converter_jff_para_automato(resultado.arquivo_jff)

    assert automato.eh_afd()


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex não está disponível no PATH.",
)
def test_complemento_retorna_relatorio_pdf():
    resultado = complemento(JFF)

    assert resultado.relatorio_pdf.startswith(b"%PDF")
    assert len(resultado.relatorio_pdf) > 1000


def test_compactar_empacota_arquivos():
    resposta = RespostaOperacao(arquivo_jff="<xml/>", relatorio_pdf=b"%PDF")

    conteudo = resposta.compactar("operacao")

    with ZipFile(BytesIO(conteudo)) as zip:
        nomes = zip.namelist()
        jff = zip.read("operacao.jff")
        pdf = zip.read("operacao.pdf")

    assert nomes == ["operacao.jff", "operacao.pdf"]
    assert jff == b"<xml/>"
    assert pdf == b"%PDF"
