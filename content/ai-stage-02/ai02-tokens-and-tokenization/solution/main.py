from fixtures import FALLBACK, VOCABS


def vocabulary(version):
    try:
        return VOCABS[version]
    except KeyError:
        raise ValueError("Неизвестная версия") from None


def encode(text, version, framed=False):
    vocab = vocabulary(version)
    fragments = sorted(vocab, key=len, reverse=True)
    result = [0] if framed else []
    position = 0
    while position < len(text):
        match = next((part for part in fragments if text.startswith(part, position)), None)
        if match is None:
            result.append(FALLBACK + ord(text[position]))
            position += 1
        else:
            result.append(vocab[match])
            position += len(match)
    if framed:
        result.append(1)
    return result


def decode(ids, version):
    by_id = {index: part for part, index in vocabulary(version).items()}
    if ids and ids[0] == 0 and ids[-1] == 1:
        ids = ids[1:-1]
    text = []
    for index in ids:
        if index in by_id:
            text.append(by_id[index])
        elif FALLBACK <= index <= FALLBACK + 0x10ffff:
            text.append(chr(index - FALLBACK))
        else:
            raise ValueError("Неизвестный ID или повреждённая рамка")
    return "".join(text)


def fits_budget(text, version, maximum):
    if maximum < 0:
        raise ValueError("Лимит должен быть неотрицательным")
    return len(encode(text, version, framed=True)) <= maximum


if __name__ == "__main__":
    ids = encode("привет!", "A", framed=True)
    assert ids == [0, 2, 3, 1] and decode(ids, "A") == "привет!"
    print(ids)
