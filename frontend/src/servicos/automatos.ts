import type { ErroApi, RespostaImportacaoJff } from '../tipos/importacao'

export const URL_IMPORTAR_JFF = '/automatos/importar'

export class ErroImportacao extends Error {
  constructor(mensagem: string) {
    super(mensagem)
    this.name = 'ErroImportacao'
  }
}

export async function enviarJff(arquivo: File): Promise<RespostaImportacaoJff> {
  const formulario = new FormData()
  formulario.append('arquivo', arquivo)

  let resposta: Response
  try {
    resposta = await fetch(URL_IMPORTAR_JFF, {
      method: 'POST',
      body: formulario,
    })
  } catch {
    throw new ErroImportacao('Não foi possível conectar ao servidor. Verifique se o back-end está rodando.')
  }

  if (!resposta.ok) {
    throw new ErroImportacao(await extrairMensagemErro(resposta))
  }

  return (await resposta.json().catch(() => ({}))) as RespostaImportacaoJff
}

async function extrairMensagemErro(resposta: Response): Promise<string> {
  try {
    const corpo = (await resposta.json()) as ErroApi
    if (typeof corpo.detalhe === 'string') return corpo.detalhe
    if (typeof corpo.mensagem === 'string') return corpo.mensagem
  } catch {
    // corpo sem JSON: usa mensagem genérica
  }
  return 'Ocorreu um erro ao importar o arquivo. Tente novamente.'
}
