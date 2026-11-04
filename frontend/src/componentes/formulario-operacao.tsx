import BotaoPrincipal from './botao-principal';
import './formulario-operacao.css'
import PainelImportacao from "./importacao/painel-importacao";
import PainelSelecao from "./selecao/painel-selecao";
import { useState } from "react";

interface FormOperacaoState {
  operacao: string;
  arquivo: File | null;
  enviando: boolean;
  erro: string | null;
  urlDownload: string | null;
}

function FormularioOperacao() {
  const [state, setState] = useState<FormOperacaoState>({
    operacao: "",
    arquivo: null,
    enviando: false,
    erro: null,
    urlDownload: null,
  });

  function handleSelecionarOperacao(operacao: string) {
    setState((s) => ({
      ...s,
      operacao,
      arquivo: null,
      enviando: false,
      erro: null,
      urlDownload: null,
    }));
  }

  function handleSelecionarArquivo(arquivo: File | null) {
    setState((s) => ({
      ...s,
      arquivo,
      erro: null,
      urlDownload: null,
    }));
  }

  async function handleEnviar() {
    const { operacao, arquivo, enviando } = state;
    if (!arquivo || enviando) return;

    setState((s) => ({ ...s, enviando: true, erro: null }));

    const formData = new FormData();
    formData.append("arquivo", arquivo);

    try {
      const resposta = await fetch(`/operacoes/${operacao}`, {
        method: "POST",
        body: formData,
      });

      if (!resposta.ok) {
        const texto = await resposta.text();
        setState((s) => ({ ...s, enviando: false, erro: texto }));
        return;
      }

      const blob = await resposta.blob();
      const url = URL.createObjectURL(blob);
      setState((s) => ({ ...s, enviando: false, urlDownload: url }));
    } catch (erro) {
      setState((s) => ({ ...s, enviando: false, erro: "Erro ao comunicar com o backend" }));
    }
  }

  function handleDownload() {
    const { urlDownload } = state;
    if (!urlDownload) return;

    const a = document.createElement("a");
    a.href = urlDownload;
    a.download = "complemento.zip";
    document.body.append(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(urlDownload);
    setState((s) => ({ ...s, urlDownload: null }));
  }

  return (
    <article className="formulario-operacao">
      <PainelSelecao
        valor={state.operacao}
        onSelecionar={handleSelecionarOperacao}
      />
      {state.operacao && (
        <PainelImportacao
          key={state.operacao}
          quantidadeSlots={1}
          onArquivoSelecionado={handleSelecionarArquivo}
        />
      )}
      <BotaoPrincipal
        label={state.urlDownload ? "Baixar .zip" : "Gerar Autômato"}
        disabled={state.enviando || !state.arquivo}
        onClick={state.urlDownload ? handleDownload : handleEnviar}
      />
      {state.erro && <p role="status">{state.erro}</p>}
    </article>
  );
}

export default FormularioOperacao;