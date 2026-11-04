import './painel-selecao.css'

function PainelSelecao() {
  return (
    <section className="painel-selecao">
      <h2>Operações</h2>

      <div className="botao-selecao">
        <select name="selecao" id="selecao">
          <option value="" selected disabled>Selecionar Operação</option>
          <option value="complemento">Complemento</option>
        </select>
      </div>

    </section>
  )
}

export default PainelSelecao;