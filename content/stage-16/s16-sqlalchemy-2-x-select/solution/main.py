from sqlalchemy import select

def active_users_statement(User):
    return select(User).where(User.active.is_(True)).order_by(User.id)
