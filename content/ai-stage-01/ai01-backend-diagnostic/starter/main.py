from fastapi import FastAPI
from demo import exercise


def create_app(actor, owners, provider, timeout=0.5) -> FastAPI:
    raise NotImplementedError("Добавь DTO, зависимость и POST /chat")


if __name__ == "__main__":
    exercise(create_app)
