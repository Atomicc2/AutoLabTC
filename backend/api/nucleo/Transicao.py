from dataclasses import dataclass

from api.nucleo.Estado import Estado


@dataclass(frozen=True)
class Transicao:
    """Representa uma transição de um autômato finito.

    simbodo=None representa uma transição épsilon (AFN).
    """

    origem: Estado
    simbodo: str | None
    destino: Estado
