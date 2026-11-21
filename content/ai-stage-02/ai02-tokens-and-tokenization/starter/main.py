from fixtures import FALLBACK, VOCABS


def encode(text, version, framed=False):
    raise NotImplementedError("Выбери максимально длинный префикс")


def decode(ids, version):
    raise NotImplementedError("Восстанови текст из ID")


def fits_budget(text, version, maximum):
    raise NotImplementedError("Учти рамку")


if __name__ == "__main__":
    ids = encode("привет!", "A", framed=True)
    assert ids == [0, 2, 3, 1] and decode(ids, "A") == "привет!"
    print(ids)
