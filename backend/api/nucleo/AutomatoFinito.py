import copy
from dataclasses import dataclass, field

from api.nucleo.Estado import Estado
from api.nucleo.Transicao import Transicao


@dataclass
class AutomatoFinito:
    """Agrega estados, alfabeto, transições e estados inicial/finais de um autômato."""

    estados: set[Estado] = field(default_factory=set)
    alfabeto: set[str] = field(default_factory=set)
    transicoes: list[Transicao] = field(default_factory=list)
    estado_inicial: Estado | None = None
    estados_finais: set[Estado] = field(default_factory=set)

    def adicionar_estado(self, estado: Estado) -> None:
        self.estados.add(estado)

    def adicionar_transicao(self, transicao: Transicao) -> None:
        self.transicoes.append(transicao)

    def obter_estado_inicial(self) -> Estado | None:
        return self.estado_inicial

    def validar(self) -> None:
        """Verifica a consistência do autômato; lança ValueError se inválido."""
        if self.estado_inicial is None or self.estado_inicial not in self.estados:
            raise ValueError(
                "Estado inicial ausente ou inexistente no conjunto de estados."
            )
        if not self.estados_finais.issubset(self.estados):
            raise ValueError(
                "Existem estados finais que não pertencem ao conjunto de estados."
            )
        for t in self.transicoes:
            if t.origem not in self.estados or t.destino not in self.estados:
                raise ValueError("Transição referencia estado inexistente.")
            if t.simbodo is not None and t.simbodo not in self.alfabeto:
                raise ValueError(f"Símbodo '{t.simbodo}' não pertence ao alfabeto.")

    def copiar(self) -> "AutomatoFinito":
        """Retorna uma cópia profunda do autômato."""
        return copy.deepcopy(self)

    def eh_afd(self) -> bool:
        """Verifica se o autômato é determinístico.

        Um AFD não possui transições épsilon (``simbodo is None``) e não possui
        duas transições com a mesma origem e o mesmo símbodo.
        """
        if self.estado_inicial is None:
            return False
        vistos: set[tuple[Estado, str | None]] = set()
        for transicao in self.transicoes:
            if transicao.simbodo is None:
                return False
            chave = (transicao.origem, transicao.simbodo)
            if chave in vistos:
                return False
            vistos.add(chave)
        return True

    def eh_completo(self) -> bool:
        """Verifica se o autômato é completo (toda origem tem transição para
        todo símbodo do alfabeto)."""
        existentes: set[tuple[Estado, str | None]] = set()
        for transicao in self.transicoes:
            if transicao.simbodo is not None:
                existentes.add((transicao.origem, transicao.simbodo))
        for estado in self.estados:
            for simbodo in self.alfabeto:
                if (estado, simbodo) not in existentes:
                    return False
        return True
