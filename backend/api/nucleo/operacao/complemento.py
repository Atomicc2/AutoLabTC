"""
Operação de complemento de autômatos finitos determinísticos (AFD).

O complemento de um AFD é obtido completando o autômato, adicionando
um estado sumidouro e as transições ausentes, quando necessário, e,
em seguida, invertendo os estados finais e não finais.

A operação exige que o autômato de entrada seja um AFD. Caso seja
recebido um AFN (transições épsilon ou não determinismo), é lançada
a exceção OperacaoInvalidaError, indicando a necessidade de conversão
prévia para AFD.

Cada etapa intermediária é registrada em uma lista de Etapa, contendo
uma descrição textual e uma cópia do autômato naquele momento. Essas
etapas podem ser consumidas posteriormente pelo gerador de PDF.
"""

from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.dto.resultado_operacao import ResultadoOperacao
from api.nucleo.excecoes import OperacaoInvalidaError
from api.nucleo.dto.etapa import Etapa
from api.nucleo.utilitario.utilitarios_operacoes import completar, inverter_finais

def complemento(automato: AutomatoFinito) -> ResultadoOperacao:
    """
    Calcula o complemento de um autômato finito determinístico (AFD).

    A operação realiza as seguintes etapas:
        1. Valida se o autômato de entrada é um AFD.
        2. Cria uma cópia do autômato original.
        3. Registra a etapa do autômato original.
        4. Completa o autômato com um estado sumidouro, se necessário,
           registrando essa transformação.
        5. Inverte os estados finais e não finais, registrando o
           resultado final.

    Args:
        automato: AFD de entrada.

    Returns:
        ResultadoOperacao: Contém o autômato resultante do complemento
        no atributo automato_final e as etapas da operação no atributo
        etapas.

    Raises:
        OperacaoInvalidaError: Se o autômato informado não for um AFD,
        seja por possuir transições épsilon ou não determinismo.
    """

    automato = automato.copiar()

    if not automato.eh_afd():
        raise OperacaoInvalidaError(
            "A operação complemento exige um AFD. "
            "O autômato informado é não determinístico; converta-o para AFD antes."
        )

    etapas: list[Etapa] = []

    etapas.append(
        Etapa(
            descricao = "Autômato original (AFD)", 
            automato = automato.copiar()
        )
    )

    if not automato.eh_completo():
        completar(automato)
        etapas.append(
            Etapa(
                descricao = "Completar autômato (estado sumidouro)",
                automato = automato.copiar(),
            )
        )

    inverter_finais(automato)
    etapas.append(
        Etapa(
            descricao = "Autômato complemento", 
            automato = automato.copiar()
        )
    )

    return ResultadoOperacao(
        automato_final = automato.copiar(),
        etapas = etapas
    )
