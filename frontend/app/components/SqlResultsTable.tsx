import { sqlPosition } from '../sqlDraft';
import type { SqlResult } from '../sqlTypes';

export function SqlResultsTable({ result, query = '', onPosition }: {
  result: SqlResult | null; query?: string; onPosition?: (position: number) => void;
}) {
  if (!result) return <p className="sql-empty">Выполните запрос, чтобы увидеть результат PostgreSQL.</p>;
  if (result.error) {
    const error = result.error;
    const caret = error.position ? sqlPosition(query, error.position) : null;
    return <div className="sql-diagnostic" role="alert">
      <strong>{error.kind === 'policy' ? 'Запрос не входит в разрешённый SELECT-режим' : 'Ошибка запроса'}</strong>
      <p>{error.message}</p>
      <div>{error.sqlstate ? <code>SQLSTATE {error.sqlstate}</code> : null}
        {caret ? <button disabled={!onPosition} onClick={() => onPosition?.(error.position!)}>Строка {caret.line}, столбец {caret.column}</button> : null}</div>
      {error.hint ? <p>{error.hint}</p> : null}
    </div>;
  }
  return <div className="sql-table-result">
    <div className="sql-result-info" role="status">
      <span>{result.has_more || result.truncated ? `Показано ${result.rows_returned} строк, есть ещё` : `Строк: ${result.rows_returned}`}</span>
      <span>{result.duration_ms} ms</span>
    </div>
    <div className="sql-table-scroll"><table aria-label="Результат PostgreSQL">
      <thead><tr>{result.columns.map((column, index) => <th key={index}>{column.name}<small>{column.pg_type}</small></th>)}</tr></thead>
      <tbody>{result.rows.map((row, index) => <tr key={index}>{row.map((value, cell) => <td key={cell}>
        {value === null ? <span className="sql-null" title="SQL NULL">NULL</span>
          : value === '' ? <span className="sql-empty-string" title="Пустая строка">&apos;&apos;</span>
          : <span title={String(value)}>{value === 'NULL' ? '"NULL"' : String(value)}</span>}
      </td>)}</tr>)}</tbody>
    </table>{result.rows.length === 0 ? <p className="sql-empty">Запрос выполнен. Строк нет.</p> : null}</div>
  </div>;
}
