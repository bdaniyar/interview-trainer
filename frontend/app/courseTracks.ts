import type { CourseData, CourseTrack } from './types';

export function trackModules(course: CourseData, track: CourseTrack) {
  return track === 'ai-engineering' ? course.ai?.modules ?? [] : course.modules;
}

export function trackForLesson(course: CourseData, slug: string): CourseTrack | undefined {
  for (const track of ['backend', 'ai-engineering'] as const) {
    if (trackModules(course, track).some((module) => module.lessons.some((lesson) => lesson.slug === slug))) {
      return track;
    }
  }
}

export function resumeTrack(course: CourseData, track: CourseTrack, remembered: string | null) {
  const previous = track === 'backend' ? course.summary.last_opened_lesson : remembered;
  if (previous && trackForLesson(course, previous) === track) return previous;
  return trackModules(course, track)[0]?.lessons[0]?.slug ?? '';
}
