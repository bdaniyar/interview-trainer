from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from main import add_and_flush

class Base(DeclarativeBase): pass
class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

def test_flush_without_commit():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        item = add_and_flush(session, Item())
        assert item.id is not None and session.in_transaction()
        item_id = item.id
        session.rollback()
        assert session.get(Item, item_id) is None
