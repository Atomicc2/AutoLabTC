import './botao-importar-jff.css'
import nuvemImportar from '../assets/nuvem-importar-arquivo.svg'

function BotaoImportarJff() {
  // const { nomeArquivo, mensagem, selecionarArquivo } = useImportarJff()

  return (
    //eu vi que label pode ser melhor quando se trabalha com o javascript
    //como estamos usando react htmlfor é o ideal ao invés de for
    <div>

    <label className= "botao-upload" htmlFor="arquivoAutomato">
        <strong>Selecionar Arquivo</strong>
        <img src={nuvemImportar} alt="icone de upload de arquivo"/>
    </label>
    
    <input type ="file" id= "arquivoAutomato"/>

    </div>
  )
}

export default BotaoImportarJff
