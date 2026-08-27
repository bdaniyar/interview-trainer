from sqlalchemy import ForeignKey, create_engine
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
