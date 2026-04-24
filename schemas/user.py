from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import re

def validate_cpf(v: str) -> str:
    """
    Validação rigorosa de CPF incluindo dígitos verificadores.
    """
    if not v:
        raise ValueError('CPF é obrigatório')

    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', v)

    if len(cpf) != 11:
        raise ValueError('CPF deve conter exatamente 11 números')

    if cpf == cpf[0] * 11:
        raise ValueError('CPF inválido (números repetidos)')

    # Cálculo dos dígitos
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValueError(f'CPF inválido (dígito verificador {i-8} incorreto)')

    return cpf

class UserBase(BaseModel):
    nome: str
    idade: Optional[int] = None
    email: EmailStr
    login: str
    cpf: str
    rg: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @field_validator('cpf')
    @classmethod
    def cpf_must_be_valid(cls, v: str) -> str:
        return validate_cpf(v)

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    idade: Optional[int] = None
    email: Optional[EmailStr] = None
    login: Optional[str] = None
    rg: Optional[str] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    nome: str
    idade: Optional[int]
    email: EmailStr
    login: str
    cpf: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
