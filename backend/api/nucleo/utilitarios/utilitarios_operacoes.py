class UtilitariosOperacoes:

  # Método completar()
  # Completa autômato adicionando um estado sumidouro (poço) e as
  # transições ausentes, quando necessário.

  # Se o autômato já for completo, nenhum estado é adicionado. Retorna o
  # próprio autômato (mutado).
  @staticmethod
  def completar(automato: AutomatoFinito) -> AutomatoFinito:

    simbodos = sorted(automato.alfabeto)

    existentes: set[tuple[Estado, str | None]] = set()
    for transicao in automato.transicoes:
        if transicao.simbodo is not None:
            existentes.add((transicao.origem, transicao.simbodo))

    faltantes: list[tuple[Estado, str]] = []
    for estado in automato.estados:
        for simbodo in simbodos:
            if (estado, simbodo) not in existentes:
                faltantes.append((estado, simbodo))

    if not faltantes:
        return automato

    # Garante nome único para o estado sumidouro.
    nome_poco = "poço"
    nomes_existentes = {estado.nome for estado in automato.estados}
    if nome_poco in nomes_existentes:
        sufixo = 1
        while f"{nome_poco}_{sufixo}" in nomes_existentes:
            sufixo += 1
        nome_poco = f"{nome_poco}_{sufixo}"

    poco = Estado(nome_poco, inicial=False, final=False)
    automato.adicionar_estado(poco)

    for estado_origem, simbodo in faltantes:
        automato.adicionar_transicao(
            Transicao(origem=estado_origem, simbodo=simbodo, destino=poco)
        )

    for simbodo in simbodos:
        automato.adicionar_transicao(
            Transicao(origem=poco, simbodo=simbodo, destino=poco)
        )


  # Método _inverter_finais()
  # Inverte estados finais e não finais de autômato (in place).
  @staticmethod
  def inverter_finais(automato: AutomatoFinito) -> AutomatoFinito:
      
      mapeamento: dict[Estado, Estado] = {}
      
      novos_estados: set[Estado] = set()
      
      for estado in automato.estados:
          novo = Estado(
              nome=estado.nome,
              inicial=estado.inicial,
              final=not estado.final,
          )
          mapeamento[estado] = novo
          novos_estados.add(novo)

      automato.estados = novos_estados
      
      if automato.estado_inicial is not None:
          automato.estado_inicial = mapeamento[automato.estado_inicial]

      automato.transicoes = [
          Transicao(
              origem=mapeamento[t.origem],
              simbodo=t.simbodo,
              destino=mapeamento[t.destino],
          )
          for t in automato.transicoes
      ]
      
      automato.estados_finais = {
          mapeamento[e] for e in automato.estados_finais if e in mapeamento
      }