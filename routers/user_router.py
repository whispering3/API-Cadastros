from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.user import UserCreate, UserOut, UserUpdate
from services import user_service
from deps import get_current_user
from models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna o perfil do usuário autenticado.
    """
    return current_user

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Cadastro de novo usuário.
    """
    return user_service.create_user(db, user_in)

@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listagem de todos os usuários (requer autenticação).
    """
    return user_service.list_users(db)

@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualização parcial ou total de dados do usuário.
    """
    return user_service.update_user(db, user_id, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    physical: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Exclusão do usuário.
    - physical=False (padrão): Exclusão lógica (Soft Delete).
    - physical=True: Exclusão física (Remove do banco).
    """
    if physical:
        user_service.hard_delete_user(db, user_id)
    else:
        user_service.soft_delete_user(db, user_id)
    return None
