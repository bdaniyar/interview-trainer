import type { CourseData, ExecutionResult, InterviewQuestion, LessonData } from './types';

export const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_ORIGIN}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  course: () => request<CourseData>('/api/course'),
  lesson: (slug: string) => request<LessonData>(`/api/lessons/${slug}`),
  openLesson: (slug: string) => request(`/api/lessons/${slug}/open`, { method: 'POST' }),
  saveFiles: (slug: string, files: Record<string, string>) =>
    request(`/api/lessons/${slug}/files`, { method: 'PUT', body: JSON.stringify({ files }) }),
  run: (lesson_slug: string, files: Record<string, string>, entrypoint: string) =>
    request<ExecutionResult>('/api/run', { method: 'POST', body: JSON.stringify({ lesson_slug, files, entrypoint }) }),
  check: (lesson_slug: string, files: Record<string, string>) =>
    request<ExecutionResult>('/api/check', { method: 'POST', body: JSON.stringify({ lesson_slug, files, entrypoint: 'main.py' }) }),
  terminal: (lesson_slug: string, files: Record<string, string>, command: string) =>
    request<ExecutionResult>('/api/terminal', { method: 'POST', body: JSON.stringify({ lesson_slug, files, command }) }),
  completeTheory: (slug: string) =>
    request<{ theory_completed: boolean; xp_awarded: number; xp: number }>(`/api/progress/${slug}/theory`, {
      method: 'POST',
      body: JSON.stringify({ completed: true }),
    }),
  solution: (slug: string) => request<{ files: Record<string, string> }>(`/api/lessons/${slug}/solution`),
  interview: () => request<{ questions: InterviewQuestion[]; current_index: number }>('/api/interview'),
  completeInterview: (question_id: string, answer: string) =>
    request<{ completed: boolean; xp_awarded: number; xp: number }>('/api/interview/complete', {
      method: 'POST',
      body: JSON.stringify({ question_id, answer }),
    }),
  setTheme: (theme: 'dark' | 'light') =>
    request('/api/preferences', { method: 'PUT', body: JSON.stringify({ theme }) }),
};
