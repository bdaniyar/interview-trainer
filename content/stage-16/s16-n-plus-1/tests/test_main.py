from sqlalchemy import ForeignKey, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from main import users_with_roles

class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    roles: Mapped[list["Role"]] = relationship()
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

def test_two_queries():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([User(id=1, roles=[Role(id=1)]), User(id=2, roles=[Role(id=2)])])
        session.commit()
        calls = []
        event.listen(engine, "before_cursor_execute", lambda *args: calls.append(1))
        users = session.scalars(users_with_roles(User)).all()
        assert [len(user.roles) for user in users] == [1, 1]
        assert len(calls) == 2
