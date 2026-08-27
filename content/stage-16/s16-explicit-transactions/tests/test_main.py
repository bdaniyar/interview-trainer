import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from main import transfer

class Base(DeclarativeBase): pass
class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column()

def test_transfer_and_failure():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        source, target = Account(id=1, balance=10), Account(id=2, balance=0)
        session.add_all([source, target]); session.commit()
        transfer(session, source, target, 4)
        assert (source.balance, target.balance) == (6, 4)
        session.rollback()
        with pytest.raises(ValueError): transfer(session, source, target, 20)
        session.refresh(source); session.refresh(target)
        assert (source.balance, target.balance) == (6, 4)
