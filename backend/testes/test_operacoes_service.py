from api.servicos.operacoes_service import complemento

def test_complemento(tmp_path):
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

    arquivo_entrada = tmp_path / "automato.jff"
    arquivo_saida = tmp_path / "complemento.jff"

    arquivo_entrada.write_text(jff, encoding="utf-8")

    resultado = complemento(str(arquivo_entrada), str(arquivo_saida))

    assert isinstance(resultado, str)
    assert arquivo_saida.exists()
    assert arquivo_saida.read_text(encoding="utf-8").strip()

    print("\nJFF resultante:")
    print(resultado)