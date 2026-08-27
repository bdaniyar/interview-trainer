from decimal import Decimal
from pydantic import BaseModel, Field

class Product(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{3}-[0-9]{4}$")
    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0)
