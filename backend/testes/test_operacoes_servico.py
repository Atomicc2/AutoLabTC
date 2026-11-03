from api.nucleo.utilitario.utilitarios_jff import converter_jff_para_automato
from api.servicos.operacoes_servico import complemento

def test_complemento():
    jff = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <structure>
        <type>fa</type>
        <automaton>
            <state id="0" name="q0">
                <x>100</x>
                <y>100</y>
                <initial/>
                <final/>
            </state>
            <state id="1" name="q1">
                <x>200</x>
                <y>100</y>
            </state>
            <transition>
                <from>0</from>
                <to>1</to>
                <read>a</read>
            </transition>
        </automaton>
    </structure>
    """

    resultado = complemento(jff)

    assert isinstance(resultado, str)
    assert resultado.strip()

    automato = converter_jff_para_automato(resultado)

    assert automato.eh_afd()