from backend.app.entidades.automato_finito import AutomatoFinito

class Operacoes:

    def complemento(self, automato_finito: AutomatoFinito) -> AutomatoFinito:
        for estado in automato_finito.estados:
            estado.final = not estado.final

        return automato_finito