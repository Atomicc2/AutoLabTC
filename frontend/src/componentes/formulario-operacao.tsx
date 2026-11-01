import './formulario-operacao.css'
import PainelImportacao from "./importacao/painel-importacao";
import PainelSelecao from "./selecao/painel-selecao";

function FormularioOperacao() {
  return (
    <section className="formulario-operacao">
      <PainelImportacao />
      <PainelSelecao />
    </section>
  )
}

export default FormularioOperacao;