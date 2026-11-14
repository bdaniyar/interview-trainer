import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { MarkdownLesson } from '../app/components/MarkdownLesson';
import { splitContent, splitSections } from '../app/components/lessonMarkdown';
import type { LessonData } from '../app/types';

afterEach(cleanup);

function loadLesson(directory: string): LessonData {
  const base = resolve(process.cwd(), '..', 'content', directory);
  return {
    ...JSON.parse(readFileSync(resolve(base, 'metadata.json'), 'utf8')),
    markdown: readFileSync(resolve(base, 'lesson.md'), 'utf8'),
    files: {}, interview: [],
    progress: { status: 'not_started', theory_completed: false, task_completed: false },
  };
}
const props = { theme: 'light' as const, position: 1, total: 359, onCompleteTheory: () => {}, onNavigate: () => {} };

it.each([
  ['s10-select-aliases-and-expressions', 'Показать решение SQL для самопроверки', 'id AS user_id'],
  ['s10-where-and-boolean-logic', 'Показать решение задачи для самопроверки', 'active IS TRUE'],
  ['s10-null-and-three-valued-logic', 'Показать решение задачи для самопроверки', 'country IS NULL'],
  ['s10-order-by-limit-and-offset', 'Показать решение для самопроверки', 'created_at DESC, id DESC'],
  ['s10-distinct', 'Показать решение для самопроверки', 'DISTINCT country'],
])('keeps the graded SQL answer closed in Learn and Review: %s', (slug, summary, sql) => {
  const lesson = loadLesson(`stage-10/${slug}`);
  render(<MarkdownLesson {...props} lesson={lesson} />);
  const answer = () => screen.getByText(summary).closest('details')!;
  expect(answer().open).toBe(false);
  expect(answer().textContent).toContain(sql);
  fireEvent.click(within(answer()).getByText(summary));
  expect(answer().open).toBe(true);
  review();
  expect(answer().open).toBe(false);
  learn();
  expect(answer().open).toBe(false);
});

function review() { fireEvent.click(screen.getByRole('button', { name: /Повторение/ })); }
function learn() { fireEvent.click(screen.getByRole('button', { name: /Обучение/ })); }
function parentAnswer(text: string): HTMLDetailsElement {
  const element = screen.getByText(text, { exact: false });
  const details = element.closest('details');
  expect(details).not.toBeNull();
  return details!;
}

it('keeps the Stage 8.1 answer closed in both modes and resets opened answers on mode changes', () => {
  const lesson = loadLesson('stage-08/s08-sync-concurrency-and-parallelism');
  render(<MarkdownLesson {...props} lesson={lesson} />);
  const answer = parentAnswer('Последовательное время — 1 + 4 + 2 = 7 секунд.');
  expect(answer.open).toBe(false);
  const question = 'Для ожиданий 1, 4 и 2 секунды найди последовательное и идеальное конкурентное время.';
  expect(screen.getAllByText(question)).toHaveLength(1);
  fireEvent.click(within(answer).getByText('Показать ответ'));
  expect(answer.open).toBe(true);
  review();
  const reviewAnswer = parentAnswer('Последовательное время — 1 + 4 + 2 = 7 секунд.');
  expect(reviewAnswer.open).toBe(false);
  expect(screen.queryByRole('heading', { name: 'Теория' })).toBeNull();
  fireEvent.click(within(reviewAnswer).getByText('Показать ответ'));
  expect(reviewAnswer.open).toBe(true);
  fireEvent.click(within(reviewAnswer).getByText('Показать ответ'));
  expect(reviewAnswer.open).toBe(false);
  learn();
  expect(screen.getByRole('heading', { name: 'Теория' })).toBeTruthy();
  expect(parentAnswer('Последовательное время — 1 + 4 + 2 = 7 секунд.').open).toBe(false);
});

it('keeps the to_thread explanation hidden while leaving its question visible', () => {
  render(<MarkdownLesson {...props} lesson={loadLesson('stage-08/s08-blocking-code-inside-async-code')} />);
  review();
  expect(screen.getAllByText('Почему', { exact: false }).length).toBeGreaterThan(0);
  const answer = parentAnswer('Затем to_thread получает Response вместо callable.');
  expect(answer.open).toBe(false);
  expect(screen.getByText('asyncio.to_thread(requests.get(url))')).toBeTruthy();
  fireEvent.click(within(answer).getByText('Показать ответ'));
  expect(answer.open).toBe(true);
});

it('keeps a real code prediction input public and its output behind a closed answer', () => {
  render(<MarkdownLesson {...props} lesson={loadLesson('reliability/parametrization')} />);
  review();
  const prediction = screen.getByRole('heading', { name: 'Предсказание результата кода' }).parentElement!;
  expect(prediction.querySelector('code')).toBeTruthy();
  const output = within(prediction).getByText('3 passed');
  const answer = output.closest('details')!;
  expect(answer.open).toBe(false);
  fireEvent.click(within(answer).getByText('Показать ответ'));
  expect(answer.open).toBe(true);
});

it('keeps the coding task signature, input/output examples and edge cases visible', () => {
  render(<MarkdownLesson {...props} lesson={loadLesson('stage-08/s08-sync-concurrency-and-parallelism')} />);
  review();
  for (const text of ['compare_waits(delays) -> tuple[int, int]', 'compare_waits([2, 3]) == (5, 3)', '(0, 0)', 'ValueError']) {
    expect(screen.getByText(text).closest('details')).toBeNull();
  }
});

it('does not carry an open answer into a different lesson', () => {
  const first = loadLesson('stage-08/s08-sync-concurrency-and-parallelism');
  const second = loadLesson('stage-08/s08-blocking-code-inside-async-code');
  const view = render(<MarkdownLesson {...props} lesson={first} />);
  review();
  const answer = parentAnswer('Последовательное время — 1 + 4 + 2 = 7 секунд.');
  fireEvent.click(within(answer).getByText('Показать ответ'));
  expect(answer.open).toBe(true);
  view.rerender(<MarkdownLesson {...props} lesson={second} />);
  expect(parentAnswer('Затем to_thread получает Response вместо callable.').open).toBe(false);
});

it('renders fenced code inside an answer without creating a spurious top-level section', () => {
  const lesson = loadLesson('stage-08/s08-sync-concurrency-and-parallelism');
  lesson.markdown = '# Example\n\n## Практика\n\nЧто напечатает код?\n\n<details>\n<summary>Показать ответ</summary>\n\n```python\nprint("hidden")\n## not a lesson heading\n```\n\n## Heading inside answer\n\nРазбор.\n\n</details>\n\n## Задача\n\nСигнатура и входные данные.';
  render(<MarkdownLesson {...props} lesson={lesson} />);
  review();
  expect(splitSections(lesson.markdown).sections.map(s => s.title)).toEqual(['Практика', 'Задача']);
  const answer = screen.getByText('Показать ответ').closest('details')!;
  expect(answer.open).toBe(false);
  expect(answer.querySelector('pre')).toBeTruthy();
  fireEvent.click(within(answer).getByText('Показать ответ'));
  expect(answer.open).toBe(true);
});

describe('structural authoring boundaries', () => {
  it('does not interpret literal disclosure tags in fenced code as an answer', () => {
    const source = '```html\n<details><summary>Example</summary>\ntext\n</details>\n```';
    expect(splitContent(source)).toEqual([{ kind: 'markdown', body: source }]);
  });
  it('keeps an unclosed authored answer hidden and handles nested disclosures', () => {
    const unclosed = splitContent('Question\n<details><summary>Показать ответ</summary>\nsecret');
    expect(unclosed[1]).toEqual({ kind: 'answer', summary: 'Показать ответ', body: 'secret' });
    const nested = '<details><summary>Outer</summary>\n<details><summary>Inner</summary>\nsecret\n</details>\n</details>';
    const outer = splitContent(nested)[0];
    expect(outer.kind).toBe('answer');
    expect(splitContent(outer.body)[0]).toEqual({ kind: 'answer', summary: 'Inner', body: 'secret' });
  });
});
