from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from main import orders_with_user

class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()

def test_detached_scalar():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Order(id=1, user=User(id=1))); session.commit()
        orders = session.scalars(orders_with_user(Order)).all()
        session.expunge_all()
        assert orders[0].user.id == 1
