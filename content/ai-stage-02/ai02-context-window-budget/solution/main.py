from fixtures import demo


def select_context(blocks, conversation_id, window, reserve, margin=0):
    remaining = window - reserve - margin
    if min(window, reserve, margin, remaining) < 0:
        raise ValueError("Некорректный бюджет")
    eligible = [(i, b) for i, b in enumerate(blocks) if b.conversation_id in {None, conversation_id}]
    if any(block.tokens < 0 for _, block in eligible):
        raise ValueError("Отрицательный размер блока")
    selected = {i for i, block in eligible if block.required}
    remaining -= sum(block.tokens for i, block in eligible if i in selected)
    if remaining < 0:
        raise ValueError("Обязательные блоки не помещаются")
    for index, block in sorted(eligible, key=lambda item: (item[1].priority, item[0]), reverse=True):
        if not block.required and block.tokens <= remaining:
            selected.add(index)
            remaining -= block.tokens
    return [block for index, block in eligible if index in selected]


if __name__ == "__main__":
    demo(select_context)
