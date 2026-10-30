import { useState } from 'react'
import type { ChangeEvent } from 'react'
import { ErroImportacao, enviarJff } from '../servicos/automatos'

const TAMANHO_MAXIMO_BYTES = 2 * 1024 * 1024
const EXTENSAO_PERMITIDA = '.jff'

export interface EstadoDoComponente {
  nomeArquivo: string
  mensagem: string
  selecionarArquivo: (evento: ChangeEvent<HTMLInputElement>) => void
}

function useImportarJff(): EstadoDoComponente {
  const [importando, setImportando] = useState(false)
  const [nomeArquivo, setNomeArquivo] = useState('')
  const [mensagem, setMensagem] = useState('')

  function selecionarArquivo(evento: ChangeEvent<HTMLInputElement>): void {
    const arquivo = evento.target.files?.[0]
    evento.target.value = ''
    if (!arquivo || importando) return

    if (!arquivo.name.toLowerCase().endsWith(EXTENSAO_PERMITIDA)) {
      setNomeArquivo('')
      setMensagem(`"${arquivo.name}" não é um arquivo .jff. Escolha um arquivo gerado no JFLAP.`)
      return
    }

    if (arquivo.size > TAMANHO_MAXIMO_BYTES) {
      setNomeArquivo('')
      setMensagem(`"${arquivo.name}" é maior que 2 MB. Escolha um arquivo menor.`)
      return
    }

    setNomeArquivo('')
    setMensagem(`Importando "${arquivo.name}"…`)
    setImportando(true)

    void enviarJff(arquivo)
      .then(() => {
        setImportando(false)
        setMensagem('')
        setNomeArquivo(arquivo.name)
      })
      .catch((erro: unknown) => {
        setImportando(false)
        setNomeArquivo('')
        setMensagem(erro instanceof ErroImportacao ? erro.message : 'Ocorreu um erro inesperado. Tente novamente.')
      })
  }

  return { nomeArquivo, mensagem, selecionarArquivo }
}

export default useImportarJff
