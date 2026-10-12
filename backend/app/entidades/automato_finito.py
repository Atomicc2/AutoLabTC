from copy import deepcopy
from backend.app.entidades import Estado, Transicao


class AutomatoFinito:

    def __init__(self, estados: list[Estado] | None = None, transicoes: list[Transicao] | None = None, alfabeto: set[str] | None = None):
        self.estados = []
        self.transicoes = []
        self.alfabeto = set()

        if estados is not None:
            self.estados = list(estados)

        if transicoes is not None:
            self.transicoes = list(transicoes)

        if alfabeto is not None:
            self.alfabeto = set(alfabeto)
        else:
            for transicao in self.transicoes:
                if transicao.simbolo is not None and transicao.simbolo != "":
                    self.alfabeto.add(transicao.simbolo)

    def eh_afd(self):
        vistas = set()

        for transicao in self.transicoes:
            simbolo = transicao.simbolo

            if simbolo is None or simbolo == "":
                return False

            chave = (transicao.de, simbolo)

            if chave in vistas:
                return False

            vistas.add(chave)

        return True

    def eh_completo(self):
        existentes = set()

        for transicao in self.transicoes:
            if transicao.simbolo is not None and transicao.simbolo != "":
                existentes.add((transicao.de, transicao.simbolo))

        for estado in self.estados:
            for simbolo in self.alfabeto:
                if (estado.id, simbolo) not in existentes:
                    return False

        return True