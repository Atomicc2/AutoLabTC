class Estado:
    
  def __init__(self, id: int, nome: str, inicial: bool = False, final: bool = False, x: int = 0, y: int = 0):
      self.id = id
      self.nome = nome
      self.inicial = inicial
      self.final = final
      self.x = x
      self.y = y
