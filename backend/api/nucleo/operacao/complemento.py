# Operação de complemento de um autômato finito determinístico (AFD).

# O complemento de um AFD é obtido completando o autômato (adicionando um
# estado sumidouro/lixo e as transições ausentes, quando necessário) e, em
# seguida, invertendo os estados finais e não finais.

# A operação exige que o autômato de entrada seja um AFD. Caso seja recebido
# um AFN (transições épsilon ou não determinismo), é lançada a exceção
# :class:`OperacaoInvalidaError`, indicando a necessidade de conversão prévia
# para AFD.

# Cada etapa intermediária é registrada em uma lista de :class:`Etapa`, que
# contém uma descrição textual e um snapshot do autômato naquele momento. Essa
# lista pode ser consumida posteriormente pelo ``UtilitarioPdf``.

from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.dto.resultado_operacao import ResultadoOperacao
from api.nucleo.excecoes import OperacaoInvalidaError
from api.nucleo.dto.etapa import Etapa
from api.nucleo.utilitario.utilitarios_operacoes import UtilitariosOperacoes

# Calcula o complemento de um AFD.

# Pré-condição: autômato deve ser um AFD. Se for um AFN (transições
# épsilon ou não determinismo), lança :class:`OperacaoInvalidaError`.

# Passos:
#     1. Valida a pré-condição (AFD).
#     2. Copia o autômato.
#     3. Registra a etapa "Autômato original (AFD)".
#     4. Completa o autômato (estado sumidouro) se necessário e registra.
#     5. Inverte estados finais/não finais e registra a etapa final.

# A lista de etapas intermediárias é anexada ao autômato retornado no
# atributo ``etapas`` (alias ``passos``).

# Args:
#     automato: AFD de entrada.

# Returns:
#     Novo autômato representando o complemento.

# Execeções:
#     OperacaoInvalidaError: se autômato não for um AFD.

def complemento(automato: AutomatoFinito) -> AutomatoFinito:
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
        UtilitariosOperacoes.completar(automato)
        etapas.append(
            Etapa(
                descricao = "Completar autômato (estado sumidouro)",
                automato = automato.copiar(),
            )
        )

    UtilitariosOperacoes.inverter_finais(automato)
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
