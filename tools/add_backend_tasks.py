"""Add FastAPI, Pydantic, SQLAlchemy and Alembic executable mini-tasks."""

from __future__ import annotations

from add_coding_tasks import Task, indexes, write_task


FRAMEWORK_TASKS = [
    Task(
        "14.2", "Health route", "Создай FastAPI app с GET /health → 200 и JSON status=ok.",
        """from fastapi import FastAPI

app = FastAPI()
# Добавь route.
""",
        """from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
""",
        """from fastapi.testclient import TestClient
from main import app

def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
""", ("fastapi", "routing"),
    ),
    Task(
        "14.3", "Validated path parameter", "GET /users/{user_id}: user_id >= 1; valid response содержит user_id, invalid даёт 422.",
        """from fastapi import FastAPI

app = FastAPI()
# Добавь endpoint.
""",
        """from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: Annotated[int, Path(ge=1)]):
    return {"user_id": user_id}
""",
        """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_valid(): assert client.get("/users/7").json() == {"user_id": 7}
def test_invalid(): assert client.get("/users/0").status_code == 422
""", ("fastapi", "path-parameter"),
    ),
    Task(
        "14.4", "Pagination query", "GET /items: offset >= 0, limit 1..100; defaults 0/20; верни оба значения.",
        """from fastapi import FastAPI

app = FastAPI()
# Добавь endpoint.
""",
        """from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
def items(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return {"offset": offset, "limit": limit}
""",
        """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_defaults(): assert client.get("/items").json() == {"offset": 0, "limit": 20}
def test_values(): assert client.get("/items?offset=5&limit=10").json() == {"offset": 5, "limit": 10}
def test_invalid(): assert client.get("/items?limit=0").status_code == 422
""", ("fastapi", "query-parameter"),
    ),
    Task(
        "14.5", "Validated request body", "Создай BookingCreate(room_id > 0, guests 1..8) и POST /bookings → 201.",
        """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# Добавь model и endpoint.
""",
        """from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class BookingCreate(BaseModel):
    room_id: int = Field(gt=0)
    guests: int = Field(ge=1, le=8)

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate):
    return payload
""",
        """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_created():
    response = client.post("/bookings", json={"room_id": 2, "guests": 3})
    assert response.status_code == 201
    assert response.json() == {"room_id": 2, "guests": 3}
def test_invalid(): assert client.post("/bookings", json={"room_id": 0, "guests": 9}).status_code == 422
""", ("fastapi", "request-body"),
    ),
    Task(
        "14.6", "Не раскрыть secret", "UserPublic response_model для GET /users/me должен удалить password_hash из handler result.",
        """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
# Добавь response model и endpoint.
""",
        """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserPublic(BaseModel):
    id: int
    email: str

@app.get("/users/me", response_model=UserPublic)
def me():
    return {"id": 1, "email": "a@example.com", "password_hash": "secret"}
""",
        """from fastapi.testclient import TestClient
from main import app

def test_secret_filtered():
    assert TestClient(app).get("/users/me").json() == {"id": 1, "email": "a@example.com"}
""", ("fastapi", "response-model", "security"),
    ),
    Task(
        "14.8", "Authorization dependency", "require_admin читает X-Role: не admin → 403; GET /admin использует Depends.",
        """from fastapi import FastAPI

app = FastAPI()
# Добавь dependency и endpoint.
""",
        """from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def require_admin(x_role: Annotated[str | None, Header()] = None):
    if x_role != "admin":
        raise HTTPException(403, "admin role required")
    return x_role

@app.get("/admin")
def admin(role: Annotated[str, Depends(require_admin)]):
    return {"role": role}
""",
        """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_denied(): assert client.get("/admin").status_code == 403
def test_allowed(): assert client.get("/admin", headers={"X-Role": "admin"}).json() == {"role": "admin"}
""", ("fastapi", "depends", "authorization"),
    ),
    Task(
        "14.10", "Yield dependency cleanup", "get_resource пишет open/close в events; GET /resource получает yielded db.",
        """from fastapi import FastAPI

app = FastAPI()
events = []
# Добавь yield dependency и endpoint.
""",
        """from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()
events = []

def get_resource():
    events.append("open")
    try:
        yield "db"
    finally:
        events.append("close")

@app.get("/resource")
def resource(value: Annotated[str, Depends(get_resource)]):
    return {"resource": value}
""",
        """from fastapi.testclient import TestClient
from main import app, events

def test_cleanup():
    events.clear()
    response = TestClient(app).get("/resource")
    assert response.json() == {"resource": "db"}
    assert events == ["open", "close"]
""", ("fastapi", "yield-dependency"),
    ),
    Task(
        "14.12", "Domain exception handler", "DomainConflict handler возвращает status 409 и JSON error; GET /conflict поднимает already booked.",
        """from fastapi import FastAPI

app = FastAPI()
# Добавь exception, handler и endpoint.
""",
        """from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class DomainConflict(Exception):
    pass

@app.exception_handler(DomainConflict)
def handle_conflict(request: Request, exc: DomainConflict):
    return JSONResponse({"error": str(exc)}, status_code=409)

@app.get("/conflict")
def conflict():
    raise DomainConflict("already booked")
""",
        """from fastapi.testclient import TestClient
from main import app

def test_handler():
    response = TestClient(app).get("/conflict")
    assert response.status_code == 409
    assert response.json() == {"error": "already booked"}
""", ("fastapi", "exception-handler"),
    ),
    Task(
        "14.13", "Request-ID middleware", "Response X-Request-ID равен входному header либо новому UUID; GET /ping возвращает pong.",
        """from fastapi import FastAPI

app = FastAPI()
# Добавь middleware и endpoint.
""",
        """from uuid import uuid4
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def request_id(request: Request, call_next):
    value = request.headers.get("X-Request-ID") or str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = value
    return response

@app.get("/ping")
def ping():
    return {"pong": True}
""",
        """from uuid import UUID
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_preserves(): assert client.get("/ping", headers={"X-Request-ID": "abc"}).headers["X-Request-ID"] == "abc"
def test_generates(): UUID(client.get("/ping").headers["X-Request-ID"])
""", ("fastapi", "middleware"),
    ),
    Task(
        "15.1", "UserCreate model", "Pydantic UserCreate: username min_length=3, age 14..120.",
        """from pydantic import BaseModel

# Создай UserCreate.
""",
        """from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    age: int = Field(ge=14, le=120)
""",
        """import pytest
from pydantic import ValidationError
from main import UserCreate

def test_valid(): assert UserCreate(username="aida", age=18).model_dump() == {"username": "aida", "age": 18}
@pytest.mark.parametrize("data", [{"username": "ab", "age": 18}, {"username": "aida", "age": 13}])
def test_invalid(data):
    with pytest.raises(ValidationError): UserCreate(**data)
""", ("pydantic-v2", "validation"),
    ),
    Task(
        "15.3", "Constrained Product", "Product: sku ABC-1234 pattern, Decimal price > 0, quantity >= 0.",
        """from pydantic import BaseModel

# Создай Product.
""",
        """from decimal import Decimal
from pydantic import BaseModel, Field

class Product(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{3}-[0-9]{4}$")
    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0)
""",
        """from decimal import Decimal
import pytest
from pydantic import ValidationError
from main import Product

def test_valid(): assert Product(sku="ABC-1234", price="10.50", quantity=0).price == Decimal("10.50")
@pytest.mark.parametrize(("field", "value"), [("sku", "bad"), ("price", 0), ("quantity", -1)])
def test_invalid(field, value):
    data = {"sku": "ABC-1234", "price": "1", "quantity": 1}
    data[field] = value
    with pytest.raises(ValidationError): Product(**data)
""", ("pydantic-v2", "field-constraints"),
    ),
    Task(
        "15.4", "Patch semantics", "UserPatch: display_name и age можно не передать или передать null; extra fields запрещены.",
        """from pydantic import BaseModel

# Создай UserPatch.
""",
        """from pydantic import BaseModel, ConfigDict

class UserPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    display_name: str | None = None
    age: int | None = None
""",
        """import pytest
from pydantic import ValidationError
from main import UserPatch

def test_missing(): assert UserPatch().model_dump(exclude_unset=True) == {}
def test_explicit_null(): assert UserPatch(display_name=None).model_dump(exclude_unset=True) == {"display_name": None}
def test_extra():
    with pytest.raises(ValidationError): UserPatch(role="admin")
""", ("pydantic-v2", "optional-nullable"),
    ),
    Task(
        "15.5", "Nested models", "Address(city,country_code length=2) и UserProfile(id>0,address,tags с independent default list).",
        """from pydantic import BaseModel

# Создай Address и UserProfile.
""",
        """from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    country_code: str = Field(min_length=2, max_length=2)

class UserProfile(BaseModel):
    id: int = Field(gt=0)
    address: Address
    tags: list[str] = Field(default_factory=list)
""",
        """from main import UserProfile

def test_nested_and_defaults():
    first = UserProfile(id=1, address={"city": "Almaty", "country_code": "KZ"})
    second = UserProfile(id=2, address={"city": "Astana", "country_code": "KZ"})
    first.tags.append("python")
    assert first.address.city == "Almaty" and second.tags == []
""", ("pydantic-v2", "nested-model"),
    ),
    Task(
        "15.6", "Email field validator", "LoginInput.email: before validator делает strip/lower; требует ровно один @ и непустые части.",
        """from pydantic import BaseModel

# Создай LoginInput.
""",
        """from pydantic import BaseModel, field_validator

class LoginInput(BaseModel):
    email: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        value = str(value).strip().lower()
        parts = value.split("@")
        if len(parts) != 2 or not all(parts):
            raise ValueError("invalid email")
        return value
""",
        """import pytest
from pydantic import ValidationError
from main import LoginInput

def test_normalizes(): assert LoginInput(email=" A@Example.COM ").email == "a@example.com"
@pytest.mark.parametrize("value", ["no-at", "@host", "a@", "a@@b"])
def test_invalid(value):
    with pytest.raises(ValidationError): LoginInput(email=value)
""", ("pydantic-v2", "field-validator"),
    ),
    Task(
        "15.7", "Cross-field validator", "BookingPeriod(start,end) с model_validator: end строго больше start.",
        """from pydantic import BaseModel

# Создай BookingPeriod.
""",
        """from pydantic import BaseModel, model_validator

class BookingPeriod(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def validate_order(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
""",
        """import pytest
from pydantic import ValidationError
from main import BookingPeriod

def test_valid(): assert BookingPeriod(start=2, end=5).end == 5
def test_invalid():
    with pytest.raises(ValidationError, match="end must be after start"):
        BookingPeriod(start=5, end=5)
""", ("pydantic-v2", "model-validator"),
    ),
]


ORM_TASKS = [
    Task(
        "16.2", "Declarative User model", "SQLAlchemy 2.x User(id,email,active): email unique+index, active default True; Mapped/mapped_column.",
        """from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Создай User.
""",
        """from sqlalchemy import Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
""",
        """from sqlalchemy import create_engine, inspect
from main import Base, User

def test_schema():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    columns = inspect(engine).get_columns("users")
    assert {column["name"] for column in columns} == {"id", "email", "active"}
    assert User.__table__.c.email.unique is True and User.__table__.c.email.index is True
""", ("sqlalchemy-2", "declarative"),
    ),
    Task(
        "16.4", "Session identity map", "load_twice делает два Session.get и возвращает tuple; не закрывает и не commit session.",
        """def load_twice(session, model, object_id):
    raise NotImplementedError
""",
        """def load_twice(session, model, object_id):
    return session.get(model, object_id), session.get(model, object_id)
""",
        """from sqlalchemy import create_engine
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
""", ("sqlalchemy-2", "identity-map"),
    ),
    Task(
        "16.6", "SQLAlchemy select", "active_users_statement(User): select active true, order by id.",
        """def active_users_statement(User):
    raise NotImplementedError
""",
        """from sqlalchemy import select

def active_users_statement(User):
    return select(User).where(User.active.is_(True)).order_by(User.id)
""",
        """from sqlalchemy import Boolean, create_engine
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
""", ("sqlalchemy-2", "select"),
    ),
    Task(
        "16.7", "Session.get repository", "get_or_none использует Session.get и не commit.",
        """def get_or_none(session, model, object_id):
    raise NotImplementedError
""",
        """def get_or_none(session, model, object_id):
    return session.get(model, object_id)
""",
        """from sqlalchemy import create_engine
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
""", ("sqlalchemy-2", "session-get"),
    ),
    Task(
        "16.8", "Flush generated id", "add_and_flush делает add+flush и возвращает entity; commit запрещён.",
        """def add_and_flush(session, entity):
    raise NotImplementedError
""",
        """def add_and_flush(session, entity):
    session.add(entity)
    session.flush()
    return entity
""",
        """from sqlalchemy import create_engine
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
""", ("sqlalchemy-2", "flush"),
    ),
    Task(
        "16.9", "Rollback failed unit of work", "persist делает add+commit; на любой Exception rollback и re-raise.",
        """def persist(session, entity):
    raise NotImplementedError
""",
        """def persist(session, entity):
    try:
        session.add(entity)
        session.commit()
        return entity
    except Exception:
        session.rollback()
        raise
""",
        """import pytest
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
""", ("sqlalchemy-2", "rollback"),
    ),
    Task(
        "16.10", "Explicit transfer transaction", "transfer проверяет positive amount/balance и меняет два Account внутри session.begin.",
        """def transfer(session, source, target, amount):
    raise NotImplementedError
""",
        """def transfer(session, source, target, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    with session.begin():
        if source.balance < amount:
            raise ValueError("insufficient funds")
        source.balance -= amount
        target.balance += amount
""",
        """import pytest
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
""", ("sqlalchemy-2", "transaction"),
    ),
    Task(
        "16.11", "ORM join", "orders_for_email(User,Order,email): select Order join User, filter email, order id.",
        """def orders_for_email(User, Order, email):
    raise NotImplementedError
""",
        """from sqlalchemy import select

def orders_for_email(User, Order, email):
    return select(Order).join(User).where(User.email == email).order_by(Order.id)
""",
        """from sqlalchemy import ForeignKey, String, create_engine
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
""", ("sqlalchemy-2", "join"),
    ),
    Task(
        "16.13", "Убрать N+1", "users_with_roles(User): select + selectinload(User.roles), order id.",
        """def users_with_roles(User):
    raise NotImplementedError
""",
        """from sqlalchemy import select
from sqlalchemy.orm import selectinload

def users_with_roles(User):
    return select(User).options(selectinload(User.roles)).order_by(User.id)
""",
        """from sqlalchemy import ForeignKey, create_engine, event
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
""", ("sqlalchemy-2", "n-plus-one", "selectinload"),
    ),
    Task(
        "16.14", "selectinload collection", "projects_with_tasks(Project): selectinload(Project.tasks), order id.",
        """def projects_with_tasks(Project):
    raise NotImplementedError
""",
        """from sqlalchemy import select
from sqlalchemy.orm import selectinload

def projects_with_tasks(Project):
    return select(Project).options(selectinload(Project.tasks)).order_by(Project.id)
""",
        """from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from main import projects_with_tasks

class Base(DeclarativeBase): pass
class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    tasks: Mapped[list["TaskModel"]] = relationship()
class TaskModel(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

def test_detached_collection():
    engine = create_engine("sqlite://"); Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Project(id=1, tasks=[TaskModel(id=1), TaskModel(id=2)])); session.commit()
        projects = session.scalars(projects_with_tasks(Project)).all()
        session.expunge_all()
        assert [task.id for task in projects[0].tasks] == [1, 2]
""", ("sqlalchemy-2", "selectinload"),
    ),
    Task(
        "16.15", "joinedload scalar", "orders_with_user(Order): joinedload(Order.user), order id.",
        """def orders_with_user(Order):
    raise NotImplementedError
""",
        """from sqlalchemy import select
from sqlalchemy.orm import joinedload

def orders_with_user(Order):
    return select(Order).options(joinedload(Order.user)).order_by(Order.id)
""",
        """from sqlalchemy import ForeignKey, create_engine
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
""", ("sqlalchemy-2", "joinedload"),
    ),
    Task(
        "17.3", "Review autogenerate", "unsafe_operations возвращает DROP/DELETE/SET NOT NULL/nullable=false operations без изменения порядка.",
        """def unsafe_operations(operations):
    raise NotImplementedError
""",
        """def unsafe_operations(operations):
    markers = ("drop ", "delete ", "set not null", "nullable=false")
    return [operation for operation in operations if any(marker in operation.lower() for marker in markers)]
""",
        """from main import unsafe_operations

def test_classifies():
    operations = [
        "ADD COLUMN nickname TEXT",
        "DROP COLUMN legacy",
        "ALTER COLUMN email SET NOT NULL",
        "create index ix_user_email",
    ]
    assert unsafe_operations(operations) == ["DROP COLUMN legacy", "ALTER COLUMN email SET NOT NULL"]
def test_empty(): assert unsafe_operations([]) == []
""", ("alembic", "migration-review"),
    ),
]


def main() -> None:
    lessons, directories = indexes()
    tasks = FRAMEWORK_TASKS + ORM_TASKS
    if len(FRAMEWORK_TASKS) != 15 or len(ORM_TASKS) != 12:
        raise RuntimeError("practice count regression")
    for task in tasks:
        lesson = lessons[task.number]
        write_task(task, lesson, directories[lesson["implementation_slug"]])
    print(f"Added {len(FRAMEWORK_TASKS)} FastAPI/Pydantic and {len(ORM_TASKS)} SQLAlchemy/Alembic tasks")


if __name__ == "__main__":
    main()
