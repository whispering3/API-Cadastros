from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Engine do SQLAlchemy configurado para o PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

def get_db():
    """
    Dependency Injection para obter a sessão do banco de dados.
    Garante que a sessão seja fechada após a requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
