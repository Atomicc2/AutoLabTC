from api.nucleo.operacao.complemento import complemento as complemento_afd
from api.nucleo.utilitario.utilitarios_jff import converter_automato_para_jff, converter_jff_para_automato

def complemento(jff: str) -> str:
  automato = converter_jff_para_automato(jff)

  resultado = complemento_afd(automato)

  return converter_automato_para_jff(resultado.automato_final)