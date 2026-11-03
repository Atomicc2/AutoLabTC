from dataclasses import dataclass

from api.nucleo.automato_finito import AutomatoFinito
from api.nucleo.dto.etapa import Etapa

@dataclass
class ResultadoOperacaoEtapas:
    automato: AutomatoFinito
    etapas: list[Etapa]