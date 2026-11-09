/** Structural authoring boundaries; answer words are never runtime filters. */
export interface MarkdownSection { title: string; body: string }
export type ContentBlock = { kind: 'markdown'; body: string } | { kind: 'answer'; summary: string; body: string };

interface SourceLine { offset: number; line: string; code: boolean; depth: number }

function sourceLines(source: string): SourceLine[] {
  const lines: SourceLine[] = [];
  let offset = 0;
  let fence: string | undefined;
  let depth = 0;
  for (const line of source.match(/[^\n]*\n|[^\n]+$/g) ?? []) {
    const marker = /^ {0,3}(`{3,}|~{3,})/.exec(line);
    lines.push({ offset, line, code: Boolean(fence || marker), depth });
    if (marker) {
      const token = marker[1];
      if (!fence) fence = token;
      else if (token[0] === fence[0] && token.length >= fence.length && !line.slice(marker[0].length).trim()) fence = undefined;
    } else if (!fence) {
      if (/^\s*<details(?:\s[^>]*)?>/i.test(line)) depth += 1;
      if (/<\/details>\s*$/i.test(line)) depth = Math.max(0, depth - 1);
    }
    offset += line.length;
  }
  return lines;
}

export function splitSections(markdown: string): { intro: string; sections: MarkdownSection[] } {
  const headings = sourceLines(markdown).flatMap(({ offset, line, code, depth }) => {
    const match = /^## ([^\n]+)/.exec(line);
    return match && !code && !depth ? [{ offset, end: offset + line.length, title: match[1].trim() }] : [];
  });
  return {
    intro: markdown.slice(0, headings[0]?.offset ?? markdown.length).trim(),
    sections: headings.map((heading, index) => ({
      title: heading.title,
      body: markdown.slice(heading.end, headings[index + 1]?.offset ?? markdown.length).trim(),
    })),
  };
}

export function splitContent(source: string): ContentBlock[] {
  const spans: { start: number; end: number; closed: boolean }[] = [];
  let start: number | undefined;
  for (const { offset, line, code, depth } of sourceLines(source)) {
    if (code) continue;
    if (!depth && /^\s*<details(?:\s[^>]*)?>/i.test(line)) start = offset;
    if (start !== undefined && depth <= 1 && /<\/details>\s*$/i.test(line)) {
      spans.push({ start, end: offset + line.length, closed: true });
      start = undefined;
    }
  }
  // Keep an invalid/unclosed answer behind a disclosure too. The validator
  // rejects it; a broken closing tag must not publish the answer in the UI.
  if (start !== undefined) spans.push({ start, end: source.length, closed: false });
  const blocks: ContentBlock[] = [];
  let cursor = 0;
  for (const span of spans) {
    if (span.start > cursor) blocks.push({ kind: 'markdown', body: source.slice(cursor, span.start) });
    const raw = source.slice(span.start, span.end);
    const opening = /^\s*<details[^>]*>/i.exec(raw)!;
    const summary = /^\s*<details[^>]*>\s*<summary>([\s\S]*?)<\/summary>/i.exec(raw);
    const body = raw.slice(summary?.[0].length ?? opening[0].length);
    blocks.push({
      kind: 'answer', summary: summary?.[1].trim() || 'Показать ответ',
      body: (span.closed ? body.replace(/<\/details>\s*$/i, '') : body).trim(),
    });
    cursor = span.end;
  }
  if (cursor < source.length) blocks.push({ kind: 'markdown', body: source.slice(cursor) });
  return blocks;
}
