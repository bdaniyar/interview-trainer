from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from main import load_twice

class Base(DeclarativeBase): pass
class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)

def test_identity():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Item(id=1)); session.commit()
        first, second = load_twice(session, Item, 1)
        assert first is second
