'use client';

import {
  Bot,
  BookOpenCheck,
  Check,
  ChevronDown,
  ChevronRight,
  Circle,
  Flame,
  GraduationCap,
  Menu,
  Moon,
  PanelLeftClose,
  PanelLeftOpen,
  Search,
  Sun,
  Trophy,
  X,
} from 'lucide-react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { api } from '../api';
import { resumeTrack, trackForLesson, trackModules } from '../courseTracks';
import type { CourseData, CourseTrack, ExecutionResult, LessonData, LessonSummary } from '../types';
import { CodeWorkspace } from './CodeWorkspace';
import { InterviewModal } from './InterviewModal';
import { MarkdownLesson } from './MarkdownLesson';
import { SqlWorkspace } from './SqlWorkspace';
import { IndexWorkspace } from './IndexWorkspace';
import { TransactionWorkspace } from './TransactionWorkspace';

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

function storedNumber(key: string, fallback: number, min: number, max: number) {
  if (typeof window === 'undefined') return fallback;
  const stored = Number(localStorage.getItem(key));
  return stored ? clamp(stored, min, max) : fallback;
}

export function CourseApp() {
  const [course, setCourse] = useState<CourseData | null>(null);
  const [lesson, setLesson] = useState<LessonData | null>(null);
  const [activeSlug, setActiveSlug] = useState('');
  const [files, setFiles] = useState<Record<string, string>>({});
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [error, setError] = useState('');
  const [loadingLesson, setLoadingLesson] = useState(true);
  const [sidebarWidth, setSidebarWidth] = useState(() => storedNumber('pythoria-sidebar-width', 278, 220, 420));
  const [workspaceRatio, setWorkspaceRatio] = useState(() => storedNumber('pythoria-workspace-ratio', 50, 34, 72));
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [expandedModules, setExpandedModules] = useState<Set<string>>(new Set());
  const [interviewOpen, setInterviewOpen] = useState(false);
  const [mentorOpen, setMentorOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [toast, setToast] = useState('');
  const filesRef = useRef(files);
  const activeSlugRef = useRef(activeSlug);
  const loadedLessonRef = useRef<LessonData | null>(null);
  const navigationRequest = useRef(0);
  const completionRequest = useRef(0);

  const track = course ? trackForLesson(course, activeSlug) ?? 'backend' : 'backend';
  const aiTrack = track === 'ai-engineering';
  const modules = useMemo(() => course ? trackModules(course, track) : [], [course, track]);
  const summary = aiTrack ? course?.ai?.summary : course?.summary;
  const flattened = useMemo(() => modules.flatMap((module) => module.lessons), [modules]);
  const activePosition = flattened.findIndex((item) => item.slug === activeSlug) + 1;

  useEffect(() => { filesRef.current = files; }, [files]);

  const applyCourse = useCallback((data: CourseData) => {
    setCourse(data);
    const storedTheme = localStorage.getItem('pythoria-theme') as 'dark' | 'light' | null;
    setTheme(storedTheme ?? data.summary.theme ?? 'dark');
    const querySlug = new URLSearchParams(window.location.search).get('lesson');
    const preferred = localStorage.getItem('pythoria-track') === 'ai-engineering' ? 'ai-engineering' : 'backend';
    const slug = querySlug && trackForLesson(data, querySlug) ? querySlug
      : resumeTrack(data, preferred, localStorage.getItem('pythoria-ai-lesson')) || resumeTrack(data, 'backend', null);
    setActiveSlug((current) => current || slug);
  }, []);

  const loadCourse = useCallback(() => api.course().then(applyCourse), [applyCourse]);

  useEffect(() => {
    api.course().then(applyCourse).catch((err: Error) => setError(err.message));
  }, [applyCourse]);

  useEffect(() => {
    if (!activeSlug) return;
    activeSlugRef.current = activeSlug;
    let cancelled = false;
    Promise.all([api.lesson(activeSlug), api.openLesson(activeSlug)])
      .then(([data]) => {
        if (cancelled) return;
        loadedLessonRef.current = data;
        filesRef.current = data.files;
        setLesson(data);
        setExpandedModules((current) => new Set(current).add(data.module_slug));
        const nextTrack = data.tracks?.includes('ai-engineering') ? 'ai-engineering' : 'backend';
        localStorage.setItem('pythoria-track', nextTrack);
        localStorage.setItem(`pythoria-${nextTrack}-lesson`, data.slug);
        setFiles(data.files);
        setLoadingLesson(false);
        window.history.replaceState({}, '', `?lesson=${activeSlug}`);
        setSidebarOpen(false);
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setError(err.message);
          setLoadingLesson(false);
        }
      });
    return () => { cancelled = true; };
  }, [activeSlug]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(''), 3200);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const saveFiles = useCallback(async () => {
    const loaded = loadedLessonRef.current;
    if (!loaded || (loaded.workspace_kind && loaded.workspace_kind !== 'python')) return;
    await api.saveFiles(loaded.slug, filesRef.current);
  }, []);

  const selectLesson = useCallback((slug: string) => {
    if (!slug || slug === activeSlugRef.current) return;
    const request = ++navigationRequest.current;
    setLoadingLesson(true);
    setError('');
    setMentorOpen(false);
    void saveFiles().catch(() => undefined).finally(() => {
      if (navigationRequest.current !== request) return;
      activeSlugRef.current = slug;
      setActiveSlug(slug);
    });
  }, [saveFiles]);

  const selectTrack = (next: CourseTrack) => {
    if (!course || track === next) return;
    const remembered = localStorage.getItem(`pythoria-${next}-lesson`);
    const slug = remembered && trackForLesson(course, remembered) === next
      ? remembered : resumeTrack(course, next, null);
    setSearch('');
    selectLesson(slug);
  };

  const refreshCourseAndLesson = useCallback(async (slug: string) => {
    const request = ++completionRequest.current;
    const [courseData, lessonData] = await Promise.all([api.course(), api.lesson(slug)]);
    if (completionRequest.current !== request) return;
    setCourse(courseData);
    if (activeSlugRef.current === slug && loadedLessonRef.current?.slug === slug) setLesson(lessonData);
  }, []);

  const completeTheory = async () => {
    if (!lesson) return;
    const slug = lesson.slug;
    try {
      const result = await api.completeTheory(slug);
      setToast(result.xp_awarded ? `Теория пройдена · +${result.xp_awarded} XP` : 'Теория уже отмечена');
      await refreshCourseAndLesson(slug);
    } catch (err) {
      setToast(err instanceof Error ? err.message : 'Не удалось сохранить прогресс');
    }
  };

  const onCheckComplete = async (slug: string, result: ExecutionResult) => {
    if (activeSlugRef.current === slug && result.passed) setToast(result.xp_awarded ? `Верное решение · +${result.xp_awarded} XP` : 'Верное решение');
    else if (activeSlugRef.current === slug) setToast(`${result.tests_passed ?? 0} / ${result.tests_total ?? 0} tests passed`);
    await refreshCourseAndLesson(slug);
  };

  const switchTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    localStorage.setItem('pythoria-theme', next);
    void api.setTheme(next).catch(() => undefined);
  };

  const navigate = (direction: -1 | 1) => {
    const next = flattened[activePosition - 1 + direction];
    if (next) selectLesson(next.slug);
  };

  const toggleModule = (slug: string) => {
    setExpandedModules((current) => {
      const next = new Set(current);
      if (next.has(slug)) next.delete(slug); else next.add(slug);
      return next;
    });
  };

  const startSidebarResize = (event: React.PointerEvent) => {
    const startX = event.clientX;
    const startWidth = sidebarWidth;
    let latest = startWidth;
    const move = (next: PointerEvent) => {
      latest = clamp(startWidth + next.clientX - startX, 220, 420);
      setSidebarWidth(latest);
    };
    const up = () => {
      localStorage.setItem('pythoria-sidebar-width', String(latest));
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };

  const startWorkspaceResize = (event: React.PointerEvent) => {
    const container = (event.currentTarget.parentElement as HTMLElement).getBoundingClientRect();
    let latest = workspaceRatio;
    const move = (next: PointerEvent) => {
      latest = clamp(((container.right - next.clientX) / container.width) * 100, 34, 72);
      setWorkspaceRatio(latest);
    };
    const up = () => {
      localStorage.setItem('pythoria-workspace-ratio', String(latest));
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };

  if (error && !course) {
    return (
      <main className={`connection-screen ${theme}`}>
        <div className="brand-mark">P</div>
        <h1>Backend пока недоступен</h1>
        <p>{error}. Запусти все сервисы через Docker Compose или локальный dev-режим.</p>
        <button className="primary-button" onClick={() => { setError(''); void loadCourse().catch((err: Error) => setError(err.message)); }}>Повторить</button>
      </main>
    );
  }

  if (!course || !summary || !activeSlug) {
    return <main className={`loading-screen ${theme}`}><div className="brand-mark pulse">P</div><p>Загружаем курс…</p></main>;
  }

  const filteredModules = search.trim()
    ? modules.map((module) => ({ ...module, lessons: module.lessons.filter((item) => item.title.toLowerCase().includes(search.trim().toLowerCase())) })).filter((module) => module.lessons.length)
    : modules;

  return (
    <main className={`course-app ${theme} ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`} style={{ '--sidebar-width': `${sidebarWidth}px` } as React.CSSProperties}>
      <header className="topbar">
        <div className="brand">
          <button className="mobile-menu" aria-label="Содержание трека" onClick={() => setSidebarOpen(true)}><Menu size={18} /></button>
          <span className="brand-mark">P</span><span className="brand-name">PYTHORIA</span>
          <button className="collapse-button" onClick={() => setSidebarCollapsed(!sidebarCollapsed)} title="Свернуть sidebar">{sidebarCollapsed ? <PanelLeftOpen size={16} /> : <PanelLeftClose size={16} />}</button>
        </div>
        <div className="course-title">
          <select aria-label="Учебный трек" value={track} onChange={(event) => selectTrack(event.target.value as CourseTrack)}>
            <option value="backend">Python Backend</option>
            {course.ai?.modules.length ? <option value="ai-engineering">AI Engineering</option> : null}
          </select>
          <small>{summary.completed} / {summary.total} уроков</small>
        </div>
        <div className="top-actions">
          <span className="streak"><Flame size={14} /> 3 дня</span>
          <span className="xp"><Trophy size={14} /> {course.summary.xp} XP</span>
          <button className="icon-button" onClick={switchTheme} aria-label="Сменить тему">{theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}</button>
          <span className="avatar">DA</span>
        </div>
      </header>

      <div className="learning-grid">
        <aside className={`course-sidebar ${sidebarOpen ? 'mobile-open' : ''}`}>
          <div className="mobile-sidebar-head"><b>Содержание</b><button onClick={() => setSidebarOpen(false)}><X size={17} /></button></div>
          <div className="course-progress">
            <div className="progress-copy"><span>Прогресс курса</span><b>{summary.percent}%</b></div>
            <div className="progress-track"><span style={{ width: `${summary.percent}%` }} /></div>
            <small>{summary.completed} уроков завершено</small>
          </div>
          <label className="lesson-search"><Search size={14} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Найти урок…" /></label>
          <nav>
            {filteredModules.map((module) => {
              const expanded = search ? true : expandedModules.has(module.slug);
              return (
                <section className="sidebar-module" key={module.slug}>
                  <button className="module-heading" onClick={() => toggleModule(module.slug)}>
                    <span>{aiTrack ? module.slug.replace('ai-stage-', 'AI') : String(module.order).padStart(2, '0')}</span><strong>{module.title}</strong>{expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                  </button>
                  {expanded ? <div className="lesson-list">{module.lessons.map((item) => <LessonRow key={item.slug} lesson={item} active={item.slug === activeSlug} onClick={() => selectLesson(item.slug)} />)}</div> : null}
                </section>
              );
            })}
          </nav>
          {aiTrack && course.ai ? <details className="ai-roadmap">
            <summary>План трека · {course.ai.roadmap.reduce((total, item) => total + item.planned, 0)} запланировано</summary>
            <ul>{course.ai.roadmap.filter((item) => item.planned).map((item) => (
              <li key={item.slug}>{item.title} · {item.planned}</li>
            ))}</ul>
          </details> : <button className="interview-link" onClick={() => setInterviewOpen(true)}><GraduationCap size={16} /><span><b>Режим собеседования</b><small>Оригинальные вопросы курса</small></span><ChevronRight size={14} /></button>}
        </aside>

        <div className="vertical-resizer sidebar-resizer" onPointerDown={startSidebarResize} />

        <div className="content-stack" style={{ gridTemplateColumns: `minmax(260px, ${100 - workspaceRatio}fr) 5px minmax(340px, ${workspaceRatio}fr)` }}>
          <section className="lesson-pane">
            <div className="lesson-toolbar">
              <div><span className="eyebrow">МОДУЛЬ {modules.findIndex((module) => module.slug === lesson?.module_slug) + 1} · УРОК {activePosition}</span><strong>{lesson?.number ? `${lesson.number} · ` : ''}{lesson?.title ?? 'Загрузка…'}</strong></div>
              <div className="toolbar-actions">
                <button className={`mentor-button ${mentorOpen ? 'active' : ''}`} onClick={() => setMentorOpen(!mentorOpen)}><Bot size={15} /> AI-ментор</button>
                <span>{activePosition} / {summary.total}</span>
              </div>
            </div>
            {loadingLesson || !lesson ? <div className="lesson-loading"><div /><div /><div /></div> : (
              <MarkdownLesson key={lesson.slug} lesson={lesson} theme={theme} position={activePosition} total={summary.total} onCompleteTheory={() => void completeTheory()} onNavigate={navigate} />
            )}
            {mentorOpen && lesson ? <aside className="mentor-card"><header><Bot size={16} /><b>AI-ментор</b><button onClick={() => setMentorOpen(false)}><X size={14} /></button></header><p>Начни с контракта задачи. Для темы <b>{lesson.topics[0]}</b> проверь граничные случаи и не меняй публичную сигнатуру.</p><div className="mentor-tip"><BookOpenCheck size={14} /> {lesson.workspace_kind === 'sql' ? 'Открой схему базы, выбери столбцы и проверь результат через Run.' : 'Запусти Check: тесты укажут, какой сценарий ещё не покрыт.'}</div></aside> : null}
          </section>
          <div
            className="vertical-resizer workspace-resizer"
            role="separator"
            aria-label="Изменить ширину IDE"
            aria-orientation="vertical"
            onPointerDown={startWorkspaceResize}
          />
          {!loadingLesson && lesson?.workspace_kind === 'project' ?
            <section className="workspace-pane tx-workspace pool-practice">
              <header className="workspace-toolbar tx-toolbar"><strong>Практика FastAPI и PostgreSQL</strong></header>
              <div className="tx-scroll">
                <p>Откройте <code>projects/pool_lab</code> в репозитории.</p>
                <p>Исправьте утечку сессии в копии <code>starter.py</code>.
                  Запустите проверку с двумя HTTP-запросами и пулом на одно соединение.</p>
                <pre>./check.sh answer.py</pre>
                <p>Команда использует локальный Docker. Результат появится в терминале.</p>
              </div>
            </section> : !loadingLesson && lesson?.workspace_kind === 'index' ?
            <IndexWorkspace key={lesson.slug} lessonSlug={lesson.slug} theme={theme} /> : !loadingLesson && lesson?.workspace_kind === 'postgres_examples' ?
            <section className="workspace-pane tx-workspace postgres-examples">
              <header className="workspace-toolbar tx-toolbar"><strong>Примеры PostgreSQL</strong></header>
              <div className="tx-scroll">
                <p className="tx-notice">В разделе «Примеры кода» есть запросы и ожидаемые результаты.</p>
                <p className="tx-notice">Запустите проверку из корня репозитория. Скрипт сверит результаты на учебной базе Docker.</p>
                <pre className="postgres-examples-command"><code>scripts/test_stage11_examples.sh</code></pre>
              </div>
            </section> : !loadingLesson && lesson?.workspace_kind === 'transaction' ?
            <TransactionWorkspace key={lesson.slug} lessonSlug={lesson.slug} theme={theme} /> : !loadingLesson && lesson?.workspace_kind === 'sql' ? <SqlWorkspace key={lesson.slug} lessonSlug={lesson.slug} theme={theme} /> : !loadingLesson && lesson ? (
            <CodeWorkspace
              key={lesson.slug}
              lessonSlug={lesson.slug}
              hasTask={lesson.has_task}
              hasSolution={lesson.has_solution}
              files={files}
              theme={theme}
              onFilesChange={setFiles}
              onSaved={saveFiles}
              onCheckComplete={(result) => void onCheckComplete(lesson.slug, result)}
            />
          ) : <div />}
        </div>
      </div>

      {interviewOpen ? <InterviewModal onClose={() => setInterviewOpen(false)} onXp={(xp) => setCourse((current) => current ? { ...current, summary: { ...current.summary, xp } } : current)} /> : null}
      {toast ? <div className="toast"><Check size={15} /> {toast}</div> : null}
      {sidebarOpen ? <button className="sidebar-scrim" aria-label="Закрыть sidebar" onClick={() => setSidebarOpen(false)} /> : null}
    </main>
  );
}

function LessonRow({ lesson, active, onClick }: { lesson: LessonSummary; active: boolean; onClick: () => void }) {
  const statusIcon = lesson.status === 'completed' ? <Check size={11} /> : lesson.status === 'in_progress' ? <span className="progress-dot" /> : <Circle size={9} />;
  return <button className={`lesson ${active ? 'active' : ''}`} onClick={onClick}><span className={`lesson-state ${lesson.status}`}>{statusIcon}</span><span>{lesson.title}</span><span className="lesson-badges">{lesson.priority ? <span className={'priority-badge ' + lesson.priority.toLowerCase()}>{lesson.priority}</span> : null}{lesson.has_task ? <span className="code-badge">CODE</span> : null}</span></button>;
}
