export type LessonStatus = 'not_started' | 'in_progress' | 'completed';

export interface LessonSummary {
  slug: string;
  title: string;
  module_slug: string;
  module_title: string;
  order: number;
  duration: number;
  xp: number;
  topics: string[];
  description: string;
  has_task: boolean;
  has_solution: boolean;
  status: LessonStatus;
  theory_completed: boolean;
  task_completed: boolean;
}

export interface CourseModule {
  slug: string;
  title: string;
  order: number;
  lessons: LessonSummary[];
}

export interface CourseData {
  title: string;
  modules: CourseModule[];
  summary: {
    total: number;
    completed: number;
    percent: number;
    xp: number;
    last_opened_lesson: string;
    theme: 'dark' | 'light';
  };
}

export interface LessonData extends Omit<LessonSummary, 'status' | 'theory_completed' | 'task_completed'> {
  markdown: string;
  files: Record<string, string>;
  interview: InterviewQuestion[];
  progress: {
    status: LessonStatus;
    theory_completed: boolean;
    task_completed: boolean;
  };
}

export interface TestResult {
  name: string;
  status: string;
  passed: boolean;
}

export interface ExecutionResult {
  stdout: string;
  stderr: string;
  exit_code: number;
  timed_out: boolean;
  duration_ms: number;
  tests?: TestResult[];
  tests_passed?: number;
  tests_total?: number;
  passed?: boolean;
  xp_awarded?: number;
  xp?: number;
}

export interface InterviewQuestion {
  id: string;
  lesson_slug: string;
  lesson_title: string;
  question: string;
  answer: string[];
  completed: boolean;
  code?: string;
  expected?: string;
  reason?: string;
}
