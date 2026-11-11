'use client';

import Editor, { type OnMount } from '@monaco-editor/react';
import type { editor as MonacoEditor } from 'monaco-editor';
import { CirclePlay, Database, FileCode2, RefreshCw, RotateCcw } from 'lucide-react';
import { useCallback, useEffect, useId, useRef, useState } from 'react';

import { sqlApi, SqlApiError } from '../sqlApi';
import { draftKey, loadDraft, sqlPosition } from '../sqlDraft';
import type { SqlCatalog, SqlCheckResult, SqlLesson, SqlResult, SqlSession } from '../sqlTypes';
import { DatabaseExplorer, SqlTableList } from './DatabaseExplorer';
import { SqlResultsTable } from './SqlResultsTable';
import { SqlCheckFeedback } from './SqlCheckFeedback';

type Busy = 'create' | 'run' | 'check' | 'reset' | 'refresh' | 'rows' | null;
interface Lease {
  alive: boolean;
  busy: boolean;
  token: number;
  session: SqlSession | null;
  lesson: SqlLesson | null;
  selected: string;
  pending: Promise<void> | null;
}

function sameSession(value: { session_id: string; generation: number }, session: SqlSession) {
  if (value.session_id !== session.session_id || value.generation !== session.generation) {
    throw new SqlApiError(409, 'stale_generation', 'Сессия изменилась. Создайте её заново.');
  }
}

export function SqlWorkspace({ lessonSlug, theme }: { lessonSlug: string; theme: 'dark' | 'light' }) {
  const [lesson, setLesson] = useState<SqlLesson | null>(null);
  const [session, setSession] = useState<SqlSession | null>(null);
  const [catalog, setCatalog] = useState<SqlCatalog | null>(null);
  const [selected, setSelected] = useState('users');
  const [query, setQuery] = useState('');
  const [executedQuery, setExecutedQuery] = useState('');
  const [result, setResult] = useState<SqlResult | null>(null);
  const [checkResult, setCheckResult] = useState<SqlCheckResult | null>(null);
  const [checkedQuery, setCheckedQuery] = useState('');
  const [completed, setCompleted] = useState(false);
  const [rows, setRows] = useState<SqlResult | null>(null);
  const [offset, setOffset] = useState(0);
  const [busy, setBusy] = useState<Busy>('create');
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(true);
  const [view, setView] = useState<'editor' | 'database' | 'results'>('editor');
  const panelId = useId();
  const workspaceRef = useRef<HTMLElement | null>(null);
  const leaseRef = useRef<Lease | null>(null);
  const queryRef = useRef('');
  const editorRef = useRef<MonacoEditor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<Parameters<OnMount>[1] | null>(null);
  const markersRef = useRef<() => void>(() => undefined);
  const showResultView = useCallback(() => {
    setView(window.innerWidth > 820 && (workspaceRef.current?.clientWidth ?? 0) > 420 ? 'editor' : 'results');
  }, []);

  const saveDraft = useCallback((value: string) => {
    const manifest = leaseRef.current?.lesson;
    if (!manifest) return;
    try {
      localStorage.setItem(draftKey(manifest), value);
      setSaved(true);
    } catch { setSaved(false); }
  }, []);

  const operation = useCallback((lease: Lease, kind: Busy, action: (current: () => boolean) => Promise<void>) => {
    if (lease.busy || !lease.alive) return;
    lease.busy = true;
    const token = ++lease.token;
    const current = () => lease.alive && leaseRef.current === lease && token === lease.token;
    setBusy(kind);
    setError('');
    lease.pending = (async () => {
      try { await action(current); }
      catch (failure) {
        if (current()) {
          setError(failure instanceof Error ? failure.message : 'Не удалось выполнить действие.');
          if (failure instanceof SqlApiError && [404, 410].includes(failure.status) && failure.code !== 'unknown_table') {
            lease.session = null;
            setSession(null); setCatalog(null); setRows(null);
          }
        }
      } finally {
        lease.busy = false;
        if (current()) setBusy(null);
      }
    })();
  }, []);

  const loadExplorer = useCallback(async (lease: Lease, current: () => boolean) => {
    const active = lease.session!;
    const next = await sqlApi.catalog(active);
    sameSession(next, active);
    const table = next.tables.find(t => t.name === lease.selected) ?? next.tables[0];
    if (!table) throw new Error('Учебная схема пуста. Пересоздайте сессию.');
    const page = await sqlApi.rows(active, table.handle);
    sameSession(page, active);
    if (page.error) throw new Error(page.error.message);
    if (current()) {
      lease.selected = table.name;
      setCatalog(next); setSelected(table.name); setRows(page); setOffset(0);
    }
  }, []);

  const connect = useCallback((lease: Lease) => operation(lease, 'create', async current => {
    if (!lease.lesson) {
      const manifest = await sqlApi.lesson(lessonSlug);
      if (!current()) return;
      lease.lesson = manifest;
      let initial = manifest.starter_sql;
      try { const draft = loadDraft(manifest); initial = draft.value; setSaved(draft.saved); }
      catch { setSaved(false); }
      queryRef.current = initial;
      setQuery(initial); setLesson(manifest); setCompleted(!!manifest.completed);
    }
    if (lease.session) {
      await sqlApi.close(lease.session);
      lease.session = null;
      if (current()) { setSession(null); setCatalog(null); setRows(null); }
    }
    const opened = await sqlApi.create(lessonSlug);
    // Retain ownership even after unmount so cleanup can close a late create.
    lease.session = opened;
    if (!current()) return;
    setSession(opened); setResult(null); setCatalog(null); setRows(null);
    await loadExplorer(lease, current);
  }), [lessonSlug, loadExplorer, operation]);

  useEffect(() => {
    const lease: Lease = { alive: true, busy: false, token: 0, session: null, lesson: null, selected: 'users', pending: null };
    leaseRef.current = lease;
    connect(lease);
    const pageHide = () => {
      if (lease.session) void sqlApi.close(lease.session).catch(() => undefined);
    };
    window.addEventListener('pagehide', pageHide);
    return () => {
      window.removeEventListener('pagehide', pageHide);
      lease.alive = false;
      // Let bounded mutations finish before Close. Aborting create/reset can
      // otherwise lose the new session ID/generation and leak a capacity slot.
      void Promise.resolve(lease.pending).finally(async () => {
        if (lease.session) await sqlApi.close(lease.session).catch(() => undefined);
      });
    };
  }, [connect]);

  const run = useCallback(() => {
    const lease = leaseRef.current;
    if (!lease?.session) return;
    operation(lease, 'run', async current => {
      const active = lease.session!;
      const source = queryRef.current;
      const output = await sqlApi.run(active, source);
      sameSession(output, active);
      if (current()) {
        setExecutedQuery(source); setResult(output); showResultView();
        if (output.session_closed) {
          lease.session = null;
          setSession(null); setCatalog(null); setRows(null);
          setError('Сессия завершена после ошибки. Создайте новую — текст запроса сохранён.');
        }
      }
    });
  }, [operation, showResultView]);

  const check = useCallback(() => {
    const lease = leaseRef.current;
    if (!lease?.lesson?.can_check || !queryRef.current.trim()) return;
    operation(lease, 'check', async current => {
      const source = queryRef.current;
      saveDraft(source);
      const output = await sqlApi.check(lessonSlug, lease.lesson!.task_id, source, crypto.randomUUID());
      if (output.task_id !== lease.lesson!.task_id) throw new Error('Ответ относится к другому SQL-заданию. Повторите Check.');
      if (current()) {
        setCheckResult(output); setCheckedQuery(source); setCompleted(output.completed);
        showResultView();
      }
    });
  }, [lessonSlug, operation, saveDraft, showResultView]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (!(event.metaKey || event.ctrlKey)) return;
      if (event.key.toLowerCase() === 's') { event.preventDefault(); event.stopPropagation(); saveDraft(queryRef.current); }
      if (event.key === 'Enter') { event.preventDefault(); event.stopPropagation(); if (event.shiftKey) check(); else run(); }
    };
    // Capture before Monaco's built-in Ctrl+Enter / Ctrl+Shift+Enter line edits.
    window.addEventListener('keydown', onKeyDown, true);
    return () => window.removeEventListener('keydown', onKeyDown, true);
  }, [check, run, saveDraft]);

  const reset = () => {
    const lease = leaseRef.current;
    if (!lease?.session) return;
    operation(lease, 'reset', async current => {
      lease.session = await sqlApi.reset(lease.session!);
      if (!current()) return;
      setSession(lease.session); setResult(null); setCatalog(null); setRows(null);
      await loadExplorer(lease, current);
    });
  };

  const refresh = () => {
    const lease = leaseRef.current;
    if (lease?.session) operation(lease, 'refresh', current => loadExplorer(lease, current));
  };

  const browse = (name: string, pageOffset = 0) => {
    const lease = leaseRef.current;
    const table = catalog?.tables.find(item => item.name === name);
    if (!lease?.session || !table) return;
    operation(lease, 'rows', async current => {
      const active = lease.session!;
      const page = await sqlApi.rows(active, table.handle, pageOffset);
      sameSession(page, active);
      if (page.error) throw new Error(page.error.message);
      if (current()) {
        lease.selected = name;
        setSelected(name); setRows(page); setOffset(pageOffset); setView('database');
      }
    });
  };

  const applyMarkers = useCallback(() => {
    const editor = editorRef.current, monaco = monacoRef.current, model = editor?.getModel();
    if (!monaco || !model) return;
    const issue = query === executedQuery ? result?.error : null;
    const caret = issue?.position ? sqlPosition(query, issue.position) : null;
    monaco.editor.setModelMarkers(model, 'pythoria-sql', issue && caret ? [{
      message: issue.message, severity: monaco.MarkerSeverity.Error,
      startLineNumber: caret.line, startColumn: caret.column,
      endLineNumber: caret.line, endColumn: caret.column + 1,
    }] : []);
  }, [executedQuery, query, result]);

  useEffect(() => { markersRef.current = applyMarkers; applyMarkers(); }, [applyMarkers]);
  const focusPosition = (position: number) => {
    const caret = sqlPosition(executedQuery, position);
    setView('editor');
    requestAnimationFrame(() => {
      if (!leaseRef.current?.alive) return;
      editorRef.current?.setPosition({ lineNumber: caret.line, column: caret.column });
      editorRef.current?.revealLineInCenter(caret.line);
      editorRef.current?.focus();
    });
  };

  return <section ref={workspaceRef} className="workspace-pane sql-workspace" aria-label="SQL Workspace">
    <header className="workspace-toolbar sql-toolbar">
      <div className="workspace-label"><Database size={15} /> SQL Lab <span>PostgreSQL 17 · shop-v1</span></div>
      <div className="workspace-actions">
        <button className="toolbar-button" disabled={!!busy || !session} onClick={refresh} title="Обновить схему и данные"><RefreshCw size={14} /> Refresh</button>
        <button className="toolbar-button" disabled={!!busy || !session} onClick={reset} title="Восстановить исходные данные"><RotateCcw size={14} /> Reset</button>
        <button className="run-button" disabled={!!busy || !session || !query.trim()} onClick={run}><CirclePlay size={15} /> {busy === 'run' ? 'Running…' : 'Run'}</button>
        {lesson?.can_check ? <button className="check-button" disabled={!!busy || !query.trim()} onClick={check}>{busy === 'check' ? 'Checking…' : 'Check'}</button> : null}
      </div>
    </header>
    <div className="sql-guidance"><p>{lesson?.prompt ?? 'Готовим учебную базу…'}</p>
      <small>Run: Ctrl/⌘ + Enter{lesson?.can_check ? ' · Check: Ctrl/⌘ + Shift + Enter' : ''}</small>
      {completed ? <strong className="sql-task-completed" role="status">Задача решена</strong> : null}</div>
    {error ? <div className="sql-connection-error" role="alert"><span>{error}</span><button disabled={!!busy} onClick={() => leaseRef.current && connect(leaseRef.current)}>Создать сессию</button></div> : null}
    <div className="sql-view-tabs" role="tablist" aria-label="SQL Lab">
      {(['editor', 'database', 'results'] as const).map((tab, index, tabs) => <button key={tab} id={`${panelId}-${tab}`} role="tab"
        aria-selected={view === tab} aria-controls={panelId} tabIndex={view === tab ? 0 : -1}
        onKeyDown={event => {
          const next = event.key === 'ArrowRight' ? (index + 1) % tabs.length : event.key === 'ArrowLeft' ? (index + tabs.length - 1) % tabs.length
            : event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : null;
          if (next !== null) { event.preventDefault(); setView(tabs[next]); document.getElementById(`${panelId}-${tabs[next]}`)?.focus(); }
        }}
        onClick={() => setView(tab)}>{tab === 'editor' ? <><FileCode2 size={13} /> query.sql</> : tab === 'database' ? 'База данных' : 'Результаты'}</button>)}
    </div>
    <div className="sql-work-area" id={panelId} role="tabpanel" aria-labelledby={`${panelId}-${view}`} data-view={view} aria-busy={!!busy}>
      <div className="sql-editor" hidden={view !== 'editor'}>
        {lesson ? <Editor path={`sql/${lesson.lesson_id}/${lesson.task_id}/query.sql`} language="sql" value={query}
          theme={theme === 'dark' ? 'vs-dark' : 'light'}
          onChange={value => { const next = value ?? ''; queryRef.current = next; setQuery(next); saveDraft(next); }}
          onMount={(editor, monaco) => { editorRef.current = editor; monacoRef.current = monaco; markersRef.current(); }}
          options={{ automaticLayout: true, fontSize: 13, lineHeight: 21, minimap: { enabled: false },
            scrollBeyondLastLine: false, wordWrap: 'on', padding: { top: 14 }, tabSize: 2, ariaLabel: 'SQL запрос' }} /> : null}
      </div>
      <div className="sql-sidebar" hidden={view !== 'editor'}><SqlTableList catalog={catalog} selected={selected} disabled={!!busy || !session} onSelect={browse} /></div>
      <div className="sql-explorer-panel" hidden={view !== 'database'}><DatabaseExplorer catalog={catalog} selected={selected} disabled={!!busy || !session} onSelect={browse} /></div>
      <section className="sql-output" aria-label={view === 'database' ? 'Данные таблицы' : 'Результаты SQL'}>
        <header><strong>{view === 'database' ? `Данные: ${selected}` : 'Результат SQL'}</strong>
          {view === 'database' && rows ? <div className="sql-pagination">
            <button disabled={!!busy || offset === 0 || !session} onClick={() => browse(selected, Math.max(0, offset - 50))}>Назад</button>
            <span>{rows.rows_returned ? offset + 1 : 0}–{offset + rows.rows_returned}</span>
            <button disabled={!!busy || !rows.has_more || !session} onClick={() => browse(selected, offset + 50)}>Далее</button>
          </div> : null}</header>
        {view !== 'database' && checkResult ? <SqlCheckFeedback result={checkResult} stale={query !== checkedQuery} /> : null}
        {view !== 'database' && busy === 'check' ? <p className="sql-empty" role="status">Проверяем запрос на тестовых наборах…</p> : null}
        {view !== 'database' && result && query !== executedQuery ? <small className="sql-result-info">Результат предыдущего запроса</small> : null}
        {busy === 'run' ? <p className="sql-empty" role="status">Выполняем SELECT…</p>
          : <SqlResultsTable result={view === 'database' ? rows : result} query={executedQuery}
            onPosition={query === executedQuery ? focusPosition : undefined} />}
      </section>
    </div>
    <footer className="sql-footer"><span role="status">{busy === 'create' ? 'Создаём сессию…' : busy === 'check' ? 'Проверяем запрос…' : busy ? 'Обновляем…' : session ? 'Read-only · сессия активна' : 'Сессия не подключена'}</span>
      <span className={saved ? '' : 'sql-save-failed'}>{saved ? 'Сохранено в этом браузере' : 'Сохранение недоступно — скопируйте запрос'}</span></footer>
  </section>;
}
