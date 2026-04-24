from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    descricao: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    descricao: str

class OrderOut(OrderBase):
    id: int
    user_id: int
    user_nome: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
