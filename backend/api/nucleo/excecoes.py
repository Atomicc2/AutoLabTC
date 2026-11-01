class ErroAutomatoNaoEncontrado(Exception):
    pass


class OperacaoInvalidaError(ValueError):
    """Exceção lançada quando uma operação não pode ser aplicada ao autômato.

    Subclasse de ``ValueError`` para manter compatibilidade com código que
    captura ``ValueError``.
    """


# Alias em português
ErroOperacaoInvalida = OperacaoInvalidaError
