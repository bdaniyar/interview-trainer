from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from main import orders_for_email

class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String)
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()

def test_join():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        a, b = User(id=1, email="a"), User(id=2, email="b")
        session.add_all([a, b, Order(id=2, user=a), Order(id=1, user=a), Order(id=3, user=b)])
        session.commit()
        assert [order.id for order in session.scalars(orders_for_email(User, Order, "a"))] == [1, 2]
