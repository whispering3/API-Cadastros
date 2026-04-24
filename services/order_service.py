from sqlalchemy.orm import Session, joinedload
from typing import List
from models.order import Order
from schemas.order import OrderCreate

def create_order(db: Session, order_in: OrderCreate, user_id: int) -> Order:
    """
    Cria um novo pedido vinculado a um usuário.
    """
    db_order = Order(
        descricao=order_in.descricao,
        user_id=user_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def list_orders(db: Session, user_id: int = None) -> List[Order]:
    """
    Lista pedidos com o nome do usuário.
    """
    query = db.query(Order).options(joinedload(Order.owner))
    if user_id:
        query = query.filter(Order.user_id == user_id)
    return query.all()

def update_order(db: Session, order_id: int, descricao: str) -> Order:
    """
    Atualiza a descrição de um pedido existente.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    db_order.descricao = descricao
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> bool:
    """
    Exclui um pedido fisicamente do banco de dados.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True
