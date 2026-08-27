import pytest
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from main import persist

class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)

def test_rollback_keeps_session_usable():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        persist(session, User(id=1, email="a"))
        with pytest.raises(IntegrityError): persist(session, User(id=2, email="a"))
        assert session.scalar(select(User).where(User.id == 1)).email == "a"
