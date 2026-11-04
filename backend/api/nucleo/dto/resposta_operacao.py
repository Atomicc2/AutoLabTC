"""DTO com os arquivos gerados por uma operação sobre autômatos.

Encapsula o .jff do autômato resultante e o relatório PDF com as
etapas intermediárias, e os empacota em um arquivo .zip para
download no frontend.
"""

from dataclasses import dataclass
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile


@dataclass
class RespostaOperacao:
    """Arquivos de saída de uma operação sobre autômatos.

    Atributos:
        arquivo_jff: Conteúdo XML do arquivo .jff com o autômato resultante.
        relatorio_pdf: Conteúdo binário do relatório PDF com as etapas.
    """

    arquivo_jff: str
    relatorio_pdf: bytes

    def compactar(self, nome_base: str) -> bytes:
        """Empacota os arquivos da operação em um .zip em memória.

        O .zip contém ``<nome_base>.jff`` e ``<nome_base>.pdf``.

        Args:
            nome_base: Nome, sem extensão, dos arquivos dentro do .zip
                e do próprio arquivo .zip indicado no download.

        Returns:
            Conteúdo binário do arquivo .zip gerado.
        """
        buffer = BytesIO()

        with ZipFile(buffer, "w", ZIP_DEFLATED) as zip:
            zip.writestr(f"{nome_base}.jff", self.arquivo_jff)
            zip.writestr(f"{nome_base}.pdf", self.relatorio_pdf)

        return buffer.getvalue()
