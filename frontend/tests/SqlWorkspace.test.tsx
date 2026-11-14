import { StrictMode } from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';

import { api } from '../app/api';
import { sqlApi, SqlApiError } from '../app/sqlApi';
import { draftKey, sqlPosition } from '../app/sqlDraft';
import type { SqlCatalog, SqlCheckResult, SqlLesson, SqlResult, SqlSession } from '../app/sqlTypes';
import type { CourseData, LessonData } from '../app/types';
import { SqlWorkspace } from '../app/components/SqlWorkspace';
import { SqlResultsTable } from '../app/components/SqlResultsTable';
import { CourseApp } from '../app/components/CourseApp';

vi.mock('@monaco-editor/react', () => ({ default: ({ value, onChange, language }: {
  value: string; onChange: (value: string) => void; language: string;
}) => <textarea aria-label="SQL запрос" data-language={language} value={value} onChange={e => onChange(e.target.value)} /> }));
vi.mock('../app/components/CodeWorkspace', () => ({ CodeWorkspace: ({ onSaved }: { onSaved: () => Promise<void> }) =>
  <section aria-label="Python Workspace"><button onClick={() => void onSaved()}>Save Python</button></section> }));

const slug = 's10-select-aliases-and-expressions';
const manifest: SqlLesson = { lesson_id: 'backend-interview.10.2.select-aliases-and-expressions',
  lesson_slug: slug, dataset_id: 'shop-v1', task_id: 'guided-select', mode: 'lesson_read',
  starter_sql: 'SELECT id, email FROM users;\n', prompt: 'Выберите столбцы.', can_check: false };
const initial: SqlSession = { session_id: 'public-1', generation: 1, lesson_id: manifest.lesson_id,
  lesson_slug: slug, task_id: manifest.task_id, dataset_id: 'shop-v1', dataset_checksum: 'a'.repeat(64),
  postgres_major: 17, created_at: '2026-11-11T00:00:00Z', expires_at: '2026-11-11T00:15:00Z', cold_start_ms: 5 };
function result(session = initial): SqlResult {
  return { session_id: session.session_id, generation: session.generation, command: 'SELECT',
    columns: [{ name: 'id', pg_type: 'int8', type_oid: 20 }], rows: [['1']], rows_returned: 1,
    has_more: false, truncated: false, duration_ms: 2, error: null, session_closed: false };
}
function catalog(session = initial): SqlCatalog {
  return { session_id: session.session_id, generation: session.generation, tables: [
    { handle: 'users-' + session.generation, schema_name: 'lab', name: 'users', columns: [
      { name: 'id', pg_type: 'bigint', nullable: false }, { name: 'manager_id', pg_type: 'bigint', nullable: true }],
      primary_key: ['id'], foreign_keys: [{ name: 'manager_fk', columns: ['manager_id'], referenced_table: 'users',
        referenced_columns: ['id'], on_update: 'NO ACTION', on_delete: 'NO ACTION' }] },
    { handle: 'order_items-' + session.generation, schema_name: 'lab', name: 'order_items', columns: [
      { name: 'order_id', pg_type: 'bigint', nullable: false }, { name: 'product_id', pg_type: 'bigint', nullable: false }],
      primary_key: ['order_id', 'product_id'], foreign_keys: [] },
  ] };
}

beforeEach(() => {
  localStorage.clear();
  window.history.replaceState({}, '', '/');
  vi.spyOn(sqlApi, 'lesson').mockResolvedValue(manifest);
  vi.spyOn(sqlApi, 'create').mockResolvedValue(initial);
  vi.spyOn(sqlApi, 'catalog').mockImplementation(async session => catalog(session));
  vi.spyOn(sqlApi, 'rows').mockImplementation(async session => result(session));
  vi.spyOn(sqlApi, 'run').mockImplementation(async session => result(session));
  vi.spyOn(sqlApi, 'reset').mockImplementation(async session => ({ ...session, generation: session.generation + 1 }));
  vi.spyOn(sqlApi, 'close').mockResolvedValue(undefined);
  vi.spyOn(sqlApi, 'check');
  vi.spyOn(api, 'saveFiles').mockResolvedValue({});
  vi.spyOn(api, 'run');
});
afterEach(async () => {
  cleanup();
  await act(async () => {});
  vi.restoreAllMocks();
});
const edit = (value: string) => fireEvent.change(screen.getByRole('textbox', { name: 'SQL запрос' }), { target: { value } });
const ready = () => screen.findByText('Read-only · сессия активна');
function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(done => { resolve = done; });
  return { promise, resolve };
}

it('opens SQL Monaco, runs real-contract requests and saves only a separate browser draft', async () => {
  render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready();
  expect(screen.getByRole('textbox').getAttribute('data-language')).toBe('sql');
  edit('SELECT email AS contact FROM users;');
  expect(localStorage.getItem(draftKey(manifest))).toBe('SELECT email AS contact FROM users;');
  fireEvent.click(screen.getByRole('button', { name: /^Run$/ }));
  await screen.findByRole('table', { name: 'Результат PostgreSQL' });
  expect(sqlApi.run).toHaveBeenCalledWith(initial, 'SELECT email AS contact FROM users;');
  expect(screen.queryByRole('button', { name: /Проверить|Check|Верное решение/ })).toBeNull();
  expect(api.saveFiles).not.toHaveBeenCalled();
  expect(api.run).not.toHaveBeenCalled();
});

it('retains query through Reset, Refresh and a theme change; rotates generation and Explorer handles', async () => {
  localStorage.setItem(draftKey(manifest), 'SELECT country FROM users;');
  const view = render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready();
  fireEvent.click(screen.getByRole('button', { name: 'Reset' }));
  await waitFor(() => expect(sqlApi.catalog).toHaveBeenLastCalledWith({ ...initial, generation: 2 }));
  await ready();
  fireEvent.click(screen.getByRole('button', { name: 'Refresh' }));
  await ready();
  view.rerender(<SqlWorkspace lessonSlug={slug} theme="light" />);
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT country FROM users;');
  expect(sqlApi.create).toHaveBeenCalledTimes(1);
  fireEvent.keyDown(window, { ctrlKey: true, key: 'Enter' });
  await waitFor(() => expect(sqlApi.run).toHaveBeenCalledWith({ ...initial, generation: 2 }, 'SELECT country FROM users;'));
  await screen.findByText('Строк: 1');
  view.unmount();
  await waitFor(() => expect(sqlApi.close).toHaveBeenLastCalledWith({ ...initial, generation: 2 }));
});

it('browses PK/composite PK and self FK using opaque handles and paged data', async () => {
  render(<SqlWorkspace lessonSlug={slug} theme="light" />);
  await ready();
  fireEvent.click(screen.getByRole('tab', { name: 'База данных' }));
  expect(screen.getByText(/\(manager_id\)/)).toBeTruthy();
  expect(screen.getByRole('button', { name: 'users (id)' })).toBeTruthy();
  fireEvent.change(screen.getByRole('combobox', { name: 'Выбрать таблицу' }), { target: { value: 'order_items' } });
  await waitFor(() => expect(sqlApi.rows).toHaveBeenLastCalledWith(initial, 'order_items-1', 0));
  await ready();
  expect(screen.getByText('(order_id, product_id)')).toBeTruthy();
  expect(screen.getByText('Данные: order_items')).toBeTruthy();
});

it('handles expiry and unavailable runner without losing edited SQL', async () => {
  vi.mocked(sqlApi.run).mockRejectedValue(new SqlApiError(410, 'expired', 'SQL-сессия завершена.'));
  render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready(); edit('SELECT 42;');
  fireEvent.click(screen.getByRole('button', { name: 'Run' }));
  await screen.findByText('SQL-сессия завершена.');
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT 42;');
  expect((screen.getByRole('button', { name: 'Run' }) as HTMLButtonElement).disabled).toBe(true);
  vi.mocked(sqlApi.create).mockResolvedValue({ ...initial, session_id: 'public-2' });
  fireEvent.click(screen.getByRole('button', { name: 'Создать сессию' }));
  await ready();
  expect(localStorage.getItem(draftKey(manifest))).toBe('SELECT 42;');
});

it('ignores a late response and closes a session created after unmount', async () => {
  const pending = deferred<SqlSession>();
  vi.mocked(sqlApi.create).mockReturnValue(pending.promise);
  const view = render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await waitFor(() => expect(sqlApi.create).toHaveBeenCalledTimes(1));
  view.unmount();
  await act(async () => pending.resolve(initial));
  await waitFor(() => expect(sqlApi.close).toHaveBeenCalledWith(initial));
  expect(sqlApi.catalog).not.toHaveBeenCalled();
});

it('closes only after an in-flight Run finishes and prevents duplicate shortcut submissions', async () => {
  const pending = deferred<SqlResult>();
  vi.mocked(sqlApi.run).mockReturnValue(pending.promise);
  const view = render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready();
  fireEvent.keyDown(window, { ctrlKey: true, key: 'Enter' });
  fireEvent.keyDown(window, { ctrlKey: true, key: 'Enter' });
  expect(sqlApi.run).toHaveBeenCalledTimes(1);
  view.unmount();
  expect(sqlApi.close).not.toHaveBeenCalled();
  await act(async () => pending.resolve(result()));
  await waitFor(() => expect(sqlApi.close).toHaveBeenCalledWith(initial));
});

it('does not create duplicate leases in React StrictMode', async () => {
  render(<StrictMode><SqlWorkspace lessonSlug={slug} theme="light" /></StrictMode>);
  await ready();
  expect(sqlApi.create).toHaveBeenCalledTimes(1);
});

const graded: SqlLesson = { ...manifest, task_id: 'sql.guided.10.2.projection.v1', can_check: true,
  task_revision: 1, completed: false, expected_columns: ['user_id', 'email'] };
const gradeResult: SqlCheckResult = { request_id: '00000000-0000-4000-8000-000000000000', task_id: graded.task_id,
  task_revision: 1, grader_revision: 'projection-v1', passed: true, tests_passed: 4, tests_total: 4,
  completed: true, feedback: [{ code: 'passed', message: 'Запрос прошёл все проверки.', sqlstate: null }] };

it('migrates the Phase 2 draft and checks via keyboard without a second simultaneous submission', async () => {
  localStorage.setItem(draftKey(manifest), 'SELECT saved_draft FROM users;');
  vi.mocked(sqlApi.lesson).mockResolvedValue(graded);
  const pending = deferred<SqlCheckResult>();
  vi.mocked(sqlApi.check).mockReturnValue(pending.promise);
  render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready();
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT saved_draft FROM users;');
  expect(localStorage.getItem(draftKey(graded))).toBe('SELECT saved_draft FROM users;');
  const editorKeys = vi.fn((event: Event) => event.stopPropagation());
  const editor = screen.getByRole('textbox');
  editor.addEventListener('keydown', editorKeys);
  fireEvent.keyDown(editor, { ctrlKey: true, shiftKey: true, key: 'Enter' });
  fireEvent.keyDown(editor, { metaKey: true, shiftKey: true, key: 'Enter' });
  expect(editorKeys).not.toHaveBeenCalled();
  expect(sqlApi.check).toHaveBeenCalledTimes(1);
  expect(vi.mocked(sqlApi.check).mock.calls[0].slice(0, 3)).toEqual([slug, graded.task_id, 'SELECT saved_draft FROM users;']);
  expect((screen.getByRole('button', { name: 'Reset' }) as HTMLButtonElement).disabled).toBe(true);
  await act(async () => pending.resolve(gradeResult));
  expect(screen.getByText('Passed')).toBeTruthy();
  expect(screen.getByText('4 / 4 проверок')).toBeTruthy();
  expect(screen.getByText('Задача решена')).toBeTruthy();
  expect(api.saveFiles).not.toHaveBeenCalled();
});

it('does not call a successful Run solved; failed Check keeps earlier completion after Reset', async () => {
  vi.mocked(sqlApi.lesson).mockResolvedValue(graded);
  vi.mocked(sqlApi.check).mockResolvedValueOnce(gradeResult).mockResolvedValueOnce({ ...gradeResult,
    passed: false, tests_passed: 1, feedback: [{ code: 'rows', message: 'Проверьте строки.', sqlstate: null }] });
  render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready();
  fireEvent.click(screen.getByRole('button', { name: 'Run' }));
  await screen.findByText('Строк: 1');
  expect(screen.queryByText('Задача решена')).toBeNull();
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  await screen.findByText('Passed');
  fireEvent.click(screen.getByRole('tab', { name: 'query.sql' }));
  edit('SELECT changed FROM users;');
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  await screen.findByText('Failed');
  expect(screen.getByText('Задача решена')).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Reset' }));
  await ready();
  fireEvent.click(screen.getByRole('tab', { name: 'query.sql' }));
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT changed FROM users;');
  expect(screen.getByText('Задача решена')).toBeTruthy();
});

it('restores solved progress on reload and allows Check after editor session expiry', async () => {
  vi.mocked(sqlApi.lesson).mockResolvedValue({ ...graded, completed: true });
  vi.mocked(sqlApi.run).mockRejectedValue(new SqlApiError(410, 'expired', 'Сессия истекла.'));
  vi.mocked(sqlApi.check).mockResolvedValue(gradeResult);
  render(<SqlWorkspace lessonSlug={slug} theme="light" />);
  await ready();
  expect(screen.getByText('Задача решена')).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Run' }));
  await screen.findByText('Сессия истекла.');
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  await screen.findByText('Passed');
  expect(sqlApi.create).toHaveBeenCalledTimes(1);
});

it('keeps editor and results together on a wide workspace after Run and Check', async () => {
  vi.mocked(sqlApi.lesson).mockResolvedValue(graded);
  vi.mocked(sqlApi.check).mockResolvedValue(gradeResult);
  render(<SqlWorkspace lessonSlug={slug} theme="light" />);
  await ready();
  Object.defineProperty(screen.getByRole('region', { name: 'SQL Workspace' }), 'clientWidth', { value: 500 });
  fireEvent.click(screen.getByRole('button', { name: 'Run' }));
  await screen.findByText('Строк: 1');
  expect(screen.getByRole('textbox', { name: 'SQL запрос' })).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  await screen.findByText('Passed');
  expect(screen.getByRole('textbox', { name: 'SQL запрос' })).toBeTruthy();
});

it('Check errors preserve the draft and do not mark an unsolved task complete', async () => {
  vi.mocked(sqlApi.lesson).mockResolvedValue(graded);
  vi.mocked(sqlApi.check).mockRejectedValue(new SqlApiError(503, 'grading_unavailable', 'Проверка недоступна.'));
  render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready(); edit('SELECT keep_me FROM users;');
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  await screen.findByText('Проверка недоступна.');
  expect(localStorage.getItem(draftKey(graded))).toBe('SELECT keep_me FROM users;');
  expect(screen.queryByText('Задача решена')).toBeNull();
});

const where: SqlLesson = { ...graded, lesson_slug: 's10-where-and-boolean-logic',
  lesson_id: 'backend-interview.10.3.where-and-boolean-logic', task_id: 'sql.basic.01',
  starter_sql: 'SELECT id, email\nFROM users;\n', prompt: 'Только активные пользователи.', expected_columns: ['id', 'email'] };
const nullable: SqlLesson = { ...where, lesson_slug: 's10-null-and-three-valued-logic',
  lesson_id: 'backend-interview.10.4.null-and-three-valued-logic', task_id: 'sql.basic.03', prompt: 'Неизвестная страна.' };
const latest: SqlLesson = { ...where, lesson_slug: 's10-order-by-limit-and-offset',
  lesson_id: 'backend-interview.10.5.order-by-limit-and-offset', task_id: 'sql.basic.04',
  starter_sql: 'SELECT id, created_at\nFROM orders;\n', prompt: 'Два последних заказа.', expected_columns: ['id', 'created_at'] };
const countries: SqlLesson = { ...where, lesson_slug: 's10-distinct', lesson_id: 'backend-interview.10.6.distinct',
  task_id: 'sql.basic.05', starter_sql: 'SELECT country\nFROM users;\n', prompt: 'Уникальные страны.', expected_columns: ['country'] };

function multipleLessons() {
  const manifests = [graded, where, nullable, latest, countries];
  const solved = new Set<string>();
  vi.mocked(sqlApi.lesson).mockImplementation(async slug => ({ ...manifests.find(m => m.lesson_slug === slug)!,
    completed: solved.has(slug) }));
  let serial = 0;
  vi.mocked(sqlApi.create).mockImplementation(async slug => {
    const manifest = manifests.find(m => m.lesson_slug === slug)!;
    return { ...initial, lesson_id: manifest.lesson_id, lesson_slug: slug, task_id: manifest.task_id, session_id: `session-${++serial}` };
  });
  vi.mocked(sqlApi.check).mockImplementation(async (slug, taskId) => {
    solved.add(slug);
    const count = [4, 5, 5, 6, 6][manifests.findIndex(m => m.task_id === taskId)];
    return { ...gradeResult, task_id: taskId, tests_total: count, tests_passed: count };
  });
  return solved;
}

it('navigates 10.2 → 10.3 → 10.4 → 10.5 → 10.6 with independent state and serialized sessions', async () => {
  multipleLessons();
  const mounted = render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready(); edit('SELECT projection_draft FROM users;');
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  await screen.findByText('Passed');
  const closing = deferred<void>();
  vi.mocked(sqlApi.close).mockReturnValueOnce(closing.promise);
  mounted.rerender(<SqlWorkspace lessonSlug={where.lesson_slug} theme="dark" />);
  await waitFor(() => expect(sqlApi.close).toHaveBeenCalledTimes(1));
  expect(sqlApi.create).toHaveBeenCalledTimes(1);
  expect(screen.queryByText('Passed')).toBeNull();
  expect(screen.queryByText('Задача решена')).toBeNull();
  await act(async () => closing.resolve());
  await ready();
  expect(screen.getByText(where.prompt)).toBeTruthy();
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe(where.starter_sql);
  edit('SELECT where_draft FROM users;');
  fireEvent.keyDown(screen.getByRole('textbox'), { metaKey: true, key: 'Enter' });
  await screen.findByText('Строк: 1');
  expect(vi.mocked(sqlApi.run).mock.calls.at(-1)?.[0].task_id).toBe(where.task_id);
  expect(screen.queryByText('Задача решена')).toBeNull();
  mounted.rerender(<SqlWorkspace lessonSlug={nullable.lesson_slug} theme="light" />);
  await ready();
  expect(screen.queryByText('Строк: 1')).toBeNull();
  expect(screen.getByText(nullable.prompt)).toBeTruthy();
  edit('SELECT null_draft FROM users;');
  fireEvent.keyDown(screen.getByRole('textbox'), { ctrlKey: true, shiftKey: true, key: 'Enter' });
  await screen.findByText('5 / 5 проверок');
  expect(vi.mocked(sqlApi.check).mock.calls.at(-1)?.slice(0, 3)).toEqual([nullable.lesson_slug, nullable.task_id, 'SELECT null_draft FROM users;']);
  fireEvent.click(screen.getByRole('button', { name: 'Reset' })); await ready();
  expect(screen.getByText('Задача решена')).toBeTruthy();
  for (const manifest of [latest, countries]) {
    mounted.rerender(<SqlWorkspace lessonSlug={manifest.lesson_slug} theme="light" />); await ready();
    expect(screen.getByText(manifest.prompt)).toBeTruthy();
    expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe(manifest.starter_sql);
    expect(screen.queryByText('Passed')).toBeNull();
    expect(screen.queryByText('Задача решена')).toBeNull();
    edit(`SELECT draft_for_${manifest.task_id};`);
    fireEvent.keyDown(screen.getByRole('textbox'), { metaKey: true, shiftKey: true, key: 'Enter' });
    await screen.findByText('6 / 6 проверок');
    expect(vi.mocked(sqlApi.check).mock.calls.at(-1)?.slice(0, 3)).toEqual([
      manifest.lesson_slug, manifest.task_id, `SELECT draft_for_${manifest.task_id};`]);
  }
  mounted.rerender(<SqlWorkspace lessonSlug={where.lesson_slug} theme="light" />);
  await ready();
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT where_draft FROM users;');
  expect(screen.queryByText('Задача решена')).toBeNull();
  expect(screen.queryByText('Passed')).toBeNull();
  mounted.rerender(<SqlWorkspace lessonSlug={slug} theme="light" />); await ready();
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT projection_draft FROM users;');
  expect(screen.getByText('Задача решена')).toBeTruthy();
  expect(localStorage.getItem(draftKey(nullable))).toBe('SELECT null_draft FROM users;');
  for (const manifest of [latest, countries]) {
    mounted.rerender(<SqlWorkspace lessonSlug={manifest.lesson_slug} theme="dark" />); await ready();
    expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe(`SELECT draft_for_${manifest.task_id};`);
    expect(screen.getByText('Задача решена')).toBeTruthy();
    expect(screen.queryByText('Passed')).toBeNull();
  }
  expect(api.saveFiles).not.toHaveBeenCalled();
});

it.each([[graded, where], [latest, countries]])('ignores late Check and waits for previous SQL lesson cleanup (%#)', async (from, to) => {
  multipleLessons();
  const pending = deferred<SqlCheckResult>();
  vi.mocked(sqlApi.check).mockReturnValueOnce(pending.promise);
  const mounted = render(<SqlWorkspace lessonSlug={from.lesson_slug} theme="dark" />); await ready();
  fireEvent.click(screen.getByRole('button', { name: 'Check' }));
  mounted.rerender(<SqlWorkspace lessonSlug={to.lesson_slug} theme="dark" />);
  await act(async () => {});
  expect(sqlApi.create).toHaveBeenCalledTimes(1);
  expect(sqlApi.close).not.toHaveBeenCalled();
  await act(async () => pending.resolve({ ...gradeResult, task_id: from.task_id })); await ready();
  expect(sqlApi.close).toHaveBeenCalledTimes(1);
  expect(screen.getByText(to.prompt)).toBeTruthy();
  expect(screen.queryByText('Задача решена')).toBeNull();
  expect(screen.queryByText('Passed')).toBeNull();
});

it('reports browser storage failure while keeping the query editable', async () => {
  render(<SqlWorkspace lessonSlug={slug} theme="dark" />);
  await ready();
  vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('quota'); });
  edit('SELECT 7;');
  expect(screen.getByText('Сохранение недоступно — скопируйте запрос')).toBeTruthy();
  expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('SELECT 7;');
});

describe('typed results and diagnostics', () => {
  it('preserves aliases, NULL, empty string, bigint, booleans and literal HTML', () => {
    const output = result();
    output.columns = Array.from({ length: 6 }, () => ({ name: 'x', pg_type: 'text', type_oid: 25 }));
    output.rows = [[null, '', '9007199254740993', false, 'NULL', '<img src=x onerror=alert(1)>']];
    output.has_more = output.truncated = true;
    const view = render(<SqlResultsTable result={output} />);
    expect(screen.getAllByRole('columnheader')).toHaveLength(6);
    expect(screen.getByTitle('SQL NULL').textContent).toBe('NULL');
    expect(screen.getByTitle('Пустая строка').textContent).toBe("''");
    expect(screen.getByText('9007199254740993')).toBeTruthy();
    expect(screen.getByText('false')).toBeTruthy();
    expect(screen.getByText('"NULL"')).toBeTruthy();
    expect(view.container.querySelector('img')).toBeNull();
    expect(screen.getByText('Показано 1 строк, есть ещё')).toBeTruthy();
  });

  it('keeps metadata on empty results and exposes SQLSTATE with Unicode-aware editor position', () => {
    const output = result(); output.rows = []; output.rows_returned = 0;
    const view = render(<SqlResultsTable result={output} />);
    expect(screen.getByText('Запрос выполнен. Строк нет.')).toBeTruthy();
    output.error = { kind: 'postgres', code: 'query_error', message: 'unknown column', sqlstate: '42703', position: 13, hint: null };
    const focus = vi.fn();
    view.rerender(<SqlResultsTable result={output} query={"SELECT '😀', bad"} onPosition={focus} />);
    fireEvent.click(screen.getByRole('button', { name: 'Строка 1, столбец 14' }));
    expect(focus).toHaveBeenCalledWith(13);
    expect(screen.getByText('SQLSTATE 42703')).toBeTruthy();
    expect(sqlPosition("SELECT 'я';\nSELECT bad", 20)).toEqual({ line: 2, column: 8, offset: 19 });
  });
});

it('switches CourseApp between SQL and Python without saving SQL via the Python files endpoint', async () => {
  const base = { module_slug: 'test', module_title: 'Test', order: 1, duration: 10, xp: 5,
    topics: ['select'], description: '', has_task: false, has_solution: false,
    progress: { status: 'not_started' as const, theory_completed: false, task_completed: false },
    markdown: '# Lesson\n\n## Теория\nText\n\n## Практика\nQuestion', interview: [],
    files: { 'main.py': 'ORIGINAL = True\n', 'extra.py': 'SAVED = 42\n' } };
  const sql: LessonData = { ...base, slug, title: 'SQL lesson', workspace_kind: 'sql' };
  const python: LessonData = { ...base, slug: 'python', title: 'Python lesson', workspace_kind: 'python' };
  const course = { title: 'Test', modules: [{ slug: 'test', title: 'Test', order: 1, lessons: [
    { ...python, status: 'not_started', theory_completed: false, task_completed: false },
    { ...sql, status: 'not_started', theory_completed: false, task_completed: false },
  ] }], summary: { total: 2, completed: 0, percent: 0, xp: 0, last_opened_lesson: slug, theme: 'light' } } as CourseData;
  vi.spyOn(api, 'course').mockResolvedValue(course);
  vi.spyOn(api, 'lesson').mockImplementation(async value => value === slug ? sql : python);
  vi.spyOn(api, 'openLesson').mockResolvedValue({});
  render(<CourseApp />);
  await ready(); edit('SELECT custom_draft FROM users;');
  fireEvent.click(screen.getByRole('button', { name: /Повторение/ }));
  expect((screen.getByRole('textbox', { name: 'SQL запрос' }) as HTMLTextAreaElement).value).toBe('SELECT custom_draft FROM users;');
  expect(sqlApi.create).toHaveBeenCalledTimes(1);
  fireEvent.click(screen.getByRole('button', { name: /Python lesson/ }));
  await screen.findByRole('region', { name: 'Python Workspace' });
  expect(api.saveFiles).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Save Python' }));
  await waitFor(() => expect(api.saveFiles).toHaveBeenCalledWith('python', base.files));
  fireEvent.click(screen.getByRole('button', { name: /SQL lesson/ }));
  await ready();
  expect((screen.getByRole('textbox', { name: 'SQL запрос' }) as HTMLTextAreaElement).value).toBe('SELECT custom_draft FROM users;');
  expect(vi.mocked(api.saveFiles).mock.calls.every(([lesson, files]) => lesson === 'python' && files['main.py'] === 'ORIGINAL = True\n')).toBe(true);
  expect(screen.queryByRole('region', { name: 'Python Workspace' })).toBeNull();
  expect(within(screen.getByRole('region', { name: 'SQL Workspace' })).queryByText('Check')).toBeNull();
});
