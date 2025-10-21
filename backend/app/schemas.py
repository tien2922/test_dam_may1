from pydantic import BaseModel, Field, ConfigDict

class ProductIn(BaseModel):
    sku: str
    name: str
    unit_price: float = 0.0

class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    unit_price: float
    stock: int
    created_at: str | None = None
    model_config = ConfigDict(from_attributes=True)

class SupplierIn(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None

class SupplierOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None
    created_at: str | None = None
    model_config = ConfigDict(from_attributes=True)

class MoveIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    move_type: str  # IN or OUT
    note: str | None = None

class MoveOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    move_type: str
    note: str | None = None
    created_at: str | None = None
    model_config = ConfigDict(from_attributes=True)
