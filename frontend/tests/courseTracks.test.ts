import { describe, expect, it } from 'vitest';

import { resumeTrack, trackForLesson, trackModules } from '../app/courseTracks';
import type { CourseData, CourseModule, LessonSummary } from '../app/types';

const moduleWith = (slug: string): CourseModule => ({
  title: slug, slug, order: 1, lessons: [{ slug } as LessonSummary],
});
const course: CourseData = {
  title: 'Backend',
  modules: [moduleWith('generators'), moduleWith('saved-backend')],
  summary: { total: 2, completed: 0, percent: 0, last_opened_lesson: 'saved-backend', theme: 'dark', xp: 5 },
  ai: {
    modules: [moduleWith('ai01-first'), moduleWith('ai02-remembered')],
    summary: { total: 2, completed: 1, percent: 50 },
    roadmap: [{ slug: 'ai-stage-01', title: 'AI', planned: 70 }],
  },
};

describe('course tracks', () => {
  it('resolves published deep links to exactly one track', () => {
    expect(trackForLesson(course, 'generators')).toBe('backend');
    expect(trackForLesson(course, 'ai02-remembered')).toBe('ai-engineering');
    expect(trackForLesson(course, 'ai01-planned')).toBeUndefined();
  });

  it('resumes each track independently and handles stale AI links', () => {
    expect(resumeTrack(course, 'backend', 'ai02-remembered')).toBe('saved-backend');
    expect(resumeTrack(course, 'ai-engineering', 'ai02-remembered')).toBe('ai02-remembered');
    expect(resumeTrack(course, 'ai-engineering', 'saved-backend')).toBe('ai01-first');
    expect(resumeTrack(course, 'ai-engineering', 'ai01-planned')).toBe('ai01-first');
    expect(trackModules(course, 'backend').flatMap((module) => module.lessons.map((lesson) => lesson.slug))).toEqual(['generators', 'saved-backend']);
  });
});
