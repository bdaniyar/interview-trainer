from sqlalchemy import select

def orders_for_email(User, Order, email):
    return select(Order).join(User).where(User.email == email).order_by(Order.id)
