"""Geração do relatório PDF com as etapas de uma operação."""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from pylatex import Command, Document, NoEscape, Section

from api.nucleo.dto.resultado_operacao import ResultadoOperacao
from api.nucleo.excecoes import ErroGeracaoPdf
from api.relatorios.diagrama import automato_para_tikz


def gerar_pdf(
    resultado: ResultadoOperacao,
    titulo: str = "Complemento de AFD",
) -> bytes:
    """Gera um PDF com o diagrama de cada etapa da operação.

    O compilador ``pdflatex`` precisa estar disponível no ``PATH`` do
    processo. O documento é criado em um diretório temporário e o conteúdo
    binário do PDF é retornado; o código LaTeX não é exposto pela API.

    Raises:
        ErroGeracaoPdf: se o LaTeX não estiver disponível ou se a compilação
            falhar.
    """
    if shutil.which("pdflatex") is None:
        raise ErroGeracaoPdf(
            "O compilador LaTeX (pdflatex) não está disponível no servidor."
        )

    try:
        return _gerar_pdf(resultado, titulo)
    except ErroGeracaoPdf:
        raise
    except Exception as erro:
        raise ErroGeracaoPdf("Não foi possível gerar o PDF do relatório.") from erro


def _gerar_pdf(resultado: ResultadoOperacao, titulo: str) -> bytes:
    documento = Document(documentclass="article", page_numbers=False)
    documento.change_document_style("plain")
    documento.preamble.append(NoEscape(r"\usepackage{tikz}"))
    documento.preamble.append(NoEscape(r"\usetikzlibrary{automata,positioning}"))
    documento.preamble.append(Command("title", titulo))
    documento.preamble.append(Command("date", ""))

    documento.append(NoEscape(r"\maketitle"))
    documento.append(Section("Resumo", label=False))
    documento.append(f"Operação: {titulo}.")
    documento.append(NoEscape(r"\par\noindent"))
    documento.append(f"Total de etapas: {len(resultado.etapas)}.")
    documento.append(NoEscape(r"\par\bigskip"))

    for indice, etapa in enumerate(resultado.etapas, start=1):
        documento.append(Section(f"Etapa {indice} - {etapa.descricao}", label=False))
        documento.append(NoEscape(automato_para_tikz(etapa.automato)))
        documento.append(NoEscape(r"\par\bigskip"))

    documento.append(NoEscape(r"Documento gerado automaticamente pelo AutoLab-TC."))

    with TemporaryDirectory(prefix="autolab_pdf_") as diretorio:
        caminho_base = Path(diretorio) / "complemento"
        documento.generate_pdf(
            str(caminho_base),
            clean=True,
            clean_tex=True,
            compiler="pdflatex",
            compiler_args=["-halt-on-error"],
        )

        caminho_pdf = caminho_base.with_suffix(".pdf")
        if not caminho_pdf.exists() or caminho_pdf.stat().st_size == 0:
            raise ErroGeracaoPdf("O compilador LaTeX não produziu um PDF.")

        return caminho_pdf.read_bytes()
