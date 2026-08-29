'use client';

import { BookOpen, Brain, Check, ChevronLeft, ChevronRight, Clock3, Code2, Sparkles } from 'lucide-react';
import { useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import remarkGfm from 'remark-gfm';

import type { LessonData } from '../types';

interface Props {
  lesson: LessonData;
  theme: 'dark' | 'light';
  position: number;
  total: number;
  onCompleteTheory: () => void;
  onNavigate: (direction: -1 | 1) => void;
}

type LessonMode = 'learn' | 'review';

interface MarkdownSection {
  title: string;
  body: string;
}

const REVIEW_SECTION = /practice|prediction|задача|interview|good answers|answer rubric/i;
const COLLAPSED_SECTION = /mental model|good answers|answer rubric|sources/i;

function splitSections(markdown: string): { intro: string; sections: MarkdownSection[] } {
  const matches = [...markdown.matchAll(/^## (.+)$/gm)];
  if (!matches.length) return { intro: markdown, sections: [] };
  const intro = markdown.slice(0, matches[0].index).trim();
  const sections = matches.map((match, index) => {
    const start = (match.index ?? 0) + match[0].length;
    const end = matches[index + 1]?.index ?? markdown.length;
    return { title: match[1].trim(), body: markdown.slice(start, end).trim() };
  });
  return { intro, sections };
}

interface MarkdownContentProps {
  source: string;
  theme: 'dark' | 'light';
}

function MarkdownContent({ source, theme }: MarkdownContentProps) {
  const renderMarkdown = (value: string, key: string) => (
    <ReactMarkdown
      key={key}
      remarkPlugins={[remarkGfm]}
      components={{
        code({ className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          if (match) {
            return (
              <SyntaxHighlighter
                language={match[1]}
                style={theme === 'dark' ? oneDark : oneLight}
                customStyle={{ margin: '18px 0', borderRadius: 10, fontSize: 12.5, border: '1px solid var(--line)' }}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            );
          }
          return <code className={className} {...props}>{children}</code>;
        },
      }}
    >
      {value}
    </ReactMarkdown>
  );

  const revealPattern = /<details><summary>(.*?)<\/summary>([\s\S]*?)<\/details>/g;
  const reveals = [...source.matchAll(revealPattern)];
  if (!reveals.length) return renderMarkdown(source, 'markdown');

  const content = [];
  let cursor = 0;
  reveals.forEach((match, index) => {
    const start = match.index ?? 0;
    if (start > cursor) content.push(renderMarkdown(source.slice(cursor, start), `before-${index}`));
    content.push(
      <details className="answer-reveal" key={`reveal-${index}`}>
        <summary>{match[1]}</summary>
        <div>{renderMarkdown(match[2].trim(), `answer-${index}`)}</div>
      </details>,
    );
    cursor = start + match[0].length;
  });
  if (cursor < source.length) content.push(renderMarkdown(source.slice(cursor), 'after'));
  return <>{content}</>;
}

export function MarkdownLesson({ lesson, theme, position, total, onCompleteTheory, onNavigate }: Props) {
  const [mode, setMode] = useState<LessonMode>('learn');
  const parsed = useMemo(() => splitSections(lesson.markdown), [lesson.markdown]);

  const changeMode = (next: LessonMode) => {
    setMode(next);
  };

  const visibleSections = mode === 'learn'
    ? parsed.sections
    : parsed.sections.filter((section) => REVIEW_SECTION.test(section.title));

  return (
    <article className="lesson-reader">
      <div className="reader-inner">
        <p className="lesson-kicker">JUNIOR BACKEND · {mode === 'learn' ? 'LEARN MODE' : 'REVIEW MODE'}</p>
        <div className="lesson-title-row">
          <div>
            <h1>{lesson.title}</h1>
            <p className="lead">{lesson.description}</p>
          </div>
          <span className={`status-pill ${lesson.progress.status}`}>{lesson.progress.status.replace('_', ' ')}</span>
        </div>
        <div className="lesson-meta">
          <span><Clock3 size={14} /> {lesson.duration} мин</span>
          <span><Code2 size={14} /> {lesson.has_task ? 'Практика' : 'Теория'}</span>
          <span><Sparkles size={14} /> +{lesson.xp} XP</span>
        </div>

        <div className="lesson-mode-switch" aria-label="Режим урока">
          <button className={mode === 'learn' ? 'active' : ''} onClick={() => changeMode('learn')}>
            <BookOpen size={15} />
            <span><b>Learn</b><small>Теория, примеры и практика</small></span>
          </button>
          <button className={mode === 'review' ? 'active' : ''} onClick={() => changeMode('review')}>
            <Brain size={15} />
            <span><b>Review</b><small>Вопросы без подсказок</small></span>
          </button>
        </div>

        <div className="markdown-body">
          {mode === 'learn' ? <MarkdownContent source={parsed.intro} theme={theme} /> : (
            <div className="review-intro">
              <b>Сначала реши без Theory</b>
              <p>Ответь на prediction, найди ошибку и проговори interview answer. Хорошие ответы и rubric раскрывай после попытки.</p>
            </div>
          )}
          {visibleSections.map((section) => COLLAPSED_SECTION.test(section.title) ? (
            <details className="lesson-disclosure" key={section.title}>
              <summary>{section.title === 'Good answers' ? 'Показать хороший ответ' : section.title}</summary>
              <div><MarkdownContent source={section.body} theme={theme} /></div>
            </details>
          ) : (
            <section className="lesson-section" key={section.title} data-section={section.title.toLowerCase()}>
              <h2>{section.title}</h2>
              <MarkdownContent source={section.body} theme={theme} />
            </section>
          ))}
        </div>

        <div className="theory-complete-card">
          <div>
            <strong>{lesson.progress.theory_completed ? 'Теория пройдена' : 'Закончил Learn mode?'}</strong>
            <p>{lesson.progress.theory_completed ? 'XP уже начислен. Переходи к практике.' : 'Отметь теорию и получи +5 XP.'}</p>
          </div>
          <button className="secondary-button" disabled={lesson.progress.theory_completed} onClick={onCompleteTheory}>
            <Check size={15} /> {lesson.progress.theory_completed ? 'Готово' : 'Отметить'}
          </button>
        </div>

        <nav className="lesson-navigation" aria-label="Навигация по урокам">
          <button disabled={position <= 1} onClick={() => onNavigate(-1)}><ChevronLeft size={16} /> Назад</button>
          <span>{position} / {total}</span>
          <button disabled={position >= total} onClick={() => onNavigate(1)}>Далее <ChevronRight size={16} /></button>
        </nav>
      </div>
    </article>
  );
}
