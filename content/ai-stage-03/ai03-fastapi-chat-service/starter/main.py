from uuid import uuid4
from contracts import demo


def create_app(provider, *, timeout=0.5, id_factory=uuid4):
    raise NotImplementedError("Добавь request/response DTO и обработчик")


if __name__ == "__main__":
    demo(create_app)
