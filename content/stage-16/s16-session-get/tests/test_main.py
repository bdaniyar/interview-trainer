from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from main import get_or_none

class Base(DeclarativeBase): pass
class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)

def test_get():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Item(id=1)); session.commit()
        assert get_or_none(session, Item, 1).id == 1
        assert get_or_none(session, Item, 2) is None
