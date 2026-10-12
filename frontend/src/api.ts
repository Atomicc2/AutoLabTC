const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function listarOperacoes(): Promise<string[]> {
  const resposta = await fetch(`${API_URL}/operacoes`)

  if (!resposta.ok) {
    throw new Error('Não foi possível carregar as operações disponíveis.')
  }

  return resposta.json()
}

export async function executarOperacao(nome: string, arquivo: File) {
  const dados = new FormData()
  dados.append('arquivo', arquivo)

  const resposta = await fetch(`${API_URL}/operacoes/${nome}`, {
    method: 'POST',
    body: dados,
  })

  if (!resposta.ok) {
    let mensagem = 'Ocorreu um erro ao executar a operação.'
    try {
      const corpo = await resposta.json()
      if (corpo && corpo.detail) {
        mensagem = corpo.detail
      }
    } catch {
      // mantém a mensagem padrão
    }
    throw new Error(mensagem)
  }

  const blob = await resposta.blob()
  const disposicao = resposta.headers.get('Content-Disposition') ?? ''
  const casamento = disposicao.match(/filename="?([^";]+)"?/)
  const nomeArquivo = casamento ? casamento[1] : `resultado_${nome}.jff`

  return { blob, nomeArquivo }
}
