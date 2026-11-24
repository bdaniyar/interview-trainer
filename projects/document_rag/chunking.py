"""Small heading-aware Markdown segmenter with original Unicode offsets."""
import re

from projects.vector_search.contracts import ChunkInput, digest


HEADING = re.compile(r"#{1,6} (.+)")


def chunk_ranges(body: str, size: int = 480, overlap: int = 48):
    if not 0 <= overlap < size:
        raise ValueError("invalid chunk bounds")
    boundaries = [(0, "Document")]
    offset = 0
    for line in body.splitlines(keepends=True):
        match = HEADING.fullmatch(line.rstrip("\r\n"))
        if match:
            if offset == 0:
                boundaries[0] = (0, match[1])
            else:
                boundaries.append((offset, match[1]))
        offset += len(line)
    boundaries.append((len(body), ""))
    for (start, section), (end, _) in zip(boundaries, boundaries[1:]):
        while start < end:
            stop = min(start + size, end)
            yield section, start, stop
            if stop == end:
                break
            start = stop - overlap


def prepare(document_id, version, body, embed_batch):
    ranges = tuple(chunk_ranges(body))
    texts = tuple(body[start:stop] for _, start, stop in ranges)
    embeddings = embed_batch(texts)
    if len(embeddings) != len(texts):
        raise ValueError("embedding batch was incomplete")
    return tuple(
        ChunkInput(digest(f"{document_id}:{version}:{start}:{stop}:{digest(text)}"),
                   section, start, text, vector)
        for (section, start, stop), text, vector in zip(ranges, texts, embeddings, strict=True)
    )
