import './painel-selecao.css'

interface PainelSelecaoProps {
  valor: string;
  onSelecionar: (valor: string) => void;
}

function PainelSelecao({ valor, onSelecionar }: PainelSelecaoProps) {
  return (
    <section className="painel-selecao">
      <h2>Operações</h2>

      <div className="botao-selecao">
        <select name="selecao" id="selecao" value={valor} onChange={(e) => onSelecionar(e.target.value)}>
          <option value="">Selecionar Operação</option>
          <option value="complemento">Complemento</option>
        </select>
      </div>

    </section>
  )
}

export default PainelSelecao;