'use client';

import { BookOpen, Brain, Check, ChevronLeft, ChevronRight, Clock3, Code2, Sparkles } from 'lucide-react';
import { useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark, oneLight } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import remarkGfm from 'remark-gfm';

import type { LessonData } from '../types';
import { splitSections, splitContent } from './lessonMarkdown';

interface Props {
  lesson: LessonData;
  theme: 'dark' | 'light';
  position: number;
  total: number;
  onCompleteTheory: () => void;
  onNavigate: (direction: -1 | 1) => void;
}

type LessonMode = 'learn' | 'review';

const REVIEW_SECTION = /практика|предсказание|задача|вопросы с собеседований|хорошие ответы|критерии хорошего ответа/i;
const COLLAPSED_SECTION = /модель понимания|хорошие ответы|критерии хорошего ответа|источники/i;

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

  return <>{splitContent(source).map((block, index) => block.kind === 'markdown'
    ? renderMarkdown(block.body, `markdown-${index}`)
    : (
      <details className="answer-reveal" key={`answer-${index}`}>
        <summary>{block.summary}</summary>
        <div><MarkdownContent source={block.body} theme={theme} /></div>
      </details>
    ))}</>;
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
        <p className="lesson-kicker">JUNIOR BACKEND · {mode === 'learn' ? 'РЕЖИМ ОБУЧЕНИЯ' : 'РЕЖИМ ПОВТОРЕНИЯ'}</p>
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
            <span><b>Обучение</b><small>Теория, примеры и практика</small></span>
          </button>
          <button className={mode === 'review' ? 'active' : ''} onClick={() => changeMode('review')}>
            <Brain size={15} />
            <span><b>Повторение</b><small>Вопросы без подсказок</small></span>
          </button>
        </div>

        <div className="markdown-body" key={`${lesson.slug}:${mode}`}>
          {mode === 'learn' ? <MarkdownContent source={parsed.intro} theme={theme} /> : (
            <div className="review-intro">
              <b>Сначала реши без теории</b>
              <p>Предскажи результат кода, найди ошибку и проговори ответ как на собеседовании. Хорошие ответы и критерии раскрывай после попытки.</p>
            </div>
          )}
          {visibleSections.map((section) => COLLAPSED_SECTION.test(section.title) ? (
            <details className="lesson-disclosure" key={section.title}>
              <summary>{section.title === 'Хорошие ответы' ? 'Показать хороший ответ' : section.title}</summary>
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
            <strong>{lesson.progress.theory_completed ? 'Теория пройдена' : 'Закончил режим обучения?'}</strong>
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
