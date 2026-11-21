from fixtures import demo


def select_context(blocks, conversation_id, window, reserve, margin=0):
    raise NotImplementedError("Сначала обязательные блоки, затем необязательные")


if __name__ == "__main__":
    demo(select_context)
