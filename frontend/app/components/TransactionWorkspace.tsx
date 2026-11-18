'use client';

import dynamic from 'next/dynamic';
import { useEffect, useRef, useState } from 'react';
import { API_ORIGIN } from '../api';
import type { SqlCheckResult, SqlResult } from '../sqlTypes';
import { SqlCheckFeedback } from './SqlCheckFeedback';
import { SqlResultsTable } from './SqlResultsTable';

const Editor = dynamic(() => import('@monaco-editor/react'), { ssr: false });
type Side = 'A' | 'B';
type Rows = Pick<SqlResult, 'columns' | 'rows' | 'rows_returned' | 'has_more' | 'truncated' | 'duration_ms' | 'error'> & { command: string };
type Session = { session_id: string; generation: number; remaining_ms: number };
type Scenario = { id: string; title: string; expected: string };
type Manifest = {
  lesson_id: string; task_id: string | null; starter_sql: string;
  completed: boolean; scenarios: Scenario[];
};
type Timeline = {
  sequence: number; ms?: number; side: string; phase: string; statement?: string;
  result?: Rows; sqlstate?: string; blockers?: Side[]; code?: string; state?: string;
};
type Status = Session & {
  states: Record<Side, string>;
  pending: Partial<Record<Side, { operation: string; blockers: Side[]; cancelled: boolean }>>;
  timeline: Timeline[]; tables: Record<string, Rows>;
};
type Demo = { timeline: { session: string; sql?: string; result?: Rows; sqlstate?: string; phase?: string }[];
  sqlstate?: string; states?: (string | null)[] };

class LabError extends Error {
  constructor(message: string, readonly code: string) { super(message); }
}

const labels: Record<string, string> = {
  ready: 'Готова', transaction: 'В транзакции', failed: 'Нужен ROLLBACK',
  disconnected: 'Соединение закрыто', running: 'Выполняется', result: 'Результат',
  blocked: 'Ожидает блокировку', released: 'Ожидание завершено',
  cancelled: 'Отмена запрошена', error: 'Ошибка', reconnected: 'Соединение восстановлено',
  snapshot: 'Снимок подтверждённых данных',
};

async function request<T>(path: string, data?: object, method?: string, keepalive?: boolean): Promise<T> {
  const response = await fetch(API_ORIGIN + path, {
    method: method ?? (data ? 'POST' : 'GET'), keepalive,
    headers: data ? { 'Content-Type': 'application/json' } : undefined,
    body: data ? JSON.stringify(data) : undefined,
  });
  const payload = await response.json() as T & { error?: { message?: string; code?: string } };
  if (!response.ok) {
    throw new LabError(payload.error?.message ?? 'Не удалось обратиться к лаборатории.',
      payload.error?.code ?? 'unknown');
  }
  return payload as T;
}

function message(error: unknown) {
  return error instanceof Error ? error.message : 'Не удалось выполнить действие.';
}

function readLocal(key: string, fallback: string) {
  try { return localStorage.getItem(key) ?? fallback; }
  catch { return fallback; }
}

function TimelineList({ entries }: { entries: Timeline[] }) {
  if (!entries.length) return <p className="sql-empty">Выполните команду в A или B.</p>;
  return <ol className="tx-timeline">
    {entries.map(event => <li key={event.sequence}>
      <div className="tx-event-label">
        <strong>{event.side === 'observer' ? 'Наблюдатель' : event.side}</strong>
        <span>{labels[event.phase] ?? event.phase}</span>
        {event.ms !== undefined && <small>+{event.ms} мс</small>}
        {event.blockers?.length ? <span>держит {event.blockers.join(', ')}</span> : null}
        {event.sqlstate && <code>SQLSTATE {event.sqlstate}</code>}
        {event.code === 'result_limit' && <span>Превышен лимит результата</span>}
        {event.code === 'connection_closed' && <span>PostgreSQL закрыл соединение</span>}
        {event.result?.command && <code>{event.result.command}</code>}
      </div>
      {event.statement && <pre>{event.statement}</pre>}
      {event.result?.columns.length ? <SqlResultsTable result={event.result} /> : null}
    </li>)}
  </ol>;
}

export function TransactionWorkspace({ lessonSlug, theme }: { lessonSlug: string; theme: 'dark' | 'light' }) {
  const base = '/api/transactions/lessons/' + lessonSlug;
  const [manifest, setManifest] = useState<Manifest>();
  const [draft, setDraft] = useState<Record<Side, string>>({ A: '', B: '' });
  const [session, setSession] = useState<Session>();
  const [status, setStatus] = useState<Status>();
  const [events, setEvents] = useState<Timeline[]>([]);
  const [tab, setTab] = useState<Side | 'timeline' | 'schema'>('A');
  const [messageText, setMessage] = useState('');
  const [opening, setOpening] = useState(false);
  const [sending, setSending] = useState<Partial<Record<Side, boolean>>>({});
  const [checking, setChecking] = useState(false);
  const [grade, setGrade] = useState<{ result: SqlCheckResult; sql: string }>();
  const [completed, setCompleted] = useState(false);
  const [runningDemo, setRunningDemo] = useState(false);
  const [demo, setDemo] = useState<{ spec: Scenario; data: Demo }>();
  const cursor = useRef(0);
  const current = useRef<Session | undefined>(undefined);
  const mounted = useRef(false);
  const generationChange = useRef(false);
  const checkRequest = useRef<{ sql: string; id: string } | undefined>(undefined);
  const key = manifest && `pythoria:tx:${manifest.lesson_id}:${manifest.task_id ?? 'practice'}`;
  const sessionKey = 'pythoria:tx:session:' + lessonSlug;

  function storeSession(active?: Session) {
    try {
      if (active) sessionStorage.setItem(sessionKey, JSON.stringify(active));
      else sessionStorage.removeItem(sessionKey);
    } catch { /* Browser storage is optional for the live connection. */ }
  }

  function endpoint(active: Session) {
    return base + '/sessions/' + active.session_id;
  }

  function close(active: Session) {
    storeSession();
    const url = endpoint(active) + '?generation=' + active.generation;
    // A short status poll may already own the controller. Retry cleanup once.
    void request(url, undefined, 'DELETE', true).catch(error => {
      if (error instanceof LabError && error.code === 'busy') {
        setTimeout(() => void request(url, undefined, 'DELETE', true).catch(() => {}), 200);
      }
    });
  }

  useEffect(() => {
    mounted.current = true;
    let disposed = false;
    void request<Manifest>(base).then(data => {
      if (disposed) return;
      const draftKey = `pythoria:tx:${data.lesson_id}:${data.task_id ?? 'practice'}`;
      setDraft({ A: readLocal(draftKey + ':A', data.starter_sql),
        B: readLocal(draftKey + ':B', 'SELECT id, available FROM inventory ORDER BY id;') });
      setManifest(data);
      setCompleted(data.completed);
      try {
        const sessionData = sessionStorage.getItem(sessionKey);
        if (sessionData) {
          const previous = JSON.parse(sessionData) as Session;
          current.current = previous;
          setSession(previous);
        }
      } catch { storeSession(); }
    }).catch(error => { if (!disposed) setMessage(message(error)); });
    return () => {
      disposed = true;
      mounted.current = false;
      if (current.current) close(current.current);
    };
    // CourseApp keys the workspace by lesson. All closures use that lesson.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [base]);

  useEffect(() => {
    if (!session) return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;
    async function poll() {
      if (!session) return;
      try {
        if (!generationChange.current) {
          const next = await request<Status>(endpoint(session) +
            `?generation=${session.generation}&after=${cursor.current}`);
          if (!cancelled && current.current === session && !generationChange.current) {
            if (next.timeline.length) {
              cursor.current = next.timeline[next.timeline.length - 1].sequence;
              setEvents(previous => [...previous, ...next.timeline].slice(-96));
            }
            setStatus(next);
          }
        }
      } catch (error) {
        if (cancelled || current.current !== session || generationChange.current) return;
        if (error instanceof LabError && ['session_closed', 'stale_session'].includes(error.code)) {
          current.current = undefined;
          storeSession();
          setSession(undefined);
          setStatus(undefined);
        }
        if (!(error instanceof LabError && error.code === 'busy')) setMessage(message(error));
      }
      if (!cancelled && current.current === session) timer = setTimeout(poll, 120);
    }
    void poll();
    return () => { cancelled = true; clearTimeout(timer); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session]);

  async function open(reset = false) {
    if (opening) return;
    const old = current.current;
    setOpening(true);
    generationChange.current = true;
    setMessage('');
    try {
      const next = reset && old
        ? await request<Session>(endpoint(old) + '/reset', { generation: old.generation })
        : await request<Session>(base + '/sessions', {});
      if (!mounted.current) { close(next); return; }
      cursor.current = 0;
      setEvents([]);
      setStatus(undefined);
      setDemo(undefined);
      current.current = next;
      storeSession(next);
      setSession(next);
    } catch (error) {
      if (mounted.current) setMessage(message(error));
    } finally {
      generationChange.current = false;
      if (mounted.current) setOpening(false);
    }
  }

  function change(side: Side, value: string) {
    setDraft(previous => ({ ...previous, [side]: value }));
    if (key) {
      try { localStorage.setItem(key + ':' + side, value); }
      catch { setMessage('Браузер не смог сохранить черновик.'); }
    }
  }

  async function run(side: Side, source: string, active = current.current) {
    if (!active) return;
    setSending(previous => ({ ...previous, [side]: true }));
    setMessage('');
    try {
      await request(endpoint(active) + '/run', { generation: active.generation, side, sql: source });
    } catch (error) { if (current.current === active) setMessage(message(error)); }
    finally { setSending(previous => ({ ...previous, [side]: false })); }
  }

  async function action(kind: 'cancel' | 'snapshot', side?: Side, operation?: string) {
    const active = current.current;
    if (!active) return;
    try {
      await request(endpoint(active) + '/' + kind, { generation: active.generation, side, operation });
      if (kind === 'snapshot') setTab('schema');
    } catch (error) { if (current.current === active) setMessage(message(error)); }
  }

  async function check() {
    if (!manifest?.task_id || checking) return;
    const sql = draft.A;
    if (checkRequest.current?.sql !== sql) checkRequest.current = { sql, id: crypto.randomUUID() };
    setChecking(true);
    setMessage('');
    try {
      const result = await request<SqlCheckResult>(base + '/tasks/' + manifest.task_id + '/check',
        { request_id: checkRequest.current.id, sql });
      if (!mounted.current) return;
      checkRequest.current = undefined;
      setGrade({ result, sql });
      setCompleted(result.completed);
    } catch (error) { if (mounted.current) setMessage(message(error)); }
    finally { if (mounted.current) setChecking(false); }
  }

  async function showScenario(spec: Scenario) {
    setRunningDemo(true);
    setMessage('');
    try {
      const data = await request<Demo>(base + '/scenario', { name: spec.id });
      if (mounted.current) { setDemo({ spec, data }); setTab('timeline'); }
    } catch (error) { if (mounted.current) setMessage(message(error)); }
    finally { if (mounted.current) setRunningDemo(false); }
  }

  function loadBlockingExample() {
    change('A', 'BEGIN;\nUPDATE inventory SET available = available - 1 WHERE id = 1 AND available > 0 RETURNING id, available;');
    change('B', 'BEGIN;\nSELECT id, available FROM inventory WHERE id = 1 FOR UPDATE;');
  }

  return <section className="workspace-pane tx-workspace" data-tab={tab}>
    <header className="workspace-toolbar tx-toolbar">
      <strong>Transaction Lab</strong>
      <div>
        <button className="secondary-button" disabled={!manifest || opening} onClick={() => void open(Boolean(session))}>
          {opening ? 'Подготовка…' : session ? 'Reset' : 'Открыть сессии'}
        </button>
        {manifest?.task_id && <button className="check-button" disabled={checking || !draft.A.trim()}
          onClick={() => void check()}>{checking ? 'Проверяем…' : 'Check A'}</button>}
      </div>
    </header>
    <div className="tx-scroll">
      {completed && <div className="sql-task-completed" role="status">Задание выполнено</div>}
      {manifest?.task_id && <p className="tx-notice">Check проверяет черновик A на шести свежих наборах.</p>}
      {grade && <SqlCheckFeedback result={grade.result} stale={draft.A !== grade.sql} />}
      {messageText && <p className="tx-notice tx-error" role="alert">{messageText}</p>}
      {session && <p className="tx-notice">Сессия: {Math.ceil((status?.remaining_ms ?? session.remaining_ms) / 1000)} с.
        Открытая транзакция без команд истекает через 5 с.</p>}
      {manifest && <nav className="tx-tabs" aria-label="Вкладки лаборатории">
        {(['A', 'B', 'timeline', 'schema'] as const).map(value =>
          <button key={value} type="button" aria-pressed={tab === value} onClick={() => setTab(value)}>
            {value === 'timeline' ? 'Timeline' : value === 'schema' ? 'Данные' : `Сессия ${value}`}
          </button>)}
      </nav>}
      {manifest && <div className="tx-editors">
        {(['A', 'B'] as const).map(side => {
          const pending = status?.pending[side];
          const state = status?.states[side];
          return <section key={side} className="tx-editor" data-side={side} aria-label={`Сессия ${side}`}>
            <header>
              <strong>Сессия {side}</strong>
              <span role="status">{pending?.blockers.length ? `Ждёт ${pending.blockers.join(', ')}`
                : pending ? 'Выполняется…' : state ? labels[state] : 'База закрыта'}</span>
            </header>
            <Editor height="155px" language="sql" path={`transaction/${lessonSlug}/${side}.sql`}
              value={draft[side]} theme={theme === 'dark' ? 'vs-dark' : 'light'}
              onChange={value => change(side, value ?? '')}
              options={{ ariaLabel: `SQL сессии ${side}`, automaticLayout: true, fontSize: 13,
                wordWrap: 'on', minimap: { enabled: false }, scrollBeyondLastLine: false }} />
            <div className="tx-buttons">
              <button className="run-button" disabled={!session || opening || !!pending || sending[side] || !draft[side].trim()}
                onClick={() => void run(side, draft[side])}>Run {side}</button>
              {['COMMIT', 'ROLLBACK'].map(command => <button key={command} type="button"
                disabled={!session || opening || !!pending || sending[side] || !['transaction', 'failed'].includes(state ?? '')}
                onClick={() => void run(side, command)}>{command}</button>)}
              {pending && <button type="button" disabled={pending.cancelled || opening}
                onClick={() => void action('cancel', side, pending.operation)}>Отмена</button>}
            </div>
          </section>;
        })}
      </div>}
      {manifest && <section className="tx-examples">
        <button className="secondary-button" onClick={loadBlockingExample}>Пример блокировки в A/B</button>
        <p>Для примера запустите A, затем B. Пока B ждёт, нажмите COMMIT в A.</p>
        {manifest.scenarios.map(spec => <button key={spec.id} className="secondary-button"
          disabled={runningDemo} onClick={() => void showScenario(spec)}>{spec.title}</button>)}
        {runningDemo && <p role="status">Запускаем сценарий в отдельной базе…</p>}
      </section>}
      <section className="tx-events">
        <h3>Timeline</h3>
        {demo && <details open>
          <summary>{demo.spec.title}</summary>
          <p>{demo.spec.expected}</p>
          {demo.data.sqlstate && <code>SQLSTATE {demo.data.sqlstate}</code>}
          {demo.data.states?.filter(Boolean).map((code, index) => <code key={index}> SQLSTATE {code} </code>)}
          <TimelineList entries={demo.data.timeline.map((item, index) => ({
            sequence: index + 1, side: item.session, statement: item.sql,
            phase: item.phase ?? (item.sqlstate ? 'error' : 'result'),
            sqlstate: item.sqlstate, result: item.result,
          }))} />
        </details>}
        <TimelineList entries={events} />
      </section>
      <section className="tx-data">
        <h3>Схема и данные</h3>
        <p><code>orders(id, user_id, status, total, created_at)</code><br />
          <code>inventory(id, available)</code><br />
          <code>reservations(request_key, room_id, active)</code><br />
          users, products, order_items, slots</p>
        <button className="secondary-button" disabled={!session || opening}
          onClick={() => void action('snapshot')}>Показать подтверждённые строки</button>
        {Object.entries(status?.tables ?? {}).map(([table, result]) =>
          <details key={table}><summary>{table}</summary><SqlResultsTable result={result} /></details>)}
      </section>
    </div>
  </section>;
}
