import os
from pydantic import field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Configurações globais da aplicação.
    Utiliza Pydantic Settings para validação de variáveis de ambiente.
    """
    APP_NAME: str = "API de Cadastro de Clientes e Pedidos"
    VERSION: str = "1.0.0"
    API_STR: str = "/api/v1"
    
    # Configurações do Banco de Dados
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/api_db"
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_protocol(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v
    
    # Segurança e JWT
    SECRET_KEY: str = "7b0e4a9e5c6d3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    class Config:
        case_sensitive = True

settings = Settings()
