from contracts import Request, demo


def build_request(question, external_note=None) -> Request:
    raise NotImplementedError("Проверь вход и собери неизменяемую структуру")


if __name__ == "__main__":
    demo(build_request)
