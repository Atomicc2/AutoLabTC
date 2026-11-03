from dataclasses import dataclass

from api.nucleo.AutomatoFinito import AutomatoFinito


# Representa uma etapa intermediária de uma operação sobre autômato.

# Atributos:
#     descricao: Descrição textual da etapa.
#     automato: Cópia do autômato no estado correspondente à etapa.

@dataclass
class Etapa:
    descricao: str
    automato: AutomatoFinito