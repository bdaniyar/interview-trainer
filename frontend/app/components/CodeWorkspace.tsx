'use client';

import Editor from '@monaco-editor/react';
import {
  CheckCircle2,
  ChevronDown,
  CirclePlay,
  FileCode2,
  FilePlus2,
  FolderOpen,
  Pencil,
  Save,
  Sparkles,
  TerminalSquare,
  Trash2,
  X,
  XCircle,
} from 'lucide-react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { api } from '../api';
import type { ExecutionResult } from '../types';

interface Props {
  lessonSlug: string;
  hasTask: boolean;
  hasSolution: boolean;
  files: Record<string, string>;
  theme: 'dark' | 'light';
  onFilesChange: (files: Record<string, string>) => void;
  onSaved: () => Promise<void>;
  onCheckComplete: (result: ExecutionResult) => void;
}

function cleanFileName(value: string) {
  return value.trim().replace(/\\/g, '/').replace(/^\/+/, '');
}

function storedTerminalHeight() {
  if (typeof window === 'undefined') return 164;
  const stored = Number(localStorage.getItem('pythoria-terminal-height'));
  return stored >= 110 && stored <= 360 ? stored : 164;
}

export function CodeWorkspace({ lessonSlug, hasTask, hasSolution, files, theme, onFilesChange, onSaved, onCheckComplete }: Props) {
  const [activeFile, setActiveFile] = useState('main.py');
  const [running, setRunning] = useState<'run' | 'check' | null>(null);
  const [saved, setSaved] = useState(true);
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [solution, setSolution] = useState<Record<string, string> | null>(null);
  const [terminalHeight, setTerminalHeight] = useState(storedTerminalHeight);
  const [terminalReady, setTerminalReady] = useState(false);
  const terminalHostRef = useRef<HTMLDivElement>(null);
  const terminalRef = useRef<import('@xterm/xterm').Terminal | null>(null);
  const fitRef = useRef<import('@xterm/addon-fit').FitAddon | null>(null);
  const filesRef = useRef(files);
  const activeFileRef = useRef(activeFile);
  const commandRef = useRef<(command: string) => void>(() => undefined);

  const fileNames = useMemo(() => Object.keys(files).sort((a, b) => a.localeCompare(b)), [files]);

  useEffect(() => { filesRef.current = files; }, [files]);
  useEffect(() => { activeFileRef.current = activeFile; }, [activeFile]);
  useEffect(() => {
    const timer = window.setTimeout(() => {
      void onSaved().then(() => setSaved(true)).catch(() => setSaved(false));
    }, 800);
    return () => window.clearTimeout(timer);
  }, [files, onSaved]);

  useEffect(() => {
    let disposed = false;
    let disposable: { dispose: () => void } | undefined;
    Promise.all([import('@xterm/xterm'), import('@xterm/addon-fit')]).then(([xterm, fitModule]) => {
      if (disposed || !terminalHostRef.current) return;
      const terminal = new xterm.Terminal({
        convertEol: true,
        cursorBlink: true,
        fontSize: 12,
        lineHeight: 1.35,
        fontFamily: 'var(--font-geist-mono), ui-monospace, monospace',
        theme: theme === 'dark'
          ? { background: '#0b1018', foreground: '#c4ccd8', cursor: '#9c88ff', green: '#48d597', red: '#ff6b7a' }
          : { background: '#f8fafc', foreground: '#253047', cursor: '#6548df', green: '#16865b', red: '#c83849' },
      });
      const fit = new fitModule.FitAddon();
      terminal.loadAddon(fit);
      terminal.open(terminalHostRef.current);
      fit.fit();
      terminal.writeln('\x1b[38;2;156;136;255mPythoria workspace\x1b[0m  Python 3.12');
      terminal.write('\r\n\x1b[38;2;156;136;255m$\x1b[0m ');
      let line = '';
      disposable = terminal.onData((data) => {
        if (data === '\r') {
          terminal.write('\r\n');
          const command = line.trim();
          line = '';
          if (command === 'clear') {
            terminal.clear();
            terminal.write('\x1b[38;2;156;136;255m$\x1b[0m ');
          } else if (command) {
            commandRef.current(command);
          } else {
            terminal.write('\x1b[38;2;156;136;255m$\x1b[0m ');
          }
        } else if (data === '\u007F') {
          if (line.length) {
            line = line.slice(0, -1);
            terminal.write('\b \b');
          }
        } else if (data === '\u000c') {
          terminal.clear();
          terminal.write('\x1b[38;2;156;136;255m$\x1b[0m ' + line);
        } else if (data >= ' ' && data !== '\u007f') {
          line += data;
          terminal.write(data);
        }
      });
      terminalRef.current = terminal;
      fitRef.current = fit;
      setTerminalReady(true);
    });
    return () => {
      disposed = true;
      disposable?.dispose();
      terminalRef.current?.dispose();
      terminalRef.current = null;
      fitRef.current = null;
    };
  }, [lessonSlug, theme]);

  useEffect(() => {
    fitRef.current?.fit();
  }, [terminalHeight, terminalReady]);

  const writeResult = useCallback((execution: ExecutionResult) => {
    const terminal = terminalRef.current;
    if (!terminal) return;
    if (execution.stdout) terminal.write(execution.stdout.replace(/\n/g, '\r\n'));
    if (execution.stderr) terminal.write(`\x1b[31m${execution.stderr.replace(/\n/g, '\r\n')}\x1b[0m`);
    const color = execution.exit_code === 0 ? '\x1b[32m' : '\x1b[31m';
    terminal.writeln(`${color}Process finished with exit code ${execution.exit_code}\x1b[0m  \x1b[90m${execution.duration_ms} ms\x1b[0m`);
    terminal.write('\r\n\x1b[38;2;156;136;255m$\x1b[0m ');
  }, []);

  const save = useCallback(async () => {
    setSaved(false);
    await onSaved();
    setSaved(true);
  }, [onSaved]);

  const run = useCallback(async () => {
    if (running) return;
    setRunning('run');
    setResult(null);
    const entrypoint = activeFileRef.current?.endsWith('.py') ? activeFileRef.current : 'main.py';
    terminalRef.current?.writeln(`\x1b[90m$ python ${entrypoint}\x1b[0m`);
    try {
      await onSaved();
      const execution = await api.run(lessonSlug, filesRef.current, entrypoint);
      setResult(execution);
      writeResult(execution);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Ошибка запуска';
      const execution = { stdout: '', stderr: message + '\n', exit_code: 1, timed_out: false, duration_ms: 0 };
      setResult(execution);
      writeResult(execution);
    } finally {
      setRunning(null);
    }
  }, [lessonSlug, onSaved, running, writeResult]);

  const check = useCallback(async () => {
    if (running || !hasTask) return;
    setRunning('check');
    setResult(null);
    terminalRef.current?.writeln('\x1b[90m$ pytest hidden tests\x1b[0m');
    try {
      await onSaved();
      const execution = await api.check(lessonSlug, filesRef.current);
      setResult(execution);
      writeResult(execution);
      onCheckComplete(execution);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Ошибка проверки';
      const execution = { stdout: '', stderr: message + '\n', exit_code: 1, timed_out: false, duration_ms: 0, passed: false };
      setResult(execution);
      writeResult(execution);
    } finally {
      setRunning(null);
    }
  }, [hasTask, lessonSlug, onCheckComplete, onSaved, running, writeResult]);

  const executeTerminal = useCallback(async (command: string) => {
    try {
      const execution = await api.terminal(lessonSlug, filesRef.current, command);
      writeResult(execution);
    } catch (error) {
      terminalRef.current?.writeln(`\x1b[31m${error instanceof Error ? error.message : 'Command failed'}\x1b[0m`);
      terminalRef.current?.write('\r\n\x1b[38;2;156;136;255m$\x1b[0m ');
    }
  }, [lessonSlug, writeResult]);
  useEffect(() => { commandRef.current = executeTerminal; }, [executeTerminal]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (!(event.metaKey || event.ctrlKey) || event.key !== 'Enter') {
        if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 's') {
          event.preventDefault();
          void save();
        }
        return;
      }
      event.preventDefault();
      if (event.shiftKey) void check(); else void run();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [check, run, save]);

  const updateActive = (value: string | undefined) => {
    if (!activeFile) return;
    onFilesChange({ ...files, [activeFile]: value ?? '' });
    setSaved(false);
  };

  const createFile = () => {
    const name = cleanFileName(window.prompt('Имя файла', 'service.py') ?? '');
    if (!name || files[name] !== undefined || name.includes('..') || !name.endsWith('.py')) return;
    onFilesChange({ ...files, [name]: '# Новый файл\n' });
    setActiveFile(name);
    setSaved(false);
  };

  const renameFile = () => {
    if (!activeFile) return;
    const name = cleanFileName(window.prompt('Новое имя', activeFile) ?? '');
    if (!name || name === activeFile || files[name] !== undefined || name.includes('..') || !name.endsWith('.py')) return;
    const next = { ...files, [name]: files[activeFile] };
    delete next[activeFile];
    onFilesChange(next);
    setActiveFile(name);
    setSaved(false);
  };

  const deleteFile = () => {
    if (!activeFile || activeFile === 'main.py' || !window.confirm(`Удалить ${activeFile}?`)) return;
    const next = { ...files };
    delete next[activeFile];
    onFilesChange(next);
    setActiveFile('main.py');
    setSaved(false);
  };

  const revealSolution = async () => {
    try {
      setSolution((await api.solution(lessonSlug)).files);
    } catch (error) {
      terminalRef.current?.writeln(`\x1b[31m${error instanceof Error ? error.message : 'Решение недоступно'}\x1b[0m`);
    }
  };

  const startTerminalResize = (event: React.PointerEvent) => {
    const startY = event.clientY;
    const startHeight = terminalHeight;
    let latest = startHeight;
    const move = (next: PointerEvent) => {
      latest = Math.min(360, Math.max(110, startHeight + startY - next.clientY));
      setTerminalHeight(latest);
    };
    const up = () => {
      localStorage.setItem('pythoria-terminal-height', String(latest));
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };

  return (
    <section className="workspace-pane">
      <div className="workspace-toolbar">
        <div className="workspace-label"><Code2Icon /> Практика <span>{lessonSlug}</span></div>
        <div className="workspace-actions">
          <span className={`save-status ${saved ? '' : 'dirty'}`}>{saved ? 'Сохранено' : 'Не сохранено'}</span>
          {hasSolution ? <button className="toolbar-button solution-button" onClick={revealSolution}><Sparkles size={14} /> Верное решение</button> : null}
          <button className="toolbar-button" onClick={() => void save()}><Save size={14} /> Save</button>
          <button className="run-button" onClick={() => void run()} disabled={Boolean(running)}><CirclePlay size={15} /> {running === 'run' ? 'Running…' : 'Run'}</button>
          <button className="check-button" onClick={() => void check()} disabled={Boolean(running) || !hasTask}>{running === 'check' ? 'Проверяем…' : 'Проверить'}</button>
        </div>
      </div>

      <div className="workbench-body" style={{ gridTemplateRows: `minmax(140px, 1fr) 5px ${terminalHeight}px` }}>
        <div className="ide-grid">
          <aside className="files-panel">
            <div className="files-heading"><span>FILES</span><div><button onClick={createFile} title="Новый файл"><FilePlus2 size={13} /></button><button onClick={renameFile} title="Переименовать"><Pencil size={12} /></button><button onClick={deleteFile} title="Удалить"><Trash2 size={12} /></button></div></div>
            <div className="folder-row"><ChevronDown size={13} /><FolderOpen size={14} /> solution</div>
            {fileNames.map((name) => (
              <button className={`file-row ${name === activeFile ? 'active' : ''}`} key={name} onClick={() => setActiveFile(name)}>
                <FileCode2 size={13} /><span>{name}</span>{files[name] !== undefined && name === activeFile && !saved ? <i>●</i> : null}
              </button>
            ))}
          </aside>
          <div className="editor-panel">
            <div className="editor-tabs">
              {fileNames.map((name) => (
                <button key={name} className={name === activeFile ? 'active' : ''} onClick={() => setActiveFile(name)}><FileCode2 size={12} />{name}{name === activeFile ? <span>×</span> : null}</button>
              ))}
            </div>
            {activeFile ? (
              <Editor
                key={`${lessonSlug}:${activeFile}`}
                path={`${lessonSlug}/${activeFile}`}
                language={activeFile.endsWith('.py') ? 'python' : 'plaintext'}
                value={files[activeFile] ?? ''}
                onChange={updateActive}
                theme={theme === 'dark' ? 'vs-dark' : 'light'}
                options={{
                  automaticLayout: true,
                  fontSize: 13,
                  lineHeight: 21,
                  fontFamily: 'var(--font-geist-mono), ui-monospace, monospace',
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  smoothScrolling: true,
                  padding: { top: 14 },
                  tabSize: 4,
                  insertSpaces: true,
                  wordWrap: 'on',
                }}
              />
            ) : null}
          </div>
        </div>
        <div className="horizontal-resizer terminal-resizer" onPointerDown={startTerminalResize} />
        <section className="terminal-panel">
          <header><div><TerminalSquare size={13} /><span>TERMINAL</span></div><div className="terminal-result-summary">
            {result?.tests_total ? <span className={result.passed ? 'passed' : 'failed'}>{result.tests_passed} / {result.tests_total} tests</span> : null}
            {result ? <span>exit {result.exit_code}</span> : null}
          </div></header>
          {result?.tests?.length ? <div className="test-strip">{result.tests.map((test) => <span key={test.name} className={test.passed ? 'passed' : 'failed'}>{test.passed ? <CheckCircle2 size={12} /> : <XCircle size={12} />}{test.name}</span>)}</div> : null}
          <div ref={terminalHostRef} className="xterm-host" />
        </section>
      </div>

      {solution ? (
        <div className="solution-popover">
          <header><div><Sparkles size={16} /> Верное решение</div><button onClick={() => setSolution(null)}><X size={16} /></button></header>
          {Object.entries(solution).map(([name, content]) => <div key={name}><b>{name}</b><pre><code>{content}</code></pre></div>)}
        </div>
      ) : null}
    </section>
  );
}

function Code2Icon() {
  return <FileCode2 size={14} />;
}
