from sqlalchemy import Boolean, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from main import active_users_statement

class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    active: Mapped[bool] = mapped_column(Boolean)

def test_statement():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([User(id=2, active=True), User(id=1, active=True), User(id=3, active=False)])
        session.commit()
        assert [user.id for user in session.scalars(active_users_statement(User))] == [1, 2]
