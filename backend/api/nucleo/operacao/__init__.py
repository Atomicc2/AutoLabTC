"""Pacote de operações sobre autômatos finitos."""

from api.nucleo.operacao.complemento import (
    Complemento,
    Etapa,
    complemento,
    complemento_com_etapas,
    completar,
)

__all__ = [
    "Complemento",
    "Etapa",
    "complemento",
    "complemento_com_etapas",
    "completar",
]
