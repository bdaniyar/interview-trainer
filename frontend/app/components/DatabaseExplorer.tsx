import { Database, KeyRound, Link2 } from 'lucide-react';
import type { SqlCatalog, SqlTable } from '../sqlTypes';

export function SqlTableList({ catalog, selected, disabled, onSelect }: {
  catalog: SqlCatalog | null; selected: string; disabled: boolean; onSelect: (name: string) => void;
}) {
  return <aside className="sql-table-list" aria-label="Таблицы базы данных">
    <h3><Database size={13} /> shop-v1</h3>
    {catalog?.tables.map(table => <button key={table.handle} disabled={disabled}
      className={selected === table.name ? 'active' : ''} onClick={() => onSelect(table.name)}>
      <span>{table.name}</span><small>{table.columns.length} столбцов</small>
    </button>)}
  </aside>;
}

export function DatabaseExplorer({ catalog, selected, disabled, onSelect }: {
  catalog: SqlCatalog | null; selected: string; disabled: boolean; onSelect: (name: string) => void;
}) {
  const table = catalog?.tables.find(item => item.name === selected);
  return <section className="sql-explorer" aria-label="Database Explorer">
    <label>Таблица <select aria-label="Выбрать таблицу" value={selected} disabled={disabled || !catalog} onChange={e => onSelect(e.target.value)}>
      {catalog?.tables.map(item => <option key={item.handle} value={item.name}>{item.name}</option>)}
    </select></label>
    {table ? <TableSchema table={table} disabled={disabled} onSelect={onSelect} /> : <p className="sql-empty">Загружаем схему…</p>}
  </section>;
}

function TableSchema({ table, disabled, onSelect }: { table: SqlTable; disabled: boolean; onSelect: (name: string) => void }) {
  return <div className="sql-schema">
    <table aria-label={`Столбцы ${table.name}`}><thead><tr><th>Столбец</th><th>Тип</th><th>Nullable</th></tr></thead>
      <tbody>{table.columns.map(column => <tr key={column.name}>
        <td><span className="sql-column-name">{table.primary_key.includes(column.name) ? <KeyRound size={11} aria-label="Primary key" /> : null}
          {table.foreign_keys.some(key => key.columns.includes(column.name)) ? <Link2 size={11} aria-label="Foreign key" /> : null}{column.name}</span></td>
        <td>{column.pg_type}</td><td>{column.nullable ? 'YES' : 'NO'}</td>
      </tr>)}</tbody></table>
    <div className="sql-relationships"><p><b>PK</b> ({table.primary_key.join(', ')})</p>
      {table.foreign_keys.map(key => <p key={key.name}><b>FK</b> ({key.columns.join(', ')}) → <button disabled={disabled}
        onClick={() => onSelect(key.referenced_table)}>{key.referenced_table} ({key.referenced_columns.join(', ')})</button></p>)}
    </div>
  </div>;
}
