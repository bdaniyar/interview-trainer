import json
import re
from hashlib import sha256

from contracts import Chunk


MARKER = re.compile(r"<!-- page: ([1-9][0-9]*) -->")
HEADING = re.compile(r"#{1,6} ([^\r\n]+)")


def boundaries(text):
    page, section, start, position = 1, None, 0, 0
    for line in text.splitlines(keepends=True):
        raw = line.rstrip("\r\n")
        marker = MARKER.fullmatch(raw)
        heading = HEADING.fullmatch(raw)
        if marker or heading:
            if start < position:
                yield start, position, page, section
            if marker:
                page = int(marker[1])
            else:
                section = heading[1].strip()
            start = position
        position += len(line)
    if start < len(text):
        yield start, len(text), page, section


def chunk_text(document_id, version, text, size, overlap):
    if (not document_id or type(version) is not int or version < 1
            or type(size) is not int or type(overlap) is not int or not 0 <= overlap < size):
        raise ValueError("invalid provenance or chunk bounds")
    result = []
    for start, end, page, section in boundaries(text):
        while start < end:
            stop = min(end, start + size)
            value = text[start:stop]
            digest = sha256(value.encode()).hexdigest()
            key = json.dumps([document_id, version, start, stop, digest], ensure_ascii=False)
            chunk_id = sha256(key.encode()).hexdigest()
            result.append(Chunk(document_id, version, chunk_id, page, section, start, stop, value, digest))
            if stop == end:
                break
            start = stop - overlap
    return tuple(result)


if __name__ == "__main__":
    for chunk in chunk_text("guide", 1, "# Ауа\nТаза ауа", 7, 2):
        print(chunk.page, chunk.section, (chunk.start, chunk.end), repr(chunk.text))
