// Called by the actual Chrome walkthrough. All operations target test port 18080.
import assert from 'node:assert/strict';

export async function transactionWalkthrough({ api, evaluate, until, selectLesson, call, size, screenshot }) {
  const dml = 's10-data-modification';
  const booking = 's11-booking-concurrency';
  const base = '/api/transactions/lessons/';
  const entry = '.tx-workspace';
  const click = selector => evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
  const button = (parent, label) => evaluate(`Array.from(document.querySelectorAll(${JSON.stringify(parent+' button')})).find(b=>b.textContent.trim()===${JSON.stringify(label)}).click()`);
  const editor = side => `window.__phase8aMonaco.editor.getEditors().find(e=>e.getDomNode()?.closest('.tx-editor[data-side=${side}]'))`;
  const fill = async (side, source) => {
    await evaluate(`(()=>{const e=${editor(side)};e.focus();e.setSelection(e.getModel().getFullModelRange());return true;})()`);
    await call('Input.insertText', { text: source });
    await until(`(${editor(side)})?.getModel().getValue()===${JSON.stringify(source)}`);
  };
  const open = async slug => {
    await selectLesson((await api('/api/lessons/'+slug)).title, slug);
    await until(`Boolean(document.querySelector('${entry}') && (${editor('A')}) && (${editor('B')}))`);
  };
  const texts = (selector, value) => `document.querySelector(${JSON.stringify(selector)})?.innerText.includes(${JSON.stringify(value)})`;
  const result = (side, value) => texts(`.tx-editor[data-side=${side}] header`, value);
  const run = side => click(`.tx-editor[data-side=${side}] .run-button`);

  await size(1720,1050);
  const xp = (await api('/api/course')).summary.xp;
  const oldPython = (await api('/api/lessons/is-vs-eq')).files;
  await open(booking);
  await button('.tx-toolbar', 'Открыть сессии');
  await until(result('B', 'Готова'));
  const lock = 'BEGIN; SELECT id FROM inventory WHERE id=1 FOR UPDATE';
  const wait = 'SELECT available FROM inventory WHERE id=1 FOR UPDATE';
  await fill('A', lock);
  await fill('B', wait);
  await run('A');
  await until(result('A', 'В транзакции'));
  await run('B');
  await until(result('B', 'Ждёт A'), 4000);
  await button('.tx-editor[data-side=A]', 'COMMIT');
  await until(texts('.tx-timeline', 'Ожидание завершено'));
  await until(result('B', 'Готова'));
  await until(texts('.tx-timeline', 'COMMIT'));
  await button('.tx-examples', 'Serializable');
  await until(texts('.tx-events', 'SQLSTATE 40001'));
  await evaluate(`Array.from(document.querySelectorAll('.lesson-mode-switch button')).find(b=>b.textContent.includes('Повторение')).click()`);
  assert.equal(await evaluate(`document.querySelector('.tx-workspace')!==null`), true);
  await evaluate(`Array.from(document.querySelectorAll('.lesson-mode-switch button')).find(b=>b.textContent.includes('Обучение')).click()`);
  await screenshot('/tmp/pythoria-phase9a-desktop.png');
  await size(390,844,true);
  await until(`document.querySelector('.course-sidebar').getBoundingClientRect().right<=0`);
  await button('.tx-tabs', 'Сессия B');
  await until(`getComputedStyle(document.querySelector('.tx-editor[data-side=A]')).display==='none'`);
  assert.equal(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`), true);
  await screenshot('/tmp/pythoria-phase9a-mobile.png');

  await size(1720,1050);
  await until(`document.querySelector('.course-sidebar').getBoundingClientRect().left>=-0.5`);
  await button('.tx-toolbar', 'Reset');
  await until(result('A', 'Готова') + ` && !document.querySelector('.tx-timeline')`);
  await until(`(${editor('A')})?.getModel().getValue()===${JSON.stringify(lock)}`);
  await open(dml);
  const correct = "UPDATE orders SET status='paid' WHERE id=10 RETURNING id,status";
  await fill('A', correct);
  await click('.tx-toolbar .check-button');
  await until(texts('.tx-workspace .sql-check-feedback.passed', '6 / 6'), 135000);
  assert.equal((await api(base+dml)).completed, true);
  await fill('A', "UPDATE orders SET status='paid' RETURNING id,status");
  await click('.tx-toolbar .check-button');
  await until(texts('.tx-workspace .sql-check-feedback.failed', 'Failed'), 135000);
  assert.equal((await api(base+dml)).completed, true);
  await fill('A', correct);
  const dark = await evaluate(`document.querySelector('.course-app').classList.contains('dark')`);
  await click('[aria-label="Сменить тему"]');
  await until(`document.querySelector('.course-app').classList.contains('dark')!==${dark}`);
  await call('Page.reload');
  await until(`document.querySelector('.tx-workspace .sql-task-completed')!==null && document.querySelector('.tx-editor textarea')!==null`);
  await evaluate(`new Promise((resolve,reject)=>window.require(['vs/editor/editor.main'],loaded=>{window.__phase8aMonaco=loaded.m||loaded;resolve(true)},reject))`);
  await until(`(${editor('A')})?.getModel().getValue()===${JSON.stringify(correct)}`);

  const oldSql = 's10-select-aliases-and-expressions';
  await selectLesson((await api('/api/lessons/'+oldSql)).title, oldSql);
  await until(`document.querySelector('.sql-workspace')!==null && document.querySelector('.tx-workspace')===null`);
  await selectLesson((await api('/api/lessons/is-vs-eq')).title, 'is-vs-eq');
  await until(`document.querySelector('.editor-panel textarea')!==null && document.querySelector('.tx-workspace')===null`);
  await open(booking);
  await until(`(${editor('A')})?.getModel().getValue()===${JSON.stringify(lock)} && (${editor('B')})?.getModel().getValue()===${JSON.stringify(wait)}`);
  assert.deepEqual((await api('/api/lessons/is-vs-eq')).files, oldPython);
  assert.equal((await api('/api/course')).summary.xp,xp);
  console.log(JSON.stringify({ transactionBrowser:true, independentMonaco:true, observedBlocking:true,
    commitRelease:true, serializable:true, validInvalidCheck:true, completionAfterReload:true,
    draftsAfterNavigation:true, preservedPython:true, theme:true, desktop:true, mobile:true, xpPreserved:true }));
}
