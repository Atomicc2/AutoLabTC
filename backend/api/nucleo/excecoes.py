class ErroAutomatoNaoEncontrado(Exception):
    """Exceção lançada quando um arquivo de autômato não é encontrado."""


class ErroJFFInvalido(Exception):
    """Exceção lançada quando um arquivo JFF é inválido."""


class OperacaoInvalidaError(ValueError):
    """Exceção lançada quando uma operação não pode ser aplicada ao autômato.

    Subclasse de ValueError para manter compatibilidade com código que
    captura ValueError.
    """


# Alias em português.
ErroOperacaoInvalida = OperacaoInvalidaError