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
