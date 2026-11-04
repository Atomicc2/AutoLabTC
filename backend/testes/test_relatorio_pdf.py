import shutil

import pytest

from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.dto.etapa import Etapa
from api.nucleo.dto.resultado_operacao import ResultadoOperacao
from api.nucleo.estado import Estado
from api.nucleo.excecoes import ErroGeracaoPdf
from api.nucleo.transicao import Transicao
from api.relatorios import documento
from api.relatorios.documento import gerar_pdf


def construir_resultado() -> ResultadoOperacao:
    q0 = Estado("q0", inicial=True)
    q1 = Estado("q1", final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a", q1))
    automato.adicionar_transicao(Transicao(q1, "a", q1))

    return ResultadoOperacao(
        automato_final=automato.copiar(),
        etapas=[
            Etapa("Automato original", automato.copiar()),
            Etapa("Automato complemento", automato.copiar()),
        ],
    )


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex não está disponível no PATH.",
)
def test_gerar_pdf_com_etapas():
    pdf = gerar_pdf(construir_resultado())

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex não está disponível no PATH.",
)
def test_gerar_pdf_com_caracteres_especiais():
    q0 = Estado("q_0", inicial=True)
    q1 = Estado("q_1", final=True)
    automato = AutomatoFinito(
        estados={q0, q1},
        alfabeto={"a&b"},
        estado_inicial=q0,
        estados_finais={q1},
    )
    automato.adicionar_transicao(Transicao(q0, "a&b", q1))
    resultado = ResultadoOperacao(
        automato_final=automato.copiar(),
        etapas=[Etapa("Automato com caracteres especiais", automato.copiar())],
    )

    pdf = gerar_pdf(resultado)

    assert pdf.startswith(b"%PDF")


def test_erro_quando_pdflatex_nao_existe(monkeypatch):
    monkeypatch.setattr(documento.shutil, "which", lambda _: None)

    with pytest.raises(ErroGeracaoPdf):
        gerar_pdf(construir_resultado())
