import { useEffect, useState } from 'react'

import './App.css'
import { executarOperacao, listarOperacoes } from './api'

function App() {
  const [operacoes, setOperacoes] = useState<string[]>([])
  const [operacao, setOperacao] = useState('')
  const [arquivo, setArquivo] = useState<File | null>(null)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')

  useEffect(() => {
    listarOperacoes()
      .then((lista) => {
        setOperacoes(lista)
        if (lista.length > 0) {
          setOperacao(lista[0])
        }
      })
      .catch((erroAtual: Error) => setErro(erroAtual.message))
  }, [])

  async function executar() {
    if (!arquivo) {
      setErro('Selecione um arquivo .jff.')
      return
    }
    if (!operacao) {
      setErro('Selecione uma operação.')
      return
    }

    setErro('')
    setCarregando(true)

    try {
      const { blob, nomeArquivo } = await executarOperacao(operacao, arquivo)

      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = nomeArquivo
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
    } catch (erroAtual) {
      const mensagem =
        erroAtual instanceof Error ? erroAtual.message : 'Erro inesperado.'
      setErro(mensagem)
    } finally {
      setCarregando(false)
    }
  }

  return (
    <main className="container">
      <h1>AutoLab-TC</h1>
      <p className="subtitulo">Aplique operações em autômatos finitos (.jff)</p>

      <label className="campo">
        <span>Arquivo .jff</span>
        <input
          type="file"
          accept=".jff"
          onChange={(evento) => setArquivo(evento.target.files?.[0] ?? null)}
        />
      </label>

      <label className="campo">
        <span>Operação</span>
        <select
          value={operacao}
          onChange={(evento) => setOperacao(evento.target.value)}
        >
          {operacoes.map((nome) => (
            <option key={nome} value={nome}>
              {nome}
            </option>
          ))}
        </select>
      </label>

      <button type="button" onClick={executar} disabled={carregando}>
        {carregando ? 'Executando...' : 'Executar'}
      </button>

      {erro && <p className="erro">{erro}</p>}
    </main>
  )
}

export default App
