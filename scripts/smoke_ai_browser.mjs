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
    await until(`document.querySelector('.lesson-title-row h1')?.textContent===${JSON.stringify(item.title)}`);
  };
  const waitLesson = (slug) => until(`new URLSearchParams(location.search).get('lesson')===${JSON.stringify(slug)} && document.querySelector('.lesson-title-row h1')`);
  const currentTrack = () => evaluate(`document.querySelector('[aria-label="Учебный трек"]').value`);
  const changeTrack = (value) => evaluate(`(() => {
    const select = document.querySelector('[aria-label="Учебный трек"]');
    select.value = ${JSON.stringify(value)};
    select.dispatchEvent(new Event('change', {bubbles:true}));
  })()`);
  const hidden = () => evaluate(`(() => {
    const answers = Array.from(document.querySelectorAll('.answer-reveal,.lesson-disclosure'));
    return answers.length > 0 && answers.every(d=>!d.open);
  })()`);
  const loadEditor = async () => {
    await until(`typeof window.require==='function' && document.querySelector('.editor-panel textarea')`);
    await evaluate(`new Promise((resolve,reject)=>window.require(['vs/editor/editor.main'],loaded=>{window.__phase8aMonaco=loaded.m||loaded;resolve(true)},reject))`);
  };
  const submit = async (action) => {
    const button = JSON.stringify(`.workspace-actions .${action}-button`);
    const exit = "document.querySelector('.terminal-result-summary span:last-child')?.textContent";
    for (let attempt = 0; attempt < 2; attempt++) {
      await until(`document.querySelector(${button}) && !document.querySelector(${button}).disabled`);
      await click(JSON.parse(button));
      await until(`document.querySelector(${button}).disabled`);
      await until(`!document.querySelector(${button}).disabled && (${exit})?.startsWith('exit ')`);
      if (await evaluate(exit) !== 'exit 124') return;
      console.log(`Python sandbox timed out during ${action}. Repeating after preview settles.`);
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
    throw new Error(`Python sandbox timed out twice during ${action}`);
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
  await submit('run');
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
  const nextTheme = await evaluate(`document.querySelector('.course-app').classList.contains('dark')`) ? 'light' : 'dark';
  await click('[aria-label="Сменить тему"]');
  await until(`document.querySelector('.course-app.${nextTheme}')`);
  await call('Page.reload');
  await waitLesson(concept);
  await until(`document.querySelector('.course-app.${nextTheme}')`);

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
    await submit('check');
    await until(`document.querySelector('.terminal-result-summary .failed')?.textContent.endsWith(' / 11 tests')`);
    assert.equal((await api('/api/lessons/' + graded.slug)).progress.task_completed, false);
    const gradedSolution = await readFile(new URL('../content/ai-stage-03/ai03-direct-provider-adapter/solution/main.py', import.meta.url), 'utf8');
    await typePython(gradedSolution);
    await submit('run');
    await until(`document.querySelector('.terminal-result-summary')?.textContent.includes('exit 0')`);
    await submit('check');
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
  if ([29, 36, 46].includes(allAi.length)) {
    const r3 = allAi.length === 46;
    const r2 = allAi.length >= 36;
    const stageCounts = r3 ? [4, 10, 8, 7, 7, 10] : r2 ? [4, 10, 8, 7, 7] : [4, 10, 8, 7];
    assert.deepEqual(before.ai.modules.map(module => module.lessons.length), stageCounts);
    assert.equal(before.ai.roadmap.reduce((total, stage) => total + stage.planned, 0), 72 - allAi.length);
    for (const item of allAi) {
      await selectLesson(item);
      assert.equal(await hidden(), true);
      if (r3 && item.slug === 'ai06-pgvector-exact-search') {
        await until(`document.body.innerText.includes('Браузерный Check проверяет только Python oracle')`);
      }
      await click('.lesson-mode-switch button:nth-child(2)');
      assert.equal(await hidden(), true);
      await click('.lesson-mode-switch button:first-child');
    }
    await evaluate(`(() => {
      const create = URL.createObjectURL;
      const anchor = HTMLAnchorElement.prototype.click;
      URL.createObjectURL = blob => {
        window.__exportedNotes = blob.text();
        return create(blob);
      };
      HTMLAnchorElement.prototype.click = function () {
        window.__exportedFile = this.download;
      };
      try {
        Array.from(document.querySelectorAll('button')).find(b=>b.textContent==='Скачать Markdown').click();
      } finally {
        URL.createObjectURL = create;
        HTMLAnchorElement.prototype.click = anchor;
      }
    })()`);
    const last = allAi.at(-1);
    assert.equal(await evaluate('window.__exportedFile'), last.slug + '.md');
    const notes = await evaluate('window.__exportedNotes');
    assert.ok(notes.includes('# ' + last.title));
    assert.ok(notes.includes('Краткий конспект') && notes.includes('Источники'));
    await call('Page.reload');
    await waitLesson(last.slug);
    assert.equal(await currentTrack(), 'ai-engineering');
    const apiLab = r2 ? last : allAi.find(item => item.slug === 'ai04-extraction-api');
    const totalChecks = r3 ? 13 : r2 ? 22 : 14;
    if (r2) {
      await navigate(backend);
      await waitLesson(backend);
      await navigate(apiLab.slug);
      await waitLesson(apiLab.slug);
      await until(`document.querySelector('.lesson-title-row h1')?.textContent===${JSON.stringify(apiLab.title)}`);
      assert.equal(await currentTrack(), 'ai-engineering');
      assert.equal(await hidden(), true);
    } else {
      await selectLesson(apiLab);
    }
    await loadEditor();
    await submit('check');
    await until(`document.querySelector('.terminal-result-summary .failed')?.textContent.endsWith(' / ${totalChecks} tests')`);
    assert.equal((await api('/api/lessons/' + apiLab.slug)).progress.task_completed, false);
    const stage = r3 ? 'ai-stage-06' : r2 ? 'ai-stage-05' : 'ai-stage-04';
    const apiSolution = await readFile(new URL(`../content/${stage}/${apiLab.slug}/solution/main.py`, import.meta.url), 'utf8');
    await typePython(apiSolution);
    await submit('run');
    await until(`document.querySelector('.terminal-result-summary')?.textContent.includes('exit 0')`);
    await submit('check');
    await until(`document.querySelector('.terminal-result-summary .passed')?.textContent==='${totalChecks} / ${totalChecks} tests'`);
    await call('Page.reload');
    await waitLesson(apiLab.slug);
    const savedLab = await api('/api/lessons/' + apiLab.slug);
    assert.equal(savedLab.files['main.py'], apiSolution);
    assert.equal(savedLab.progress.task_completed, true);
    console.log(JSON.stringify({aiLessons:allAi.length, stageCounts, markdownExport:true, notesAfterReload:true, failedCheck:true, passedCheck:totalChecks}));
  }
  console.log(JSON.stringify({aiNavigation:true, trackProgress:true, learnReview:true, monacoRun:true, savedFiles:true, reload:true, mobile390:true, themes:true, deepLink:true}));
}
