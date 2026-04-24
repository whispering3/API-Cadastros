from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

# Contexto de hash para senhas usando Argon2 como padrão
# O passlib gerencia automaticamente a verificação de hashes antigos (bcrypt)
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Gera um token JWT.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha para armazenamento seguro.
    """
    return pwd_context.hash(password)
