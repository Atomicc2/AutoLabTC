from backend.app.entidades.estado import Estado
from backend.app.entidades.transicao import Transicao
from backend.app.erros import OperacaoInvalidaError

OPERACOES = {}


def registrar(nome):
    def decorador(funcao):
        OPERACOES[nome] = funcao
        return funcao

    return decorador


def completar(automato):
    simbolos = sorted(automato.alfabeto)

    existentes = set()
    for transicao in automato.transicoes:
        if transicao.simbolo is not None and transicao.simbolo != "":
            existentes.add((transicao.de, transicao.simbolo))

    faltantes = []
    for estado in automato.estados:
        for simbolo in simbolos:
            if (estado.id, simbolo) not in existentes:
                faltantes.append((estado.id, simbolo))

    if not faltantes:
        return automato

    maior_id = max((estado.id for estado in automato.estados), default=-1)
    maior_x = max((estado.x for estado in automato.estados), default=0)
    maior_y = max((estado.y for estado in automato.estados), default=0)

    poco = Estado(maior_id + 1, "poço", False, False, maior_x + 100, maior_y)
    automato.estados.append(poco)

    for id_origem, simbolo in faltantes:
        automato.transicoes.append(Transicao(id_origem, poco.id, simbolo))

    for simbolo in simbolos:
        automato.transicoes.append(Transicao(poco.id, poco.id, simbolo))

    return automato


@registrar("complemento")
def complemento(automato_finito):
    if not automato_finito.eh_afd():
        raise OperacaoInvalidaError(
            "A operação complemento exige um AFD. O autômato informado é não determinístico."
        )

    novo = automato_finito.copiar()

    if not novo.eh_completo():
        completar(novo)

    for estado in novo.estados:
        estado.final = not estado.final

    return novo
