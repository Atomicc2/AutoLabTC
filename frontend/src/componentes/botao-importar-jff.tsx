import "./botao-importar-jff.css";
import nuvemImportar from "../assets/nuvem-importar-arquivo.svg";
import { useRef } from "react";

function BotaoImportarJff() {
  const inputRef = useRef<HTMLInputElement>(null);
  
  // const { nomeArquivo, mensagem, selecionarArquivo } = useImportarJff()

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        id="importar-jff"
        accept=".jff"
        hidden
      />

      <button
        type="button"
        className="upload-botao"
        onClick={() => inputRef.current?.click()}
      >
        <span>Selecionar Arquivo</span>
        <img src={nuvemImportar} alt="" aria-hidden="true" width="30" height="29" />
      </button>
    </div>
  );
}

export default BotaoImportarJff;
