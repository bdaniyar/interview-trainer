import type { SqlLesson } from './sqlTypes';

export const draftKey = (lesson: SqlLesson) => `pythoria:sql:${lesson.lesson_id}:${lesson.task_id}`;

// PostgreSQL positions count characters; Monaco columns/offsets count UTF-16.
export function sqlPosition(query: string, position: number) {
  const prefix = Array.from(query).slice(0, Math.max(0, position - 1)).join('');
  return { offset: prefix.length, line: prefix.split('\n').length,
    column: prefix.length - prefix.lastIndexOf('\n') };
}
