import type { SqlCheckResult } from '../sqlTypes';

export function SqlCheckFeedback({ result, stale }: { result: SqlCheckResult; stale: boolean }) {
  return <section className={`sql-check-feedback ${result.passed ? 'passed' : 'failed'}`} aria-label="Проверка SQL" role="status">
    <header><strong>{result.passed ? 'Passed' : 'Failed'}</strong><span>{result.tests_passed} / {result.tests_total} проверок</span></header>
    {stale ? <small>Проверка предыдущего запроса</small> : null}
    <ul>{result.feedback.map((item, index) => <li key={index}>{item.message}{item.sqlstate ? <code> SQLSTATE {item.sqlstate}</code> : null}</li>)}</ul>
  </section>;
}
