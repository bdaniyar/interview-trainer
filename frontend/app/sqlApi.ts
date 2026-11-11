import { API_ORIGIN } from './api';
import type { SqlCatalog, SqlCheckResult, SqlLesson, SqlResult, SqlSession } from './sqlTypes';

export class SqlApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

async function request<T>(path: string, method = 'GET', payload?: unknown, keepalive = false, timeoutMs = 45000): Promise<T> {
  let response: Response;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    response = await fetch(`${API_ORIGIN}/api/sql${path}`, {
      method, headers: { 'Content-Type': 'application/json' },
      body: payload === undefined ? undefined : JSON.stringify(payload),
      signal: controller.signal,
      keepalive,
    });
  } catch {
    throw new SqlApiError(503, 'backend_unavailable', 'Нет связи с сервером. Запрос остался в браузере.');
  } finally { clearTimeout(timer); }
  if (!response.ok) {
    const body = await response.json().catch(() => ({})) as { error?: { code?: string; message?: string }; detail?: unknown };
    throw new SqlApiError(response.status, body.error?.code ?? 'invalid_request',
      body.error?.message ?? (typeof body.detail === 'string' ? body.detail : 'Не удалось выполнить SQL-запрос.'));
  }
  return response.status === 204 ? undefined as T : response.json() as Promise<T>;
}

const sidPath = (session: SqlSession) => `/sessions/${encodeURIComponent(session.session_id)}`;
export const sqlApi = {
  lesson: (slug: string) => request<SqlLesson>(`/lessons/${encodeURIComponent(slug)}`),
  create: (lesson_slug: string) => request<SqlSession>('/sessions', 'POST', { lesson_slug }),
  run: (session: SqlSession, sql: string) => request<SqlResult>(sidPath(session) + '/run', 'POST', { generation: session.generation, sql }),
  catalog: (session: SqlSession) => request<SqlCatalog>(sidPath(session) + `/catalog?generation=${session.generation}`),
  rows: (session: SqlSession, handle: string, offset = 0) => request<SqlResult>(
    sidPath(session) + `/tables/${encodeURIComponent(handle)}/rows?generation=${session.generation}&limit=50&offset=${offset}`),
  reset: (session: SqlSession) => request<SqlSession>(sidPath(session) + '/reset', 'POST', { generation: session.generation }),
  close: (session: SqlSession) => request<void>(sidPath(session) + `?generation=${session.generation}`, 'DELETE', undefined, true),
  check: (lessonSlug: string, taskId: string, sql: string, requestId: string) => request<SqlCheckResult>(
    `/lessons/${encodeURIComponent(lessonSlug)}/tasks/${encodeURIComponent(taskId)}/check`, 'POST',
    { request_id: requestId, sql }, false, 120000),
};
