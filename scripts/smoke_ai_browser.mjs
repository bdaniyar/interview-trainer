import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

export async function aiWalkthrough({ call, evaluate, until, click, typePython, type, api, size, frontendOrigin }) {
  const backend = 'is-vs-eq';
  const concept = 'ai01-ai-roles-and-boundaries';
  const selectLesson = async (item) => {
    await type('.lesson-search input', item.title);
    const button = `Array.from(document.querySelectorAll('.course-sidebar button.lesson')).find(b=>b.textContent.includes(${JSON.stringify(item.title)}))`;
    await until(button);
    await evaluate(`(${button}).click()`);
    await waitLesson(item.slug);
  };
  const waitLesson = (slug) => until(`new URLSearchParams(location.search).get('lesson')===${JSON.stringify(slug)} && document.querySelector('.lesson-title-row h1')`);
  const currentTrack = () => evaluate(`document.querySelector('[aria-label="Учебный трек"]').value`);
  const changeTrack = (value) => evaluate(`(() => {
    const select = document.querySelector('[aria-label="Учебный трек"]');
    select.value = ${JSON.stringify(value)};
    select.dispatchEvent(new Event('change', {bubbles:true}));
  })()`);
  const hidden = () => evaluate(`Array.from(document.querySelectorAll('.answer-reveal,.lesson-disclosure')).every(d=>!d.open)`);
  const loadEditor = async () => {
    await until(`typeof window.require==='function' && document.querySelector('.editor-panel textarea')`);
    await evaluate(`new Promise((resolve,reject)=>window.require(['vs/editor/editor.main'],loaded=>{window.__phase8aMonaco=loaded.m||loaded;resolve(true)},reject))`);
  };
  const navigate = (slug = '') => call('Page.navigate', {url: frontendOrigin + '/' + (slug ? '?lesson=' + slug : '')});

  await navigate(backend);
  await waitLesson(backend);
  assert.equal(await currentTrack(), 'backend');
  const before = await api('/api/course');
  const backendFiles = (await api('/api/lessons/' + backend)).files;
  const allAi = before.ai.modules.flatMap(module => module.lessons);
  await changeTrack('ai-engineering');
  await waitLesson(allAi[0].slug);
  if (allAi[0].slug !== concept) await selectLesson(allAi.find(item => item.slug === concept));
  assert.equal(await currentTrack(), 'ai-engineering');
  assert.equal(await evaluate(`document.querySelector('.course-progress b').textContent`), before.ai.summary.percent + '%');
  assert.equal(await hidden(), true);
  await click('.answer-reveal summary');
  assert.equal(await hidden(), false);
  await click('.lesson-mode-switch button:nth-child(2)');
  assert.equal(await hidden(), true);
  await click('.lesson-mode-switch button:first-child');
  assert.equal(await hidden(), true);
  await type('.lesson-search input', 'identity');
  await until(`document.querySelectorAll('.course-sidebar .lesson-list .lesson').length===0`);
  await type('.lesson-search input', 'Deep Learning');
  await until(`document.querySelectorAll('.course-sidebar .lesson-list .lesson').length===1`);

  await loadEditor();
  const solution = await readFile(new URL('../content/ai-stage-01/ai01-ai-roles-and-boundaries/solution/main.py', import.meta.url), 'utf8');
  await typePython(solution);
  await click('.workspace-actions .run-button');
  await until(`document.querySelector('.terminal-panel')?.innerText.includes('Черновик: llm')`);
  await click('.theory-complete-card button');
  await until(`document.querySelector('.theory-complete-card strong')?.textContent==='Урок отмечен'`);
  const after = await api('/api/course');
  assert.equal(after.ai.summary.completed, before.ai.summary.completed + 1);
  assert.equal(after.summary.completed, before.summary.completed);
  assert.equal(after.summary.xp, before.summary.xp + 5);

  await changeTrack('backend');
  await waitLesson(backend);
  assert.deepEqual((await api('/api/lessons/' + backend)).files, backendFiles);
  await changeTrack('ai-engineering');
  await waitLesson(concept);
  assert.equal((await api('/api/lessons/' + concept)).files['main.py'], solution);
  await navigate();
  await waitLesson(concept);
  await size(390, 844, true);
  await until(`document.querySelector('.course-sidebar')?.getBoundingClientRect().right<=0`);
  await click('.mobile-menu');
  await until(`document.querySelector('.course-sidebar')?.getBoundingClientRect().left>=-1`);
  await click('.mobile-sidebar-head button');
  assert.equal(await evaluate(`document.documentElement.scrollWidth<=innerWidth`), true);
  await click('[aria-label="Сменить тему"]');
  await until(`document.querySelector('.course-app.light')`);
  await call('Page.reload');
  await waitLesson(concept);
  await until(`document.querySelector('.course-app.light')`);

  await changeTrack('backend');
  await waitLesson(backend);
  await navigate(concept);
  await waitLesson(concept);
  assert.equal(await currentTrack(), 'ai-engineering');
  await size(1720, 1050);
  const graded = allAi.find(item => item.slug === 'ai03-direct-provider-adapter');
  if (graded) {
    // A deep-linked lesson in another AI module must select the right sidebar.
    await selectLesson(graded);
    assert.equal(await hidden(), true);
    await loadEditor();
    await click('.workspace-actions .check-button');
    await until(`document.querySelector('.terminal-result-summary .failed')?.textContent==='0 / 11 tests'`);
    assert.equal((await api('/api/lessons/' + graded.slug)).progress.task_completed, false);
    const gradedSolution = await readFile(new URL('../content/ai-stage-03/ai03-direct-provider-adapter/solution/main.py', import.meta.url), 'utf8');
    await typePython(gradedSolution);
    await click('.workspace-actions .run-button');
    await until(`document.querySelector('.terminal-result-summary')?.textContent.includes('exit 0')`);
    await click('.workspace-actions .check-button');
    await until(`document.querySelector('.terminal-result-summary .passed')?.textContent==='11 / 11 tests'`);
    await until(`document.querySelector('.lesson-title-row .status-pill')?.textContent==='completed'`);
    const result = await api('/api/course');
    assert.equal(result.ai.summary.completed, after.ai.summary.completed + 1);
    assert.equal(result.summary.completed, before.summary.completed);
    assert.equal(result.summary.xp, after.summary.xp + 20);
    await changeTrack('backend');
    await waitLesson(backend);
    await changeTrack('ai-engineering');
    await waitLesson(graded.slug);
    assert.equal((await api('/api/lessons/' + graded.slug)).files['main.py'], gradedSolution);
    await call('Page.reload');
    await waitLesson(graded.slug);
    assert.equal((await api('/api/lessons/' + graded.slug)).progress.task_completed, true);
    console.log(JSON.stringify({aiGraded:true, failedCheck:true, passedCheck:11, xp:20, savedFiles:true, completionAfterReload:true}));
  }
  console.log(JSON.stringify({aiNavigation:true, trackProgress:true, learnReview:true, monacoRun:true, savedFiles:true, reload:true, mobile390:true, themes:true, deepLink:true}));
}
