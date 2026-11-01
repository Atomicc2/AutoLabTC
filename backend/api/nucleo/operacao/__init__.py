"""Pacote de operações sobre autômatos finitos."""

from api.nucleo.operacao.Complemento import (
    Complemento,
    Etapa,
    complemento,
    complemento_com_etapas,
    completar,
    eh_afd,
    eh_completo,
)

__all__ = [
    "Complemento",
    "Etapa",
    "complemento",
    "complemento_com_etapas",
    "completar",
    "eh_afd",
    "eh_completo",
]
