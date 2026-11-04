from api.nucleo.dto.resposta_operacao import RespostaOperacao
from api.nucleo.dto.resultado_operacao import ResultadoOperacao
from api.nucleo.operacao.complemento import complemento as complemento_afd
from api.nucleo.utilitario.utilitarios_jff import (
    converter_automato_para_jff,
    converter_jff_para_automato,
)
from api.relatorios.documento import gerar_pdf


def complemento(jff: str) -> RespostaOperacao:
    """Realiza a operação de complemento e gera os arquivos de resposta.

    Converte o .jff recebido em um AutomatoFinito, calcula o complemento
    e produz o .jff do autômato resultante e o relatório PDF com as
    etapas intermediárias da operação.

    Raises:
        ErroJFFInvalido: se o conteúdo não for um .jff válido.
        OperacaoInvalidaError: se o autômato não for um AFD.
        ErroGeracaoPdf: se o relatório PDF não puder ser gerado.
    """
    automato = converter_jff_para_automato(jff)
    resultado = complemento_afd(automato)

    return RespostaOperacao(
        arquivo_jff=converter_automato_para_jff(resultado.automato_final),
        relatorio_pdf=gerar_pdf(resultado),
    )
