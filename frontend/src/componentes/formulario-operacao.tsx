import BotaoPrincipal from './botao-principal';
import './formulario-operacao.css'
import PainelImportacao from "./importacao/painel-importacao";
import PainelSelecao from "./selecao/painel-selecao";

function FormularioOperacao() {
  return (
    <article className="formulario-operacao">
      <PainelImportacao />
      <PainelSelecao />
    </article>
  )
}

export default FormularioOperacao;