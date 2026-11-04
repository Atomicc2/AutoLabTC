import "./painel-importacao.css";
import { useState } from "react";
import type { ChangeEvent } from "react";
import BotaoImportarJff from "./botao-importar-jff";

const TAMANHO_MAXIMO_BYTES = 1024 * 1024; // 1MB
const EXTENSAO_PERMITIDA = ".jff";

interface SlotImportacao {
  arquivo: File | null;
  erro: string | null;
}

function criarSlot(): SlotImportacao {
  return { arquivo: null, erro: null };
}

function validarArquivo(arquivo: File): string | null {
  if (!arquivo.name.toLowerCase().endsWith(EXTENSAO_PERMITIDA)) {
    return `"${arquivo.name}" não é um arquivo .jff.`;
  }

  if (arquivo.size > TAMANHO_MAXIMO_BYTES) {
    return `"${arquivo.name}" é maior que 1 MB.`;
  }

  return null;
}

interface PainelImportacaoProps {
  quantidadeSlots: number;
  onArquivoSelecionado?: (arquivo: File | null) => void;
}

function PainelImportacao({ quantidadeSlots, onArquivoSelecionado }: PainelImportacaoProps) {
  const slotsIniciais = Array.from({ length: quantidadeSlots }, criarSlot);
  const [slots, setSlots] = useState<SlotImportacao[]>(slotsIniciais);

  function selecionar(
    posicao: number,
    evento: ChangeEvent<HTMLInputElement>,
  ): void {
    const arquivo = evento.target.files?.[0] ?? null;
    evento.target.value = "";

    if (!arquivo) {
      onArquivoSelecionado?.(null);
      return;
    }

    const erro = validarArquivo(arquivo);
    setSlots((slotsAtuais) =>
      slotsAtuais.map((slot, indice) =>
        indice === posicao ? { arquivo: erro ? null : arquivo, erro } : slot,
      ),
    );
    onArquivoSelecionado?.(erro ? null : arquivo);
  }

  return (
    <section className="painel-importacao">
      <ul>
        {slots.map((slot, posicao) => (
          <li key={posicao}>
            <h2>Autômato {posicao + 1}</h2>
            <BotaoImportarJff
              arquivo={slot.arquivo}
              onSelecionar={(evento) => selecionar(posicao, evento)}
            />
            {slot.erro && <p role="status">{slot.erro}</p>}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default PainelImportacao;