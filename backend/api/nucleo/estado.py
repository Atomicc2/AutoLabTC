from dataclasses import dataclass


@dataclass
class Estado:
    """Representa um estado de um autômato finito."""

    nome: str
    inicial: bool = False
    final: bool = False

    def __eq__(self, outro):
        if not isinstance(outro, Estado):
            return NotImplemented
        return self.nome == outro.nome

    def __hash__(self):
        return hash(self.nome)