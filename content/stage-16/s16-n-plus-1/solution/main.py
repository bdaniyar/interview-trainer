from sqlalchemy import select
from sqlalchemy.orm import selectinload

def users_with_roles(User):
    return select(User).options(selectinload(User.roles)).order_by(User.id)
