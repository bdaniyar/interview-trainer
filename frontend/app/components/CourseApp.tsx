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
import type { CourseData, ExecutionResult, LessonData, LessonSummary } from '../types';
import { CodeWorkspace } from './CodeWorkspace';
import { InterviewModal } from './InterviewModal';
import { MarkdownLesson } from './MarkdownLesson';

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

  const flattened = useMemo(() => course?.modules.flatMap((module) => module.lessons) ?? [], [course]);
  const activePosition = flattened.findIndex((item) => item.slug === activeSlug) + 1;

  useEffect(() => { filesRef.current = files; }, [files]);
  useEffect(() => { activeSlugRef.current = activeSlug; }, [activeSlug]);

  const applyCourse = useCallback((data: CourseData) => {
    setCourse(data);
    const storedTheme = localStorage.getItem('pythoria-theme') as 'dark' | 'light' | null;
    setTheme(storedTheme ?? data.summary.theme ?? 'dark');
    const querySlug = new URLSearchParams(window.location.search).get('lesson');
    const exists = data.modules.some((module) => module.lessons.some((item) => item.slug === querySlug));
    setActiveSlug((current) => current || (exists && querySlug ? querySlug : data.summary.last_opened_lesson));
    setExpandedModules((current) => current.size ? current : new Set([data.modules[0]?.slug]));
  }, []);

  const loadCourse = useCallback(() => api.course().then(applyCourse), [applyCourse]);

  useEffect(() => {
    api.course().then(applyCourse).catch((err: Error) => setError(err.message));
  }, [applyCourse]);

  useEffect(() => {
    if (!activeSlug) return;
    let cancelled = false;
    Promise.all([api.lesson(activeSlug), api.openLesson(activeSlug)])
      .then(([data]) => {
        if (cancelled) return;
        setLesson(data);
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
    if (!activeSlugRef.current) return;
    await api.saveFiles(activeSlugRef.current, filesRef.current);
  }, []);

  const selectLesson = useCallback((slug: string) => {
    if (!slug || slug === activeSlugRef.current) return;
    setLoadingLesson(true);
    setMentorOpen(false);
    void saveFiles().catch(() => undefined).finally(() => setActiveSlug(slug));
  }, [saveFiles]);

  const refreshCourseAndLesson = useCallback(async () => {
    const [courseData, lessonData] = await Promise.all([api.course(), api.lesson(activeSlugRef.current)]);
    setCourse(courseData);
    setLesson(lessonData);
  }, []);

  const completeTheory = async () => {
    if (!lesson) return;
    try {
      const result = await api.completeTheory(lesson.slug);
      setToast(result.xp_awarded ? `Теория пройдена · +${result.xp_awarded} XP` : 'Теория уже отмечена');
      await refreshCourseAndLesson();
    } catch (err) {
      setToast(err instanceof Error ? err.message : 'Не удалось сохранить прогресс');
    }
  };

  const onCheckComplete = async (result: ExecutionResult) => {
    if (result.passed) setToast(result.xp_awarded ? `Верное решение · +${result.xp_awarded} XP` : 'Верное решение');
    else setToast(`${result.tests_passed ?? 0} / ${result.tests_total ?? 0} tests passed`);
    await refreshCourseAndLesson();
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

  if (!course || !activeSlug) {
    return <main className={`loading-screen ${theme}`}><div className="brand-mark pulse">P</div><p>Загружаем курс…</p></main>;
  }

  const filteredModules = search.trim()
    ? course.modules.map((module) => ({ ...module, lessons: module.lessons.filter((item) => item.title.toLowerCase().includes(search.toLowerCase())) })).filter((module) => module.lessons.length)
    : course.modules;

  return (
    <main className={`course-app ${theme} ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`} style={{ '--sidebar-width': `${sidebarWidth}px` } as React.CSSProperties}>
      <header className="topbar">
        <div className="brand">
          <button className="mobile-menu" onClick={() => setSidebarOpen(true)}><Menu size={18} /></button>
          <span className="brand-mark">P</span><span className="brand-name">PYTHORIA</span>
          <button className="collapse-button" onClick={() => setSidebarCollapsed(!sidebarCollapsed)} title="Свернуть sidebar">{sidebarCollapsed ? <PanelLeftOpen size={16} /> : <PanelLeftClose size={16} />}</button>
        </div>
        <div className="course-title"><span>{course.title}</span><small>{course.summary.completed} / {course.summary.total} уроков</small></div>
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
            <div className="progress-copy"><span>Прогресс курса</span><b>{course.summary.percent}%</b></div>
            <div className="progress-track"><span style={{ width: `${course.summary.percent}%` }} /></div>
            <small>{course.summary.completed} уроков завершено</small>
          </div>
          <label className="lesson-search"><Search size={14} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Найти урок…" /></label>
          <nav>
            {filteredModules.map((module) => {
              const expanded = search ? true : expandedModules.has(module.slug);
              return (
                <section className="sidebar-module" key={module.slug}>
                  <button className="module-heading" onClick={() => toggleModule(module.slug)}>
                    <span>{String(module.order).padStart(2, '0')}</span><strong>{module.title}</strong>{expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                  </button>
                  {expanded ? <div className="lesson-list">{module.lessons.map((item) => <LessonRow key={item.slug} lesson={item} active={item.slug === activeSlug} onClick={() => selectLesson(item.slug)} />)}</div> : null}
                </section>
              );
            })}
          </nav>
          <button className="interview-link" onClick={() => setInterviewOpen(true)}><GraduationCap size={16} /><span><b>Режим собеседования</b><small>Оригинальные вопросы курса</small></span><ChevronRight size={14} /></button>
        </aside>

        <div className="vertical-resizer sidebar-resizer" onPointerDown={startSidebarResize} />

        <div className="content-stack" style={{ gridTemplateColumns: `minmax(260px, ${100 - workspaceRatio}fr) 5px minmax(340px, ${workspaceRatio}fr)` }}>
          <section className="lesson-pane">
            <div className="lesson-toolbar">
              <div><span className="eyebrow">МОДУЛЬ {course.modules.findIndex((module) => module.slug === lesson?.module_slug) + 1} · УРОК {activePosition}</span><strong>{lesson?.title ?? 'Загрузка…'}</strong></div>
              <div className="toolbar-actions">
                <button className={`mentor-button ${mentorOpen ? 'active' : ''}`} onClick={() => setMentorOpen(!mentorOpen)}><Bot size={15} /> AI-ментор</button>
                <span>{activePosition} / {course.summary.total}</span>
              </div>
            </div>
            {loadingLesson || !lesson ? <div className="lesson-loading"><div /><div /><div /></div> : (
              <MarkdownLesson lesson={lesson} theme={theme} position={activePosition} total={course.summary.total} onCompleteTheory={() => void completeTheory()} onNavigate={navigate} />
            )}
            {mentorOpen && lesson ? <aside className="mentor-card"><header><Bot size={16} /><b>AI-ментор</b><button onClick={() => setMentorOpen(false)}><X size={14} /></button></header><p>Начни с контракта задачи. Для темы <b>{lesson.topics[0]}</b> проверь граничные случаи и не меняй публичную сигнатуру.</p><div className="mentor-tip"><BookOpenCheck size={14} /> Запусти Check: тесты укажут, какой сценарий ещё не покрыт.</div></aside> : null}
          </section>
          <div
            className="vertical-resizer workspace-resizer"
            role="separator"
            aria-label="Изменить ширину IDE"
            aria-orientation="vertical"
            onPointerDown={startWorkspaceResize}
          />
          {lesson ? (
            <CodeWorkspace
              key={lesson.slug}
              lessonSlug={lesson.slug}
              hasTask={lesson.has_task}
              hasSolution={lesson.has_solution}
              files={files}
              theme={theme}
              onFilesChange={setFiles}
              onSaved={saveFiles}
              onCheckComplete={(result) => void onCheckComplete(result)}
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
