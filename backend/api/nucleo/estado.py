from dataclasses import dataclass


@dataclass(frozen=True)
class Estado:
    """Representa um estado de um autômato finito."""

    nome: str
    inicial: bool = False
    final: bool = False
