class MagicBox:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"Message: {self.text}"

    def __repr__(self):
        return f"MagicBox(text={self.text!r})"

    def __len__(self):
        return len(self.text)

    def __bool__(self):
        return bool(self.text)


filled = MagicBox("Coding is magic")
empty = MagicBox("")
filled_str = str(filled)
filled_repr = repr(filled)
filled_len = len(filled)
filled_bool = bool(filled)
empty_bool = bool(empty)
