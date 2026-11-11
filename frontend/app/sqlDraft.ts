import type { SqlLesson } from './sqlTypes';

export const draftKey = (lesson: SqlLesson) => `pythoria:sql:${lesson.lesson_id}:${lesson.task_id}`;

export function loadDraft(lesson: SqlLesson) {
  const existing = localStorage.getItem(draftKey(lesson));
  if (existing !== null) return { value: existing, saved: true };
  // Keep the Phase 2 draft when its guided activity becomes a graded task.
  const legacy = localStorage.getItem(`pythoria:sql:${lesson.lesson_id}:guided-select`);
  if (legacy !== null) {
    try { localStorage.setItem(draftKey(lesson), legacy); }
    catch { return { value: legacy, saved: false }; }
    return { value: legacy, saved: true };
  }
  return { value: lesson.starter_sql, saved: true };
}

// PostgreSQL positions count characters; Monaco columns/offsets count UTF-16.
export function sqlPosition(query: string, position: number) {
  const prefix = Array.from(query).slice(0, Math.max(0, position - 1)).join('');
  return { offset: prefix.length, line: prefix.split('\n').length,
    column: prefix.length - prefix.lastIndexOf('\n') };
}
