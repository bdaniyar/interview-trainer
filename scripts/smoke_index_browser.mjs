import assert from 'node:assert/strict';

export async function indexWalkthrough({api, evaluate, until, selectLesson, call, size, screenshot}) {
  const slug = 's11-pagination';
  const xp = (await api('/api/course')).summary.xp;
  const lesson = await api('/api/lessons/' + slug);
  await selectLesson(lesson.title, slug);
  const editor = "window.__phase8aMonaco.editor.getEditors().find(e=>e.getDomNode()?.closest('.index-workspace'))";
  await until(`Boolean(${editor})`);
  const solution = "SELECT id, created_at FROM orders WHERE created_at >= TIMESTAMP '2026-11-08' AND created_at < TIMESTAMP '2026-11-09' ORDER BY created_at,id LIMIT 30";
  async function type(sql) {
    await evaluate(`(()=>{const e=${editor}; e.focus(); e.setSelection(e.getModel().getFullModelRange()); return true;})()`);
    await call('Input.insertText', {text: sql});
    await until(`(${editor}).getModel().getValue()===${JSON.stringify(sql)}`);
  }
  await type(solution);
  await evaluate("document.querySelector('.index-workspace .run-button').click()");
  await until("document.querySelector('.index-workspace table[aria-label=\"Результат PostgreSQL\"]') && document.querySelector('.index-plan') && !document.querySelector('.index-workspace .run-button').disabled");
  assert.equal(await evaluate("document.querySelector('.index-plan').innerText.includes('Буферы') && document.querySelector('.index-plan').innerText.includes('факт 30')"), true);
  assert.equal((await api('/api/index-lab/lessons/' + slug)).completed, false);
  await evaluate("document.querySelector('.index-workspace .check-button').click()");
  await until("document.querySelector('.index-workspace .sql-check-feedback.passed')?.textContent.includes('6 / 6')", 120000);
  await type(solution.replace('created_at < TIMESTAMP', 'created_at <= TIMESTAMP'));
  await evaluate("document.querySelector('.index-workspace .check-button').click()");
  await until("document.querySelector('.index-workspace .sql-check-feedback.failed') && document.querySelector('.index-workspace .sql-task-completed')", 120000);
  await type(solution);
  await evaluate("Array.from(document.querySelectorAll('.lesson-mode-switch button')).find(b=>b.textContent.includes('Повторение')).click()");
  assert.equal(await evaluate("document.querySelector('.index-workspace')!==null"), true);
  await evaluate("Array.from(document.querySelectorAll('.lesson-mode-switch button')).find(b=>b.textContent.includes('Обучение')).click()");
  const dark = await evaluate("document.querySelector('.course-app').classList.contains('dark')");
  await evaluate("document.querySelector('[aria-label=\"Сменить тему\"]').click()");
  await until(`document.querySelector('.course-app').classList.contains('dark')!==${dark}`);
  await call('Page.reload');
  await until(`typeof window.require==='function' && !!document.querySelector('.index-workspace .monaco-editor')`);
  await evaluate(`new Promise((resolve,reject)=>window.require(['vs/editor/editor.main'],loaded=>{window.__phase8aMonaco=loaded.m||loaded;resolve(true)},reject))`);
  await until(`(${editor})?.getModel().getValue()===${JSON.stringify(solution)} && document.querySelector('.index-workspace .sql-task-completed')`);
  await evaluate("document.querySelector('.index-workspace .run-button').click()");
  await until("document.querySelector('.index-plan') && !document.querySelector('.index-workspace .run-button').disabled");
  await evaluate("document.querySelector('.index-plan').scrollIntoView({block:'center'})");
  await screenshot('/tmp/pythoria-phase9c-index-desktop.png');
  await size(390,844,true);
  await until("document.querySelector('.course-sidebar').getBoundingClientRect().right<=0");
  assert.equal(await evaluate('document.documentElement.scrollWidth<=window.innerWidth'), true);
  await evaluate("document.querySelector('.index-plan').scrollIntoView({block:'center'})");
  await screenshot('/tmp/pythoria-phase9c-index-mobile.png');
  await size(1720,1050);
  await until("document.querySelector('.course-sidebar').getBoundingClientRect().left>=-0.5");
  await evaluate("document.querySelector('.index-workspace .secondary-button').click()");
  assert.equal(await evaluate(`!document.querySelector('.index-plan') && (${editor}).getModel().getValue()===${JSON.stringify(solution)}`), true);
  assert.equal((await api('/api/index-lab/lessons/' + slug)).completed, true);
  const pooling = await api('/api/lessons/s11-connection-pooling');
  await selectLesson(pooling.title, pooling.slug);
  await until("document.querySelector('.pool-practice')?.innerText.includes('./check.sh answer.py')");
  assert.equal((await api('/api/course')).summary.xp, xp);
  console.log(JSON.stringify({indexLab:true, typedRows:true, actualPlan:true, correctAndIncorrectCheck:true,
    completionAndDraftReload:true, desktop1720:true, mobile390:true, resetPreservedProgress:true, sqlXpZero:true}));
}
