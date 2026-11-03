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
from api.nucleo.estado import Estado
from api.nucleo.excecoes import OperacaoInvalidaError
from api.nucleo.transicao import Transicao
from api.nucleo.dto.etapa import Etapa
from api.nucleo.utilitarios.utilitarios_operacoes import UtilitariosOperacoes

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
    if not automato.eh_afd():
        raise OperacaoInvalidaError(
            "A operação complemento exige um AFD. "
            "O autômato informado é não determinístico; converta-o para AFD antes."
        )

    resultado = automato.copiar()
    etapas: list[Etapa] = []

    etapas.append(
        Etapa(
            descricao = "Autômato original (AFD)", 
            automato = automato.copiar()
        )
    )

    if not resultado.eh_completo():
        UtilitariosOperacoes.completar(resultado)
        etapas.append(
            Etapa(
                descricao="Completar autômato (estado sumidouro)",
                automato=resultado.copiar(),
            )
        )

    UtilitariosOperacoes.inverter_finais(resultado)
    etapas.append(Etapa(descricao="Autômato complemento", automato=resultado.copiar()))

    resultado.etapas = etapas
    resultado.passos = etapas
    return resultado


def complemento_com_etapas(
    automato: AutomatoFinito,
) -> tuple[AutomatoFinito, list[Etapa]]:
    """Executa o complemento e retorna ``(autômato, etapas)``."""
    resultado = complemento(automato)
    etapas = getattr(resultado, "etapas", [])
    return resultado, etapas


class Complemento:

    @staticmethod
    def complemento(automato: AutomatoFinito) -> AutomatoFinito:
        return complemento(automato)

    @staticmethod
    def executar(automato: AutomatoFinito) -> tuple[AutomatoFinito, list[Etapa]]:
        return complemento_com_etapas(automato)
