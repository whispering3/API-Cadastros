from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str, active_only: bool = True) -> Optional[User]:
    query = db.query(User).filter(User.email == email)
    if active_only:
        query = query.filter(User.is_active == True)
    return query.first()

def get_user_by_login(db: Session, login: str, active_only: bool = True) -> Optional[User]:
    query = db.query(User).filter(User.login == login)
    if active_only:
        query = query.filter(User.is_active == True)
    return query.first()

def get_user_by_cpf(db: Session, cpf: str, active_only: bool = True) -> Optional[User]:
    query = db.query(User).filter(User.cpf == cpf)
    if active_only:
        query = query.filter(User.is_active == True)
    return query.first()

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Cria um novo usuário com senha hasheada.
    """
    if get_user_by_email(db, user_in.email, active_only=False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O e-mail informado já está cadastrado (mesmo que inativo)."
        )
    
    if get_user_by_login(db, user_in.login, active_only=False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O login informado já está cadastrado."
        )
    
    if get_user_by_cpf(db, user_in.cpf, active_only=False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O CPF informado já está cadastrado."
        )

    db_user = User(
        nome=user_in.nome,
        idade=user_in.idade,
        email=user_in.email,
        login=user_in.login,
        cpf=user_in.cpf,
        rg=user_in.rg,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def list_users(db: Session) -> List[User]:
    """
    Lista apenas usuários ativos (não deletados logicamente).
    """
    return db.query(User).filter(User.is_active == True).all()

def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
    """
    Atualização parcial ou total de dados.
    """
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def soft_delete_user(db: Session, user_id: int) -> bool:
    """
    Realiza a exclusão lógica do usuário.
    """
    db_user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db_user.is_active = False
    db_user.deleted_at = datetime.utcnow()
    db.commit()
    return True

def hard_delete_user(db: Session, user_id: int) -> bool:
    """
    Realiza a exclusão física do usuário do banco de dados.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Autentica o usuário validando o e-mail ou login e a senha.
    """
    # Tenta buscar por e-mail
    user = get_user_by_email(db, username)
    
    # Se não encontrar por e-mail, tenta por login
    if not user:
        user = get_user_by_login(db, username)
        
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
