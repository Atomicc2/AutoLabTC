from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.estado import Estado
from api.nucleo.excecoes import OperacaoInvalidaError
from api.nucleo.transicao import Transicao

def completar(automato: AutomatoFinito) -> None:
    """
    Completa o autômato adicionando um estado sumidouro (poço)
    e as transições ausentes, quando necessário.

    Se o autômato já for completo, nenhuma alteração é realizada.
    Modifica o próprio autômato (in-place).
    """

    simbolos = sorted(automato.alfabeto)

    existentes: set[tuple[Estado, str | None]] = set()
    for transicao in automato.transicoes:
        if transicao.simbodo is not None:
            existentes.add((transicao.origem, transicao.simbodo))

    faltantes: list[tuple[Estado, str]] = []
    for estado in automato.estados:
        for simbodo in simbolos:
            if (estado, simbodo) not in existentes:
                faltantes.append((estado, simbodo))

    if not faltantes:
        return

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

    for simbodo in simbolos:
        automato.adicionar_transicao(
            Transicao(origem=poco, simbodo=simbodo, destino=poco)
        )

def inverter_finais(automato: AutomatoFinito) -> None:
    """
    Inverte os estados finais e não finais do autômato.

    Exige um AFD.
    Modifica o próprio autômato (in-place).
    """
    if not automato.eh_afd():
        raise OperacaoInvalidaError(
            "A operação complemento exige um AFD. "
            "O autômato informado é não determinístico; converta-o para AFD antes."
        )

    for estado in automato.estados:
        estado.final = not estado.final

    automato.estados_finais = {
        estado for estado in automato.estados if estado.final
    }