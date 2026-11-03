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

# Método completar()
# Completa autômato adicionando um estado sumidouro (poço) e as
# transições ausentes, quando necessário.

# Se o autômato já for completo, nenhum estado é adicionado. Retorna o
# próprio autômato (mutado).
def completar(automato: AutomatoFinito) -> AutomatoFinito:

    simbodos = sorted(automato.alfabeto)

    existentes: set[tuple[Estado, str | None]] = set()
    for transicao in automato.transicoes:
        if transicao.simbodo is not None:
            existentes.add((transicao.origem, transicao.simbodo))

    faltantes: list[tuple[Estado, str]] = []
    for estado in automato.estados:
        for simbodo in simbodos:
            if (estado, simbodo) not in existentes:
                faltantes.append((estado, simbodo))

    if not faltantes:
        return automato

    # Garante nome único para o estado sumidouro.
    nome_poco = "poço"
    nomes_existentes = {estado.nome for estado in automato.estados}
    if nome_poco in nomes_existentes:
        sufixo = 1
        while f"{nome_poco}_{sufixo}" in nomes_existentes:
            sufixo += 1
        nome_poco = f"{nome_poco}_{sufixo}"

    poco = Estado(nome_poco, inicial=False, final=False)
    automato.adicionar_estado(poco)

    for estado_origem, simbodo in faltantes:
        automato.adicionar_transicao(
            Transicao(origem=estado_origem, simbodo=simbodo, destino=poco)
        )

    for simbodo in simbodos:
        automato.adicionar_transicao(
            Transicao(origem=poco, simbodo=simbodo, destino=poco)
        )

    return automato


# Método _inverter_finais()
# Inverte estados finais e não finais de autômato (in place).
def _inverter_finais(automato: AutomatoFinito) -> AutomatoFinito:
    mapeamento: dict[Estado, Estado] = {}
    novos_estados: set[Estado] = set()
    for estado in automato.estados:
        novo = Estado(
            nome=estado.nome,
            inicial=estado.inicial,
            final=not estado.final,
        )
        mapeamento[estado] = novo
        novos_estados.add(novo)

    automato.estados = novos_estados
    if automato.estado_inicial is not None:
        automato.estado_inicial = mapeamento[automato.estado_inicial]
    automato.transicoes = [
        Transicao(
            origem=mapeamento[t.origem],
            simbodo=t.simbodo,
            destino=mapeamento[t.destino],
        )
        for t in automato.transicoes
    ]
    automato.estados_finais = {
        mapeamento[e] for e in automato.estados_finais if e in mapeamento
    }
    return automato

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
        completar(resultado)
        etapas.append(
            Etapa(
                descricao="Completar autômato (estado sumidouro)",
                automato=resultado.copiar(),
            )
        )

    _inverter_finais(resultado)
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
    """Fachada para a operação de complemento (compatibilidade de chamada)."""

    @staticmethod
    def complemento(automato: AutomatoFinito) -> AutomatoFinito:
        return complemento(automato)

    @staticmethod
    def executar(automato: AutomatoFinito) -> tuple[AutomatoFinito, list[Etapa]]:
        return complemento_com_etapas(automato)
