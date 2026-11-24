from hashlib import sha256

import pytest

from main import chunk_text


@pytest.mark.parametrize("text,size,overlap", [
    ("", 4, 1), ("\n\n", 3, 0), ("абвгдежзий", 3, 2), ("Қазақша 😀", 4, 0),
    ("# А\nсөз\n\n# Б\r\nкелесі", 6, 2), ("<!-- page: 9 -->\nкүрделі", 5, 1), ("z" * 147, 17, 16),
])
def test_offsets_lossless_coverage_and_progress(text, size, overlap):
    chunks = chunk_text("guide", 2, text, size, overlap)
    assert chunks == chunk_text("guide", 2, text, size, overlap)
    assert all(a.start < b.start for a, b in zip(chunks, chunks[1:]))
    assert len({chunk.chunk_id for chunk in chunks}) == len(chunks)
    covered = set()
    for chunk in chunks:
        assert chunk.text == text[chunk.start:chunk.end]
        assert 0 < len(chunk.text) <= size
        assert chunk.digest == sha256(chunk.text.encode()).hexdigest()
        covered.update(range(chunk.start, chunk.end))
    assert covered == set(range(len(text)))


def test_metadata_boundaries_and_version_identity():
    text = "введение\n# Ауа\nмәтін\n<!-- page: 3 -->\nжаңа\n## Басқа\nмәтін"
    a = chunk_text("abc", 1, text, 100, 5)
    b = chunk_text("abc", 2, text, 100, 5)
    assert [(x.page, x.section) for x in a] == [(1, None), (1, "Ауа"), (3, "Ауа"), (3, "Басқа")]
    assert [x.digest for x in a] == [x.digest for x in b]
    assert not {x.chunk_id for x in a} & {x.chunk_id for x in b}
    assert not {x.chunk_id for x in a} & {x.chunk_id for x in chunk_text("other", 1, text, 100, 5)}


def test_exact_overlap_within_section():
    chunks = chunk_text("doc", 1, "abcdefghi", 5, 2)
    assert [(c.start, c.end) for c in chunks] == [(0, 5), (3, 8), (6, 9)]


@pytest.mark.parametrize("key,version,size,overlap", [
    ("doc", 1, 2, 2), ("doc", 1, 4, -1), ("doc", 1, 0, 0), ("doc", True, 4, 0),
    ("", 2, 4, 0), ("doc", 2, 4, False), ("doc", 0, 9, 1),
])
def test_invalid_contract(key, version, size, overlap):
    with pytest.raises(ValueError):
        chunk_text(key, version, "x", size, overlap)
