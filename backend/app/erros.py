class ErroDeDominio(Exception):
    status = 400

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


class ArquivoInvalidoError(ErroDeDominio):
    status = 400


class OperacaoNaoEncontradaError(ErroDeDominio):
    status = 404


class OperacaoInvalidaError(ErroDeDominio):
    status = 422
