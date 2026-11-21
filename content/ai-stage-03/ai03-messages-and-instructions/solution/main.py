from contracts import ALLOWED_TOOLS, POLICY, InputItem, Request, demo


def build_request(question, external_note=None) -> Request:
    if not isinstance(question, str) or not question.strip() or len(question) > 240:
        raise ValueError("Некорректный вопрос")
    if external_note is not None and (not isinstance(external_note, str) or len(external_note) > 600):
        raise ValueError("Некорректная заметка")
    items = (InputItem("question", question),)
    if external_note and external_note.strip():
        items += (InputItem("untrusted_note", external_note),)
    return Request(POLICY, items, ALLOWED_TOOLS)


if __name__ == "__main__":
    demo(build_request)
