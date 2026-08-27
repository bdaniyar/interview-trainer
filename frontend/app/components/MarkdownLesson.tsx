'use client';

import { Check, ChevronLeft, ChevronRight, Clock3, Code2, Sparkles } from 'lucide-react';
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

export function MarkdownLesson({ lesson, theme, position, total, onCompleteTheory, onNavigate }: Props) {
  return (
    <article className="lesson-reader">
      <div className="reader-inner">
        <p className="lesson-kicker">PYTHON INTERNALS</p>
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

        <div className="markdown-body">
          <ReactMarkdown
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
            {lesson.markdown}
          </ReactMarkdown>
        </div>

        <div className="theory-complete-card">
          <div>
            <strong>{lesson.progress.theory_completed ? 'Теория пройдена' : 'Закончил читать?'}</strong>
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
