from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Order(Base):
    """
    Representação da tabela de Pedidos.
    Vinculada obrigatoriamente a um Usuário.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Key apontando para o usuário autenticado
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relacionamento: O pedido pertence a um usuário
    owner = relationship("User", back_populates="orders")
