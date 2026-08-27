from decimal import Decimal
import pytest
from pydantic import ValidationError
from main import Product

def test_valid(): assert Product(sku="ABC-1234", price="10.50", quantity=0).price == Decimal("10.50")
@pytest.mark.parametrize(("field", "value"), [("sku", "bad"), ("price", 0), ("quantity", -1)])
def test_invalid(field, value):
    data = {"sku": "ABC-1234", "price": "1", "quantity": 1}
    data[field] = value
    with pytest.raises(ValidationError): Product(**data)
