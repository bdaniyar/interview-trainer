from sqlalchemy import create_engine, inspect
from main import Base, User

def test_schema():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    columns = inspect(engine).get_columns("users")
    assert {column["name"] for column in columns} == {"id", "email", "active"}
    assert User.__table__.c.email.unique is True and User.__table__.c.email.index is True
