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
  priority?: 'P0' | 'P1' | 'P2' | 'P3';
  interview_probability?: 'very_high' | 'high' | 'medium' | 'low';
  content_status?: 'complete' | 'planned' | 'archived';
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
  short_answer?: string;
  junior_answer?: string;
  follow_up_question?: string;
  follow_up_answer?: string;
  expected_answer?: {
    must_mention?: string[];
    good_additions?: string[];
    common_wrong_answers?: string[];
    follow_up_questions?: string[];
  };
  completed: boolean;
  code?: string;
  expected?: string;
  reason?: string;
}

export interface InterviewSet {
  slug: string;
  title: string;
  description: string;
  estimated_minutes: number;
}

export interface InterviewData {
  questions: InterviewQuestion[];
  current_index: number;
  sets: InterviewSet[];
  active_set: string;
}
