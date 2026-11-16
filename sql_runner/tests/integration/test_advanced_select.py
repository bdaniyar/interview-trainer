"""Real PG17 advanced SELECT contracts, independent relational oracles and lesson goldens."""
from decimal import Decimal
import json
from pathlib import Path
import re

import pytest

from sql_runner.app.comparator import compare
from sql_runner.app.policy import PolicyError, validate
from sql_runner.tests.integration.advanced_inputs import COMMON, RECURSIVE
from sql_runner.tests.integration.test_order_distinct_grading import fixture, grade, run, task_for

IDS = ['sql.subquery.27','sql.subquery.31','sql.subquery.28','sql.subquery.30','sql.subquery.32',
       'sql.basic.06','sql.set.50','sql.window.37','sql.window.33','sql.window.36','sql.window.38']
TYPES = ['int8 numeric','int8 int8','int8 text','int8 numeric','int8 int4','int8 text','text',
         'int8 int8 numeric numeric','int8 int8 int8','int8 int8 numeric','int8 int8 timestamptz']
EQUIVALENTS = [
 'SELECT o.id,o.total FROM orders o CROSS JOIN (SELECT AVG(total) v FROM orders) a WHERE o.total>a.v',
 'SELECT o.id,o.user_id FROM orders o JOIN (SELECT user_id,MAX(created_at) t FROM orders GROUP BY user_id) m ON m.user_id=o.user_id AND m.t=o.created_at ORDER BY o.user_id,o.id DESC',
 "SELECT id,email FROM users WHERE id IN (SELECT user_id FROM orders WHERE status='paid')",
 "SELECT user_id,SUM(total) AS revenue FROM orders WHERE status='paid' GROUP BY user_id HAVING SUM(total)>=150 ORDER BY user_id",
 'WITH RECURSIVE c AS (SELECT id,manager_id,0 AS depth FROM users WHERE id=4 UNION ALL SELECT u.id,u.manager_id,c.depth+1 FROM c JOIN users u ON c.manager_id=u.id) SELECT id,depth FROM c ORDER BY depth',
 "SELECT id,CASE WHEN status='paid' THEN 'completed' WHEN status='cancelled' THEN 'cancelled' ELSE 'pending' END AS label FROM orders",
 "SELECT DISTINCT u.country FROM users u WHERE u.active AND NOT EXISTS (SELECT 1 FROM users p JOIN orders o ON o.user_id=p.id WHERE o.status='paid' AND p.country IS NOT DISTINCT FROM u.country) ORDER BY u.country NULLS LAST",
 'SELECT o.id,o.user_id,o.total,(SELECT i.total FROM orders i WHERE i.user_id=o.user_id AND (i.created_at<o.created_at OR (i.created_at=o.created_at AND i.id<o.id)) ORDER BY i.created_at DESC,i.id DESC LIMIT 1) AS previous_total FROM orders o ORDER BY o.user_id,o.created_at,o.id',
 'SELECT o.id,o.user_id,1+(SELECT COUNT(*) FROM orders i WHERE i.user_id=o.user_id AND (i.created_at>o.created_at OR (i.created_at=o.created_at AND i.id>o.id))) AS row_number FROM orders o ORDER BY o.user_id,row_number',
 'SELECT id,user_id,SUM(total) OVER(PARTITION BY user_id ORDER BY created_at,id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total FROM orders ORDER BY user_id,created_at,id',
 'SELECT o.id,o.user_id,(SELECT i.created_at FROM orders i WHERE i.user_id=o.user_id AND (i.created_at>o.created_at OR (i.created_at=o.created_at AND i.id>o.id)) ORDER BY i.created_at,i.id LIMIT 1) AS next_created_at FROM orders o ORDER BY o.user_id,o.created_at,o.id'
]
WRONG = [
 'SELECT id,total FROM orders WHERE total >= (SELECT AVG(total) FROM orders)',
 'SELECT id,user_id FROM orders WHERE created_at=(SELECT MAX(created_at) FROM orders) ORDER BY user_id',
 "SELECT u.id,u.email FROM users u JOIN orders o ON u.id=o.user_id WHERE o.status='paid'",
 "SELECT user_id,SUM(total) revenue FROM orders WHERE status='paid' GROUP BY user_id HAVING SUM(total)>150 ORDER BY user_id",
 'WITH RECURSIVE c AS (SELECT id,manager_id,0 depth FROM users WHERE id=4 UNION ALL SELECT u.id,u.manager_id,c.depth+1 FROM users u JOIN c ON u.id=c.manager_id WHERE c.depth<1) SELECT id,depth FROM c ORDER BY depth',
 "SELECT id,CASE status WHEN 'paid' THEN 'completed' WHEN 'cancelled' THEN 'cancelled' END AS label FROM orders",
 "SELECT DISTINCT country FROM users WHERE active AND country NOT IN (SELECT u.country FROM users u JOIN orders o ON o.user_id=u.id WHERE o.status='paid') ORDER BY country NULLS LAST",
 'SELECT id,user_id,total,LAG(total) OVER(ORDER BY created_at,id) AS previous_total FROM orders ORDER BY user_id,created_at,id',
 'SELECT id,user_id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC) AS row_number FROM orders ORDER BY user_id,row_number',
 'SELECT id,user_id,SUM(total) OVER(PARTITION BY user_id ORDER BY created_at) AS running_total FROM orders ORDER BY user_id,created_at,id',
 'SELECT id,user_id,LAG(created_at) OVER(PARTITION BY user_id ORDER BY created_at,id) AS next_created_at FROM orders ORDER BY user_id,created_at,id'
]
PUBLIC_USERS=[(1,'KZ',True,None),(2,'KZ',True,1),(3,None,False,1),(4,'GE',True,2)]
PUBLIC_ORDERS=[(10,1,'paid','100.00',1),(11,1,'cancelled','40.00',2),(12,2,'paid','200.00',3),(13,2,'paid','50.00',4),(14,4,'new','80.00',5)]


def oracle(task_id, case='public'):
    """Python arithmetic/set/sequence model; never executes or parses reference SQL."""
    users, orders = ((PUBLIC_USERS,PUBLIC_ORDERS) if case=='public' else (RECURSIVE if task_id=='sql.subquery.32' else COMMON)[case])
    money=lambda value: format(Decimal(value),'.2f')
    stamp=lambda day: f'2026-{2 if case=="public" else 3:02d}-{day:02d}T00:00:00Z'
    email=lambda i: f'{chr(96+i)}@example.com' if case=='public' else f'{i}@phase8.test'
    byuser={u[0]:sorted([o for o in orders if o[1]==u[0]],key=lambda o:(o[4],o[0])) for u in users}
    if task_id=='sql.subquery.27':
        mean=sum((Decimal(o[3]) for o in orders),Decimal(0))/len(orders) if orders else None
        return [[str(o[0]),money(o[3])] for o in orders if Decimal(o[3])>mean]
    if task_id=='sql.subquery.31':
        return [[str(o[0]),str(uid)] for uid,items in sorted(byuser.items()) for o in items if o[4]==max(i[4] for i in items)]
    if task_id=='sql.subquery.28':
        return [[str(u[0]),email(u[0])] for u in users if any(o[2]=='paid' for o in byuser[u[0]])]
    if task_id=='sql.subquery.30':
        totals={uid:sum((Decimal(o[3]) for o in items if o[2]=='paid'),Decimal(0)) for uid,items in byuser.items()}
        return [[str(uid),money(total)] for uid,total in sorted(totals.items()) if total>=150]
    if task_id=='sql.subquery.32':
        parents={u[0]:u[3] for u in users};current=4;rows=[];seen=set()
        while current in parents:
            assert current not in seen, 'Trusted main-task fixtures must be acyclic'
            seen.add(current);rows.append([str(current),str(len(rows))]);current=parents[current]
        return rows
    if task_id=='sql.basic.06':
        labels={'paid':'completed','cancelled':'cancelled'}
        return [[str(o[0]),labels.get(o[2],'pending')] for o in orders]
    if task_id=='sql.set.50':
        left={u[1] for u in users if u[2]};right={u[1] for u in users if any(o[2]=='paid' for o in byuser[u[0]])}
        return [[v] for v in sorted(left-right,key=lambda v:(v is None,v or ''))]
    rows=[]
    for uid,items in sorted(byuser.items()):
        if task_id=='sql.window.33':items=items[::-1]
        running=Decimal(0)
        for idx,o in enumerate(items):
            if task_id=='sql.window.37':value=[money(o[3]),money(items[idx-1][3]) if idx else None]
            elif task_id=='sql.window.33':value=[str(idx+1)]
            elif task_id=='sql.window.36':running+=Decimal(o[3]);value=[money(running)]
            else:value=[stamp(items[idx+1][4]) if idx+1<len(items) else None]
            rows.append([str(o[0]),str(uid),*value])
    return rows


def expected(task_id,case='public'):
    task=task_for(task_id);rows=oracle(task_id,case)
    return dict(columns=[dict(name=n,pg_type=t) for n,t in zip(task.expected_columns,TYPES[IDS.index(task_id)].split())],rows=rows,rows_returned=len(rows),error=None,truncated=False,has_more=False)


def hardcoded(task_id):
    task=task_for(task_id);types=TYPES[IDS.index(task_id)].split()
    literal=lambda value,kind: 'NULL::'+kind if value is None else "'"+str(value).replace("'","''")+"'::"+kind
    values=','.join('('+','.join(literal(v,t) for v,t in zip(row,types))+')' for row in oracle(task_id))
    return 'SELECT * FROM (VALUES '+values+') v('+','.join(task.expected_columns)+')'


@pytest.mark.parametrize('task_id',IDS)
def test_all_six_datasets_have_independent_typed_reference_results(manager,task_id):
    for case in task_for(task_id).cases:
        with fixture(manager,task_id,case.id) as (handle,task):
            actual=run(manager,handle,task.reference_sql)
            assert not actual['error'] and not actual['has_more'] and not actual['truncated']
            assert [c['pg_type'] for c in actual['columns']]==TYPES[IDS.index(task_id)].split()
            assert compare(expected(task_id,case.id.removesuffix('-v1')),actual,comparison=task.comparison,numeric_compatible=True,ordered_key_columns=task.ordered_key_columns)=='passed', (task_id,case.id,actual)
    assert not manager.backend.containers()


@pytest.mark.parametrize('task_id',IDS)
@pytest.mark.parametrize('kind',['reference','equivalent','wrong','hardcoded'])
def test_full_check_advanced_contracts(manager,task_id,kind):
    i=IDS.index(task_id)
    query={'reference':task_for(task_id).reference_sql,'equivalent':EQUIVALENTS[i],'wrong':WRONG[i],'hardcoded':hardcoded(task_id)}[kind]
    answer=grade(manager,task_id,query)
    if kind in {'reference','equivalent'}:assert answer['passed'] and answer['tests_passed']==6
    else:
        assert not answer['passed'] and answer['tests_passed']<6
        if kind=='hardcoded':assert answer['tests_passed']==1
    assert not manager.backend.containers()
    assert not any(value in json.dumps(answer) for value in ['phase8.test','reference_sql','seed_file'])


@pytest.mark.parametrize('task_id',IDS)
def test_contract_column_row_order_and_duplicate_mutations_fail(manager,task_id):
    with fixture(manager,task_id,'public-v1') as (handle,task):
        good=run(manager,handle,task.reference_sql)
        for query in ['SELECT * FROM ('+task.reference_sql.rstrip(';')+') q LIMIT 0',
                      'SELECT * FROM ('+task.reference_sql.rstrip(';')+') q UNION ALL SELECT * FROM ('+task.reference_sql.rstrip(';')+') q',
                      'SELECT 1 AS wrong_column']:
            actual=run(manager,handle,query)
            assert compare(good,actual,comparison=task.comparison,numeric_compatible=True,ordered_key_columns=task.ordered_key_columns)!='passed'
        if task.comparison=='ordered' and len(good['rows'])>1:
            reverse=good|{'rows':good['rows'][::-1]}
            assert compare(good,reverse,comparison=task.comparison,numeric_compatible=True,ordered_key_columns=task.ordered_key_columns)=='rows'


@pytest.mark.parametrize('query',[
 'WITH RECURSIVE c AS (SELECT 1 UNION ALL SELECT 1 FROM c) DELETE FROM users',
 'WITH x AS (DELETE FROM orders RETURNING *) SELECT * FROM x',
 'SELECT * FROM pg_catalog.pg_roles','SELECT pg_read_file(\'/etc/passwd\')',
 'SELECT 1; UPDATE orders SET total=0','SELECT * FROM users FOR UPDATE',
])
def test_advanced_select_does_not_broaden_write_or_admin_policy(query):
    with pytest.raises(PolicyError):validate(query)


def test_recursive_nontermination_deadline_truncation_and_recovery(manager,session):
    sid=session['session_id']
    result=manager.run(sid,1,'WITH RECURSIVE n AS (SELECT 1 AS v UNION ALL SELECT v+1 FROM n) SELECT SUM(v) FROM n')
    # Materializing an unbounded recursive result can hit temp_file_limit first.
    assert result['error'] and result['error']['sqlstate'] in {'53400','57014'}
    assert not manager.backend.containers()  # Resource faults dispose the affected lease.
    sid=manager.create()['session_id']
    cpu=manager.run(sid,1,"WITH RECURSIVE n AS (SELECT 1::bigint AS v UNION ALL SELECT v+length(repeat('x',100000+(v%2)::integer)) FROM n) SELECT SUM(v) FROM n")
    assert cpu['error'] and cpu['error']['sqlstate']=='57014'
    assert not manager.backend.containers()
    sid=manager.create()['session_id']
    limited=manager.run(sid,1,'WITH RECURSIVE n AS (SELECT 1 AS v UNION ALL SELECT v+1 FROM n WHERE v<600) SELECT v FROM n')
    assert limited['truncated'] or limited['has_more']
    assert manager.run(sid,1,'SELECT COUNT(*) AS n FROM users')['rows']==[['4']]
    assert len(manager.backend.containers())==1


GOLDENS=json.loads((Path(__file__).with_name('advanced_lesson_expected.json')).read_text())
@pytest.mark.parametrize('slug,goldens',GOLDENS.items())
def test_all_advanced_lesson_blocks_have_independent_typed_results(manager,session,slug,goldens):
    source=(Path(__file__).resolve().parents[3]/'content/stage-10'/slug/'lesson.md').read_text()
    blocks=list(re.finditer(r'```sql\n(.*?)```',source,re.S))
    assert len(blocks)==len(goldens)
    for block,golden in zip(blocks,goldens):
        actual=manager.run(session['session_id'],1,block[1])
        if golden.get('error'):
            assert golden['error'] in source[max(0,block.start()-350):block.start()]
            assert actual['error']['sqlstate']==golden['error']
            continue
        if 'reference_task' in golden:
            task=task_for(golden['reference_task']);expect=expected(task.id)
            assert compare(expect,actual,comparison=task.comparison,numeric_compatible=True,ordered_key_columns=task.ordered_key_columns)=='passed'
            continue
        assert not actual['error'] and not actual['truncated'],(slug,block[1],actual)
        assert [c['name'] for c in actual['columns']]==golden['names']
        assert [c['pg_type'] for c in actual['columns']]==golden['types']
        assert actual['rows']==golden['rows'],(slug,block[1],actual['rows'],golden['rows'])
    assert len(manager.backend.containers())==1
