import os
from dotenv import load_dotenv

load_dotenv()


class Configuracao:
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave-secreta-padrao")


configuracao = Configuracao()
