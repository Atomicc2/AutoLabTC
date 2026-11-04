"""Utilitários para escrever texto de usuário em documentos LaTeX."""

_CARACTERES_ESPECIAIS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
    "|": r"\textbar{}",
}


def escapar_latex(texto: str) -> str:
    """Escapa os caracteres que têm significado especial em LaTeX.

    Nomes de estados e símbolos vêm de arquivos ``.jff`` e, por isso, não
    podem ser inseridos diretamente no documento.
    """
    return "".join(
        _CARACTERES_ESPECIAIS.get(caractere, caractere) for caractere in texto
    )
