import './botao-importar-jff.css'
import nuvemImportar from '../../assets/nuvem-importar-arquivo.svg'
import { useRef } from 'react'
import type { ChangeEvent } from 'react'

interface BotaoImportarJffProps {
  arquivo: File | null;
  onSelecionar: (evento: ChangeEvent<HTMLInputElement>) => void;
}

const LIMITE_NOME = "Selecionar Arquivo".length

function truncarNome(nome: string): string {
  return nome.length <= LIMITE_NOME ? nome : `${nome.slice(0, LIMITE_NOME - 6)}...`
}

function BotaoImportarJff({ arquivo, onSelecionar }: BotaoImportarJffProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  return (
    <div className="botao-importar">
      <input
        ref={inputRef}
        type="file"
        accept=".jff"
        onChange={onSelecionar}
        hidden
      />
      <button
        type="button"
        title={arquivo?.name}
        onClick={() => inputRef.current?.click()}
      >
        <span>{arquivo ? truncarNome(arquivo.name) : 'Selecionar Arquivo'}</span>
        <img src={nuvemImportar} alt="" aria-hidden="true" width="30" height="29" />
      </button>
    </div>
  )
}

export default BotaoImportarJff
