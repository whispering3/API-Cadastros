from pydantic import BaseModel, ConfigDict
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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
