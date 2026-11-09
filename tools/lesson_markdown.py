"""Small structural reader for lesson headings, fenced code and disclosures.

Only explicit <details>/<summary> authoring markup defines an answer. No answer
is inferred or hidden from words in prose by the runtime renderer.
"""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Section:
    title: str
    body: str
    start: int
    end: int


@dataclass(frozen=True)
class Disclosure:
    start: int
    end: int
    summary: str
    body: str
    closed: bool
    initially_open: bool


def structural_lines(source: str):
    offset = 0
    fence = None
    depth = 0
    for line in source.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        in_code = fence is not None or marker is not None
        yield offset, line, in_code, depth
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[marker.end():].strip():
                fence = None
        elif fence is None:
            if re.match(r'^\s*<details(?:\s[^>]*)?>', line, re.I):
                depth += 1
            if re.search(r'</details>\s*$', line, re.I):
                depth = max(0, depth - 1)
        offset += len(line)


def sections(source: str) -> list[Section]:
    headings = []
    for offset, line, code, depth in structural_lines(source):
        match = re.match(r'^## ([^\n]+)', line)
        if match and not code and not depth:
            headings.append((offset, offset + len(line), match[1].strip()))
    return [Section(title, source[body_start:headings[i + 1][0] if i + 1 < len(headings) else len(source)].strip(), start,
                    headings[i + 1][0] if i + 1 < len(headings) else len(source))
            for i, (start, body_start, title) in enumerate(headings)]


def disclosures(source: str) -> list[Disclosure]:
    result = []
    start = None
    for offset, line, code, depth in structural_lines(source):
        if code:
            continue
        if depth == 0 and re.match(r'^\s*<details(?:\s[^>]*)?>', line, re.I):
            start = offset
        if start is not None and depth <= 1 and re.search(r'</details>\s*$', line, re.I):
            end = offset + len(line)
            result.append(_disclosure(source, start, end, True))
            start = None
    if start is not None:
        result.append(_disclosure(source, start, len(source), False))
    return result


def _disclosure(source: str, start: int, end: int, closed: bool) -> Disclosure:
    block = source[start:end]
    opening = re.match(r'\s*<details([^>]*)>', block, re.I)
    summary = re.match(r'\s*<details[^>]*>\s*<summary>(.*?)</summary>', block, re.I | re.S)
    body = block[summary.end() if summary else opening.end():]
    if closed:
        body = re.sub(r'</details>\s*$', '', body, flags=re.I)
    return Disclosure(start, end, summary[1].strip() if summary else '', body.strip(), closed,
                      bool(re.search(r'\bopen\b', opening[1], re.I)))


def public_markdown(source: str) -> str:
    """Mask answer bodies while preserving positions, including line numbers."""
    visible = source
    for block in reversed(disclosures(source)):
        masked = re.sub(r'[^\n]', ' ', source[block.start:block.end])
        visible = visible[:block.start] + masked + visible[block.end:]
    return visible


def fenced_blocks(source: str) -> list[tuple[str, str, int]]:
    result = []
    fence = None
    for offset, line, _, _ in structural_lines(source):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if not marker:
            continue
        if fence is None:
            fence = (marker[1], line[marker.end():].strip().lower(), offset, offset + len(line))
        elif marker[1][0] == fence[0][0] and len(marker[1]) >= len(fence[0]) and not line[marker.end():].strip():
            result.append((fence[1], source[fence[3]:offset], fence[2]))
            fence = None
    return result
