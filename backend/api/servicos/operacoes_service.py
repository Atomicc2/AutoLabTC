from api.nucleo.operacao.complemento import complemento as complemento_afd
from api.nucleo.utilitario.utilitarios_jff import converter_automato_para_jff, converter_jff_para_automato
from pathlib import Path

def complemento(jff: str, caminho_saida: str | Path) -> str:
    automato = converter_jff_para_automato(jff)

    resultado = complemento_afd(automato)

    caminho = converter_automato_para_jff(
        resultado.automato_final,
        caminho_saida
    )

    return caminho.read_text(encoding="utf-8")