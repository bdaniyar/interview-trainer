from sqlalchemy import select
from sqlalchemy.orm import selectinload

def projects_with_tasks(Project):
    return select(Project).options(selectinload(Project.tasks)).order_by(Project.id)
