export interface SqlLesson {
  lesson_id: string;
  lesson_slug: string;
  dataset_id: 'shop-v1';
  task_id: 'guided-select';
  mode: 'lesson_read';
  starter_sql: string;
  prompt: string;
  can_check: false;
}

export interface SqlSession {
  session_id: string;
  generation: number;
  lesson_id: string;
  lesson_slug: string;
  task_id: string;
  dataset_id: string;
  dataset_checksum: string;
  postgres_major: number;
  created_at: string;
  expires_at: string;
  cold_start_ms: number;
}

export interface SqlError {
  kind: 'policy' | 'postgres' | 'resource' | 'infrastructure';
  code: string;
  message: string;
  sqlstate: string | null;
  position: number | null;
  hint: string | null;
}

export interface SqlResult {
  session_id: string;
  generation: number;
  command: 'SELECT';
  columns: { name: string; pg_type: string; type_oid: number }[];
  rows: (string | boolean | null)[][];
  rows_returned: number;
  has_more: boolean;
  truncated: boolean;
  duration_ms: number;
  error: SqlError | null;
  session_closed: boolean;
}

export interface SqlTable {
  handle: string;
  schema_name: 'lab';
  name: string;
  columns: { name: string; pg_type: string; nullable: boolean }[];
  primary_key: string[];
  foreign_keys: { name: string; columns: string[]; referenced_table: string;
    referenced_columns: string[]; on_update: string; on_delete: string }[];
}

export interface SqlCatalog {
  session_id: string;
  generation: number;
  tables: SqlTable[];
}
