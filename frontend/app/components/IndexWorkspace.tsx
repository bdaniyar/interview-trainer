'use client';

import dynamic from 'next/dynamic';
import { useEffect, useRef, useState } from 'react';
import { API_ORIGIN } from '../api';
import type { SqlCheckResult, SqlResult } from '../sqlTypes';
import { SqlCheckFeedback } from './SqlCheckFeedback';
import { SqlResultsTable } from './SqlResultsTable';

const Editor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

type Manifest = {
  lesson_id: string; task_id: string; title: string; prompt: string; starter: string;
  queries: string[]; completed: boolean;
};
type Plan = {
  'Node Type': string; 'Relation Name'?: string; 'Index Name'?: string;
  'Plan Rows'?: number; 'Actual Rows'?: number; 'Actual Loops'?: number;
  'Shared Hit Blocks'?: number; 'Shared Read Blocks'?: number;
  'Rows Removed by Filter'?: number; 'Rows Removed by Index Recheck'?: number;
  'Heap Fetches'?: number; 'Sort Method'?: string; 'Hash Batches'?: number;
  'Index Cond'?: string; Filter?: string; Plans?: Plan[];
};
type Proof = {
  result?: SqlResult; error?: string; sqlstate?: string;
  plan?: Plan; baseline_plan?: Plan; controlled?: Plan;
  samples?: number[]; baseline_samples?: number[]; median_ms?: number;
  planning_ms?: number; baseline_planning_ms?: number;
};
type Preview = { estimated: boolean; runs: Proof[]; definitions: [string, string][]; valid: boolean };

async function request<T>(path: string, data?: object): Promise<T> {
  const response = await fetch(API_ORIGIN + path, data ? {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data),
  } : undefined);
  const payload = await response.json() as T & { error?: { message?: string } };
  if (!response.ok) throw new Error(payload.error?.message ?? 'Лаборатория временно недоступна.');
  return payload;
}

function PlanNode({ plan }: { plan: Plan }) {
  return <li>
    <strong>{plan['Node Type']}</strong>
    {plan['Relation Name'] && <span> · {plan['Relation Name']}</span>}
    {plan['Index Name'] && <span> · {plan['Index Name']}</span>}
    <div>Оценка строк {plan['Plan Rows'] ?? '—'}, факт {plan['Actual Rows'] ?? '—'},
      проходов {plan['Actual Loops'] ?? '—'}</div>
    <div>Буферы · {plan['Shared Hit Blocks'] ?? 0} попаданий, {plan['Shared Read Blocks'] ?? 0} чтений</div>
    {plan['Index Cond'] && <code>Index Cond · {plan['Index Cond']}</code>}
    {plan.Filter && <code>Filter · {plan.Filter}</code>}
    {plan['Rows Removed by Filter'] !== undefined && <div>Фильтр отбросил {plan['Rows Removed by Filter']} строк за проход</div>}
    {plan['Rows Removed by Index Recheck'] !== undefined && <div>Повторная проверка индекса отбросила {plan['Rows Removed by Index Recheck']} строк за проход</div>}
    {plan['Heap Fetches'] !== undefined && <div>Обращения к строкам таблицы · {plan['Heap Fetches']}</div>}
    {plan['Sort Method'] && <div>Метод сортировки · {plan['Sort Method']}</div>}
    {plan['Hash Batches'] !== undefined && <div>Пакеты хеш-таблицы · {plan['Hash Batches']}</div>}
    {plan.Plans?.length ? <ul>{plan.Plans.map((child, index) => <PlanNode key={index} plan={child} />)}</ul> : null}
  </li>;
}

export function IndexWorkspace({ lessonSlug, theme }: { lessonSlug: string; theme: 'dark' | 'light' }) {
  const base = '/api/index-lab/lessons/' + lessonSlug;
  const [manifest, setManifest] = useState<Manifest>();
  const [draft, setDraft] = useState('');
  const [error, setError] = useState('');
  const [pending, setPending] = useState<'run' | 'check'>();
  const [preview, setPreview] = useState<Preview>();
  const [grade, setGrade] = useState<{ result: SqlCheckResult; sql: string }>();
  const [completed, setCompleted] = useState(false);
  const latestRequest = useRef<{ sql: string; id: string } | undefined>(undefined);
  const mounted = useRef(false);
  const key = manifest && `pythoria:index:${manifest.lesson_id}:${manifest.task_id}`;

  useEffect(() => {
    mounted.current = true;
    let active = true;
    void request<Manifest>(base).then(data => {
      if (!active) return;
      setManifest(data);
      setCompleted(data.completed);
      const draftKey = `pythoria:index:${data.lesson_id}:${data.task_id}`;
      try { setDraft(localStorage.getItem(draftKey) ?? data.starter); }
      catch { setDraft(data.starter); }
    }).catch(err => { if (active) setError(err.message); });
    return () => { active = false; mounted.current = false; };
  }, [base]);

  function edit(source: string) {
    setDraft(source);
    if (key) {
      try { localStorage.setItem(key, source); }
      catch { setError('Браузер не смог сохранить черновик.'); }
    }
  }

  async function submit(kind: 'run' | 'check') {
    if (pending || !manifest || !draft.trim()) return;
    setError('');
    setPending(kind);
    const sql = draft;
    try {
      if (kind === 'run') {
        const result = await request<Preview>(base + '/run', { sql });
        if (mounted.current) setPreview(result);
      } else {
        if (latestRequest.current?.sql !== sql) latestRequest.current = { sql, id: crypto.randomUUID() };
        const result = await request<SqlCheckResult>(base + '/check', { sql, request_id: latestRequest.current.id });
        if (!mounted.current) return;
        setCompleted(result.completed);
        setGrade({ result, sql });
        latestRequest.current = undefined;
      }
    } catch (err) {
      if (mounted.current) setError(err instanceof Error ? err.message : 'Ошибка запроса');
    } finally {
      if (mounted.current) setPending(undefined);
    }
  }

  return <section className="workspace-pane tx-workspace index-workspace">
    <header className="workspace-toolbar tx-toolbar">
      <strong>Индексы и планы запросов</strong>
      <div>
        <button className="secondary-button" disabled={!!pending} onClick={() => {
          setPreview(undefined);
          setGrade(undefined);
          setError('');
        }}>Reset</button>
        <button className="run-button" disabled={!!pending || !draft.trim()} onClick={() => void submit('run')}>Run</button>
        <button className="check-button" disabled={!!pending || !draft.trim()} onClick={() => void submit('check')}>Check</button>
      </div>
    </header>
    <div className="tx-scroll">
      {completed && <p className="sql-task-completed" role="status">Задание выполнено</p>}
      {pending && <p role="status">{pending === 'run' ? 'Выполняем запросы…' : 'Проверяем независимые наборы…'}</p>}
      {error && <p role="alert">{error}</p>}
      {manifest && <>
        <h3>{manifest.title}</h3>
        <p className="tx-notice">{manifest.prompt}</p>
        <Editor height="200px" language="sql" path={`index/${lessonSlug}.sql`} value={draft} onChange={value => edit(value ?? '')}
          theme={theme === 'dark' ? 'vs-dark' : 'light'} options={{ ariaLabel: 'SQL упражнения', automaticLayout: true,
            wordWrap: 'on', fontSize: 13, minimap: { enabled: false }, scrollBeyondLastLine: false }} />
        <details><summary>Запросы и таблицы</summary>
          <p>users(id, email, region)<br />orders(id, user_id, hotel_id, arrival, created_at, status, total)</p>
          {manifest.queries.map(query => <pre key={query}>{query}</pre>)}
        </details>
      </>}
      {grade && <SqlCheckFeedback result={grade.result} stale={grade.sql !== draft} />}
      {preview && <>
        {preview.definitions.map(([id, definition]) => <pre key={id}>{definition}</pre>)}
        {preview.runs.map((item, index) => <section key={index}>
          {item.error && <p role="alert">{item.sqlstate ? 'SQLSTATE ' + item.sqlstate + ' · PostgreSQL отклонил запрос. Проверьте имена и типы в схеме.' : 'Не удалось собрать результат. Проверьте объём данных и условие запроса.'}</p>}
          {item.result && <SqlResultsTable result={item.result} />}
          {item.plan && <details open><summary>План PostgreSQL</summary><ul className="index-plan"><PlanNode plan={item.plan} /></ul></details>}
          {item.samples?.length ? <p>Время выполнения в мс · {item.samples.join(', ')}. Медиана {item.median_ms}.
            Планирование первого запуска заняло {item.planning_ms} мс.</p> : null}
          {item.baseline_plan && <details><summary>Исходный план</summary>
            <p>Повторные измерения в мс · {item.baseline_samples?.join(', ')}.
              Планирование первого запуска заняло {item.baseline_planning_ms} мс.</p>
            <ul className="index-plan"><PlanNode plan={item.baseline_plan} /></ul>
          </details>}
          {item.controlled && <details><summary>Проверка применимости индекса</summary>
            <p>В контролируемом запуске PostgreSQL получает менее предпочтительный последовательный путь.
              Этот план проверяет доступность индексного пути. Время сравнивается по обычным запускам.</p>
            <ul className="index-plan"><PlanNode plan={item.controlled} /></ul>
          </details>}
        </section>)}
        <p>{preview.estimated ? 'План показывает только оценки. Добавьте ANALYZE и BUFFERS, чтобы увидеть фактические строки и счётчики.' : preview.valid ? 'На публичном наборе условие выполнено.' : 'Публичное наблюдение не выполняет условия задания.'}</p>
      </>}
    </div>
  </section>;
}
