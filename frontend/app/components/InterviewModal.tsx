'use client';

import { ArrowLeft, ArrowRight, CheckCircle2, Code2, X } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

import { api } from '../api';
import type { InterviewQuestion } from '../types';

interface Props {
  onClose: () => void;
  onXp: (xp: number) => void;
}

export function InterviewModal({ onClose, onXp }: Props) {
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [revealed, setRevealed] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.interview().then((data) => {
      setQuestions(data.questions);
      setIndex(data.current_index);
    }).catch((err: Error) => setError(err.message));
  }, []);

  const question = questions[index];
  const completedCount = useMemo(() => questions.filter((item) => item.completed).length, [questions]);

  const move = (delta: number) => {
    setIndex((current) => Math.min(Math.max(0, current + delta), questions.length - 1));
    setAnswer('');
    setRevealed(false);
  };

  const reveal = async () => {
    if (!question) return;
    setRevealed(true);
    try {
      const result = await api.completeInterview(question.id, answer);
      setQuestions((current) => current.map((item) => item.id === question.id ? { ...item, completed: true } : item));
      onXp(result.xp);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не удалось сохранить ответ');
    }
  };

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true" aria-label="Interview mode">
      <section className="interview-modal">
        <header>
          <div className="interview-title"><span className="interview-icon"><Code2 size={18} /></span><div><b>Interview mode</b><small>{completedCount} из {questions.length} отвечено</small></div></div>
          <button className="icon-button" onClick={onClose} aria-label="Закрыть"><X size={17} /></button>
        </header>
        <div className="interview-progress"><span style={{ width: `${questions.length ? ((index + 1) / questions.length) * 100 : 0}%` }} /></div>
        {error ? <p className="error-banner">{error}</p> : null}
        {!question ? <div className="interview-loading">Загружаем вопросы…</div> : (
          <div className="interview-content">
            <div className="question-counter">QUESTION {index + 1} / {questions.length} · {question.lesson_title}</div>
            <h2>{question.question}</h2>
            {question.code ? <pre className="question-code"><code>{question.code}</code></pre> : null}
            <label htmlFor="interview-answer">Твой ответ</label>
            <textarea id="interview-answer" value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Объясни своими словами…" />
            {!revealed ? (
              <button className="primary-button reveal-button" onClick={reveal}>Показать ответ</button>
            ) : (
              <div className="expected-answer">
                <div className="expected-heading"><CheckCircle2 size={17} /> Ключевые пункты</div>
                {question.expected ? <p><b>Expected:</b> {question.expected}</p> : null}
                <ul>{question.answer.map((item) => <li key={item}>{item}</li>)}</ul>
                {question.reason ? <p><b>Причина:</b> {question.reason}</p> : null}
              </div>
            )}
          </div>
        )}
        <footer>
          <button className="ghost-button" disabled={index === 0} onClick={() => move(-1)}><ArrowLeft size={15} /> Назад</button>
          <button className="ghost-button" disabled={index >= questions.length - 1} onClick={() => move(1)}>Далее <ArrowRight size={15} /></button>
        </footer>
      </section>
    </div>
  );
}
