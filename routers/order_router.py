from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas.order import OrderCreate, OrderOut, OrderUpdate
from services import order_service
from deps import get_current_user
from models.user import User

router = APIRouter()

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um pedido vinculado ao usuário autenticado.
    """
    return order_service.create_order(db, order_in, current_user.id)

@router.get("/", response_model=List[OrderOut])
def list_orders(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista pedidos com filtro opcional por usuário.
    """
    return order_service.list_orders(db, user_id)

@router.patch("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Opcional: Validar se o pedido pertence ao usuário (ou se é admin)
    updated = order_service.update_order(db, order_id, order_in.descricao)
    if not updated:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return updated

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not order_service.delete_order(db, order_id):
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": "Pedido removido com sucesso"}
