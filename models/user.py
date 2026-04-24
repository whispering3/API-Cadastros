from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """
    Representação da tabela de Usuários (Clientes).
    Inclui suporte a Soft Delete.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    rg = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    
    # Controle de Soft Delete
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamento: Um usuário tem muitos pedidos
    orders = relationship("Order", back_populates="owner")
