import './painel-selecao.css'
import setaBotaoSelect from '../../assets/seta-botao-select.svg'

function PainelSelecao() {
  return (
    <section className="painel-selecao">
      <h2>Operações</h2>

      <div className="botao-selecao">
        
        <select name="selecao" id="selecao">
          <option value="">Selecionar Operação</option>
          <option value="complemento">Complemento</option>
          <option value="klenee">Fecho de Klenee (estrela)</option>
          <option value="uniao">União</option>
          <option value="interseccao">Intersecção</option>
          <option value="concatenacao">Concatenação</option>
          <option value="diferenca">Diferença</option>
        </select>
      </div>

    </section>
  )
}

export default PainelSelecao;