from api.nucleo.dto.resultado_operacao import ResultadoOperacao
from api.nucleo.operacao.complemento import complemento as complemento_afd
from api.nucleo.utilitario.utilitarios_jff import (
    converter_automato_para_jff,
    converter_jff_para_automato,
)
from api.relatorios.documento import gerar_pdf


def _resultado_complemento(jff: str) -> ResultadoOperacao:
    """Executa a operação de complemento sobre o autômato do arquivo JFF."""
    automato = converter_jff_para_automato(jff)
    return complemento_afd(automato)


def complemento(jff: str) -> str:
    resultado = _resultado_complemento(jff)

    return converter_automato_para_jff(resultado.automato_final)


def complemento_pdf(jff: str) -> bytes:
    """Gera o relatório PDF com as etapas da operação de complemento."""
    return gerar_pdf(_resultado_complemento(jff))
