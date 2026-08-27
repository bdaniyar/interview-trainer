from sqlalchemy import select
from sqlalchemy.orm import joinedload

def orders_with_user(Order):
    return select(Order).options(joinedload(Order.user)).order_by(Order.id)
